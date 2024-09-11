from typing import List, Optional

import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.models import Transformer
from transformers import (
    PreTrainedTokenizerBase,
    TrainerCallback,
    TrainerControl,
    TrainerState,
    TrainingArguments,
)

from word_injection.model import ExtendableSentenceTransformer


class ResetFixedEmbeddingsCallback(TrainerCallback):
    """
    A SentenceTransformerTrainer callback that resets the fixed embeddings of the model to their original values.
    """

    def __init__(self, trainable_indices: List[int] = None):
        self._trainable_indices: List[int] = trainable_indices or []
        self._original: Optional[torch.Tensor] = None
        self._fixed_tokens_mask: Optional[List[int]] = None

    def add_trainable_index(self, index: int):
        """Add an index to the list of trainable indices"""
        if index in self._trainable_indices:
            raise ValueError(f"Index {index} is already trainable")

        self._trainable_indices.append(index)

    def on_train_begin(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        """Keep the original state of the input token embeddings"""
        # Create a mask for fixed tokens
        tokenizer: PreTrainedTokenizerBase = kwargs.get("tokenizer")
        vocab_size = len(tokenizer.get_vocab())
        self._fixed_tokens_mask = list(
            set(range(vocab_size)) - set(self._trainable_indices)
        )

        # Get the model that the callback is attached to
        model: ExtendableSentenceTransformer = kwargs.get("model")
        first_module: Transformer = model._first_module()  # noqa

        # Keep the original embeddings
        self._original = (
            first_module.auto_model.embeddings.word_embeddings.weight.detach().clone()
        )

    def on_train_end(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        """Clean the state of the callback"""
        self._original = None
        self._fixed_tokens_mask = None

    def on_step_end(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        """Revert the fixed embeddings to their original values"""
        model: SentenceTransformer = kwargs.get("model")
        first_module: Transformer = model._first_module()  # noqa
        embeddings = first_module.auto_model.embeddings

        # Change the fixed dimensions back to their original values
        with torch.no_grad():
            embeddings.word_embeddings.weight[self._fixed_tokens_mask] = self._original[
                self._fixed_tokens_mask
            ]
