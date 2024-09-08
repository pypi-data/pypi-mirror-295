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
from keras_nlp.src.models.preprocessor import Preprocessor
from keras_nlp.src.utils.tensor_utils import strip_to_ragged
from keras_nlp.src.utils.tensor_utils import tf_preprocessing_function


@keras_nlp_export("keras_nlp.models.CausalLMPreprocessor")
class CausalLMPreprocessor(Preprocessor):
    """Base class for causal language modeling preprocessing layers.

    `CausalLMPreprocessor` tasks wrap a `keras_nlp.tokenizer.Tokenizer` to
    create a preprocessing layer for causal language modeling tasks. It is
    intended to be paired with a `keras.models.CausalLM` task.

    All `CausalLMPreprocessor` take inputs a single input. This can be a single
    string or a batch of strings. See examples below. These inputs
    will be tokenized and padded/truncated to a fixed sequence length.

    This layer will always output a `(x, y, sample_weight)` tuple, where `x`
    is a dictionary with the tokenized inputs, `y` contains the tokens from `x`
    offset by 1, and `sample_weight` marks where `y` contains padded
    values. The exact contents of `x` will vary depending on the model being
    used.

    a `CausalLMPreprocessor` contains two extra methods, `generate_preprocess`
    and `generate_postprocess` for use with generation. See examples below.

    All `CausalLMPreprocessor` tasks include a `from_preset()` constructor
    which can be used to load a pre-trained config and vocabularies. You can
    call the `from_preset()` constructor directly on this base class, in which
    case the correct class for you model will be automatically instantiated.

    Examples.
    ```python
    preprocessor = keras_nlp.models.CausalLMPreprocessor.from_preset(
        "bert_base_en_uncased",
        sequence_length=256, # Optional.
    )

    # Tokenize, mask and pack a single sentence.
    x = "The quick brown fox jumped."
    x, y, sample_weight = preprocessor(x)

    # Tokenize and pad/truncate a batch of labeled sentences.
    x = ["The quick brown fox jumped.", "Call me Ishmael."]
    x, y, sample_weight = preprocessor(x)

    # With a `tf.data.Dataset`.
    ds = tf.data.Dataset.from_tensor_slices(x)
    ds = ds.map(preprocessor, num_parallel_calls=tf.data.AUTOTUNE)

    # Generate preprocess and postprocess.
    x = preprocessor.generate_preprocess(x)  # Tokenized numeric inputs.
    x = preprocessor.generate_postprocess(x)  # Detokenized string outputs.
    ```
    """

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
        x = self.tokenizer(x)
        # Pad with one extra token to account for the truncation below.
        token_ids, padding_mask = self.packer(
            x,
            sequence_length=sequence_length + 1,
            add_start_value=self.add_start_token,
            add_end_value=self.add_end_token,
        )
        # The last token does not have a next token, so we truncate it out.
        x = {
            "token_ids": token_ids[..., :-1],
            "padding_mask": padding_mask[..., :-1],
        }
        # Target `y` will be the next token.
        y, sample_weight = token_ids[..., 1:], padding_mask[..., 1:]
        return keras.utils.pack_x_y_sample_weight(x, y, sample_weight)

    @tf_preprocessing_function
    def generate_preprocess(
        self,
        x,
        sequence_length=None,
    ):
        """Convert strings to integer token input for generation.

        Similar to calling the layer for training, this method takes in strings
        or tensor strings, tokenizes and packs the input, and computes a padding
        mask masking all inputs not filled in with a padded value.

        Unlike calling the layer for training, this method does not compute
        labels and will never append a `tokenizer.end_token_id` to the end of
        the sequence (as generation is expected to continue at the end of the
        inputted prompt).
        """
        if not self.built:
            self.build(None)

        x = self.tokenizer(x)
        token_ids, padding_mask = self.packer(
            x, sequence_length=sequence_length, add_end_value=False
        )
        return {
            "token_ids": token_ids,
            "padding_mask": padding_mask,
        }

    @tf_preprocessing_function
    def generate_postprocess(
        self,
        x,
    ):
        """Convert integer token output to strings for generation.

        This method reverses `generate_preprocess()`, by first removing all
        padding and start/end tokens, and then converting the integer sequence
        back to a string.
        """
        if not self.built:
            self.build(None)

        token_ids, padding_mask = x["token_ids"], x["padding_mask"]
        ids_to_strip = self.tokenizer.special_token_ids
        token_ids = strip_to_ragged(token_ids, padding_mask, ids_to_strip)
        return self.tokenizer.detokenize(token_ids)

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
