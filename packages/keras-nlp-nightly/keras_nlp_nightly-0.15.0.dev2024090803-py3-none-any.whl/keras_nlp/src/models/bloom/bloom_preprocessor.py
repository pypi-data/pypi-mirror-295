# Copyright 2024 The KerasNLP Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import keras

from keras_nlp.src.api_export import keras_nlp_export
from keras_nlp.src.layers.preprocessing.start_end_packer import StartEndPacker
from keras_nlp.src.models.bloom.bloom_backbone import BloomBackbone
from keras_nlp.src.models.bloom.bloom_tokenizer import BloomTokenizer
from keras_nlp.src.models.preprocessor import Preprocessor
from keras_nlp.src.utils.tensor_utils import tf_preprocessing_function


@keras_nlp_export("keras_nlp.models.BloomPreprocessor")
class BloomPreprocessor(Preprocessor):
    """BLOOM preprocessing layer which tokenizes and packs inputs.

    This preprocessing layer will do 2 things:

    - Tokenize the inputs using the `tokenizer`.
    - Construct a dictionary with keys `"token_ids"`, `"padding_mask"`, that can
        be passed directly to a `keras_nlp.models.BloomBackbone`.

    This layer can be used directly with `tf.data.Dataset.map` to preprocess
    string data in the `(x, y, sample_weight)` format used by
    `keras.Model.fit`.

    The call method of this layer accepts three arguments, `x`, `y`, and
    `sample_weight`. `x` can be a python string or tensor representing a single
    segment, a list of python strings representing a batch of single segments,
    or a list of tensors representing multiple segments to be packed together.
    `y` and `sample_weight` are both optional, can have any format, and will be
    passed through unaltered.

    Args:
        tokenizer: A `keras_nlp.models.BloomTokenizer` instance.
        sequence_length: The length of the packed inputs.
        add_start_token: If `True`, the preprocessor will prepend the tokenizer
            start token to each input sequence.
        add_end_token: If `True`, the preprocessor will append the tokenizer
            end token to each input sequence.

    Call arguments:
        x: A string, `tf.Tensor` or list of python strings.
        y: Any label data. Will be passed through unaltered.
        sample_weight: Any label weight data. Will be passed through unaltered.
        sequence_length: Pass to override the configured `sequence_length` of
            the layer.

    Examples:

    Directly calling the layer on data.
    ```python
    preprocessor = keras_nlp.models.BloomPreprocessor.from_preset(
        "bloom_560m_multi"
    )
    # Tokenize and pack a single sentence.
    preprocessor("The quick brown fox jumped.")

    # Tokenize a batch of single sentences.
    preprocessor(["The quick brown fox jumped.", "Call me Ishmael."])

    # Custom vocabulary.
    features = ["a quick fox.", "a fox quick."]
    vocab = {"<pad>": 0, "<s>":1, "</s>":2, "a": 3, "Ġquick": 4, "Ġfox": 5}
    merges = ["Ġ q", "u i", "c k", "ui ck", "Ġq uick"]
    merges += ["Ġ f", "o x", "Ġf ox"]
    tokenizer = keras_nlp.models.BloomTokenizer(
        vocabulary=vocab,
        merges=merges,
    )
    preprocessor = keras_nlp.models.BloomPreprocessor(tokenizer=tokenizer)
    preprocessor("The quick brown fox jumped.")
    ```

    Mapping with `tf.data.Dataset`.
    ```python
    preprocessor = keras_nlp.models.BloomPreprocessor.from_preset(
        "bloom_560m_multi"
    )

    text = tf.constant(["The quick brown fox jumped.", "Call me Ishmael."])
    label = tf.constant([1, 1])

    # Map labeled single sentences.
    ds = tf.data.Dataset.from_tensor_slices((text, label))
    ds = ds.map(preprocessor, num_parallel_calls=tf.data.AUTOTUNE)

    # Map unlabeled single sentences.
    ds = tf.data.Dataset.from_tensor_slices(text)
    ds = ds.map(preprocessor, num_parallel_calls=tf.data.AUTOTUNE)
    ```
    """

    backbone_cls = BloomBackbone
    tokenizer_cls = BloomTokenizer

    def __init__(
        self,
        tokenizer,
        sequence_length=1024,
        add_start_token=True,
        add_end_token=True,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.tokenizer = tokenizer
        self.packer = None
        self.sequence_length = sequence_length
        self.add_start_token = add_start_token
        self.add_end_token = add_end_token

    def build(self, input_shape):
        # Defer packer creation to `build()` so that we can be sure tokenizer
        # assets have loaded when restoring a saved model.
        self.packer = StartEndPacker(
            start_value=self.tokenizer.start_token_id,
            end_value=self.tokenizer.end_token_id,
            pad_value=self.tokenizer.pad_token_id,
            sequence_length=self.sequence_length,
            return_padding_mask=True,
        )
        self.built = True

    @tf_preprocessing_function
    def call(
        self,
        x,
        y=None,
        sample_weight=None,
        sequence_length=None,
    ):
        sequence_length = sequence_length or self.sequence_length
        token_ids, padding_mask = self.packer(
            self.tokenizer(x),
            sequence_length=sequence_length,
            add_start_value=self.add_start_token,
            add_end_value=self.add_end_token,
        )
        x = {
            "token_ids": token_ids,
            "padding_mask": padding_mask,
        }
        return keras.utils.pack_x_y_sample_weight(x, y, sample_weight)

    def get_config(self):
        config = super().get_config()
        config.update(
            {
                "sequence_length": self.sequence_length,
                "add_start_token": self.add_start_token,
                "add_end_token": self.add_end_token,
            }
        )
        return config

    @property
    def sequence_length(self):
        """The padded length of model input sequences."""
        return self._sequence_length

    @sequence_length.setter
    def sequence_length(self, value):
        self._sequence_length = value
        if self.packer is not None:
            self.packer.sequence_length = value
