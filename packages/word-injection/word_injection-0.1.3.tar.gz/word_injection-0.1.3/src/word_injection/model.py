import logging
from typing import Any, Dict, Iterable, List, Optional, Union

import torch
from sentence_transformers import (
    SentenceTransformer,
    SentenceTransformerModelCardData,
    SimilarityFunction,
)
from sentence_transformers.models import Pooling, Transformer
from torch import nn
from transformers import BertModel

logger = logging.getLogger(__name__)


class ExtendableSentenceTransformer(SentenceTransformer):
    """
    An extendable SentenceTransformer allows to specify tokens with trainable input embeddings, while keeping the rest
    of them fixed. This is useful when we want to fine-tune the model with new tokens, and add new items to the
    vocabulary, without impacting the existing embeddings.
    """

    def __init__(
        self,
        model_name_or_path: Optional[str] = None,
        modules: Optional[Iterable[nn.Module]] = None,
        device: Optional[str] = None,
        prompts: Optional[Dict[str, str]] = None,
        default_prompt_name: Optional[str] = None,
        similarity_fn_name: Optional[Union[str, SimilarityFunction]] = None,
        cache_folder: Optional[str] = None,
        trust_remote_code: bool = False,
        revision: Optional[str] = None,
        local_files_only: bool = False,
        token: Optional[Union[bool, str]] = None,
        use_auth_token: Optional[Union[bool, str]] = None,
        truncate_dim: Optional[int] = None,
        model_kwargs: Optional[Dict[str, Any]] = None,
        tokenizer_kwargs: Optional[Dict[str, Any]] = None,
        config_kwargs: Optional[Dict[str, Any]] = None,
        model_card_data: Optional[SentenceTransformerModelCardData] = None,
    ) -> None:
        super().__init__(
            model_name_or_path,
            modules,
            device,
            prompts,
            default_prompt_name,
            similarity_fn_name,
            cache_folder,
            trust_remote_code,
            revision,
            local_files_only,
            token,
            use_auth_token,
            truncate_dim,
            model_kwargs,
            tokenizer_kwargs,
            config_kwargs,
            model_card_data,
        )

        # Restrict the training to the input embeddings only
        self._transformer: Transformer = self[0]
        assert isinstance(self._transformer.auto_model, BertModel)
        for name, param in self._transformer.auto_model.named_parameters():
            # TODO: check if the name is correct for all models
            if "embeddings.word_embeddings.weight" == name:
                param.requires_grad = True
                continue
            param.requires_grad = False

    def add_token(
        self, token: str, init_from_tokens: List[Union[str, int]] = None
    ) -> int:
        """
        Add a new token to the vocabulary.
        :param token:
        :param init_from_tokens:
        :return: the id of the new token
        """
        if token in self._transformer.tokenizer.vocab.keys():
            return self.token_to_id(token)

        # Add token to the tokenizer and resize the embeddings to include it
        num_added_tokens = self._transformer.tokenizer.add_tokens([token])
        logger.info("Added %d tokens to the vocabulary", num_added_tokens)
        self._transformer.auto_model.resize_token_embeddings(
            len(self._transformer.tokenizer)
        )

        # Get the id of the new token
        new_token_id = self.token_to_id(token)
        if not init_from_tokens:
            return new_token_id

        # Initialize the new token embeddings with an average of the provided tokens
        init_embeddings = self.get_input_token_embeddings(init_from_tokens)
        with torch.no_grad():
            self._transformer.auto_model.embeddings.word_embeddings.weight[
                new_token_id
            ] = init_embeddings.mean(dim=0)

        return new_token_id

    def get_tokenization(
        self, text: str, skip_special_tokens: bool = True
    ) -> List[str]:
        """
        Tokenize the text.
        :param text:
        :param skip_special_tokens:
        :return:
        """
        token_ids = self._transformer.tokenize([text])["input_ids"][0].tolist()
        return self._transformer.tokenizer.convert_ids_to_tokens(
            token_ids,
            skip_special_tokens=skip_special_tokens,
        )

    def extract_unknown_words(self, text: str) -> List[str]:
        """
        Extract words which were considered as unknown tokens during tokenization.
        :param text:
        :return:
        """
        tokenization = self._transformer.tokenizer(text, add_special_tokens=False)
        tokens = tokenization.tokens()
        words = tokenization.words()
        unknown_word_spans = [
            tokenization.word_to_chars(word_id)
            for token, word_id in zip(tokens, words)
            if token == self._transformer.tokenizer.unk_token
        ]
        return [text[span.start : span.end] for span in unknown_word_spans]

    def get_input_token_embeddings(
        self, tokens: Optional[List[Union[str, int]]] = None
    ) -> torch.Tensor:
        """
        Get the input embeddings for multiple tokens (all by default).
        :return:
        """
        all_weights = self[0].auto_model.embeddings.word_embeddings.weight
        if tokens is None:
            return all_weights.detach().clone()

        token_ids = [self.token_to_id(token) for token in tokens]
        return all_weights[token_ids].detach().clone()

    def get_input_token_embedding(self, token: Union[str, int]) -> torch.Tensor:
        """
        Get the input embedding for the token.
        :param token:
        :return:
        """
        token_id = self.token_to_id(token)
        return (
            self[0]
            .auto_model.embeddings.word_embeddings.weight[token_id]
            .detach()
            .clone()
        )

    def get_closest_input_embeddings(
        self, token: Union[str, int], k: int = 5
    ) -> Dict[str, float]:
        """
        Get the closest input embeddings to the token. The embeddings are compared using cosine similarity.
        :param token:
        :param k:
        :return:
        """
        token_embedding = self.get_input_token_embedding(token)
        embeddings = self[0].auto_model.embeddings.word_embeddings.weight
        with torch.no_grad():
            similarities = torch.nn.functional.cosine_similarity(
                embeddings, token_embedding.unsqueeze(0), dim=-1
            )
            similarities = similarities.squeeze()
            _, indices = torch.topk(similarities, k=k)
            return {
                self._transformer.tokenizer.convert_ids_to_tokens(i.item()): s.item()
                for i, s in zip(indices, similarities[indices])
            }

    def get_vocabulary_size(self) -> int:
        """
        Get the size of the vocabulary.
        :return:
        """
        return len(self._transformer.tokenizer.get_vocab())

    def to_cls_pooling(self) -> SentenceTransformer:
        """
        Convert the model to a SentenceTransformer with a CLS pooling.
        :return:
        """
        assert isinstance(self[0], Transformer)
        pooling_model = Pooling(self[0].get_word_embedding_dimension(), "cls")
        model = SentenceTransformer(modules=[self[0], pooling_model])
        return model

    def token_to_id(self, token: Union[str, int]) -> int:
        """
        Convert token to its id.
        :param token:
        :return:
        """
        if isinstance(token, str):
            return self._transformer.tokenizer.vocab[token]
        return token

    def id_to_token(self, token_id: int) -> str:
        """
        Convert token id to its string representation.
        :param token_id:
        :return:
        """
        return self._transformer.tokenizer.convert_ids_to_tokens(token_id)
