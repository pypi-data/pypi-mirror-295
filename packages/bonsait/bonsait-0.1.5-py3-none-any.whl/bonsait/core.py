import logging
from typing import Iterable, Optional, Union

import torch

from bonsait.cache import BaseClass, EmbeddingCache
from bonsait.configs import BONSAI_ACTIVITY_API, DEFAULT_MODEL
from bonsait.models import Encoder
from bonsait.utils.similarity_func import calc_cosine_similarity


class BonsaiTransformer:
    def __init__(
        self,
        model: Optional[Encoder] = None,
        device: str = "cpu",
    ) -> None:
        if model is None:
            print(f"No model is provided, the default model {DEFAULT_MODEL} is used")
            model = Encoder.from_sentence_transformer(model_name=DEFAULT_MODEL)
        self._model = model
        self._device = device

        self._source_class = None
        self._target_class = None

    def set_target_class(self, target_class: BaseClass = None):
        if target_class is None:
            target_class = BaseClass.from_bonsai(name="activity")
            print(
                f"get BONSAI activity classification as the default target classification from {BONSAI_ACTIVITY_API}"
            )
        self._target_class = target_class

    def set_source_class(self, source_class: Union[str, list]):
        # TODO: add support for multiple source classes
        self._source_class = source_class

    def encode_source_class(self) -> torch.Tensor:
        array_source = self._model.encode(self._source_class).unsqueeze(0)
        return array_source

    def encode_target_class(self, cache: EmbeddingCache = EmbeddingCache()):
        # self.set_target_class(target_class)
        if not self._target_class:
            raise ValueError("target_class is not set")
        class_embedding_cached = cache.load_embedding(
            class_value=self._target_class.values
        )
        if class_embedding_cached is not None:
            logging.info("Using cached classifications")
            return class_embedding_cached
        else:
            print(f"Start encoding {self._target_class.name}")
            # TODO: add parallelism here
            class_embedding = [
                self._model.encode(classification)
                for classification in self._target_class.values
            ]
            cache.save_embedding(
                encoding=class_embedding, class_value=self._target_class.values
            )
            return class_embedding

    def match(
        self,
        source_class: Optional[str] = None,
        target_class: Optional[BaseClass] = None,
        similarity_func: Optional[callable] = None,
        top_k: int = 1,
    ):
        """
        Computes the correspondence classification from target_class
        that is most similar to the source_class based on cosine similarity.

        Returns the top `top_k` most similar matches.
        """

        self.set_source_class(source_class)
        source_vector = self.encode_source_class()
        self.set_target_class(target_class)
        target_vectors = self.encode_target_class()

        # Stack all target vectors to create the target matrix
        target_matrix = torch.stack(target_vectors).to(self._device)

        if similarity_func is None:
            logging.info(
                f"No similarity func provided, using the default cosine similarity: {calc_cosine_similarity.__name__}"
            )
            similarity_func = calc_cosine_similarity

        # Compute similarity scores
        similarity_scores = similarity_func(source_vector, target_matrix)

        # Get the top `top_k` most similar indices
        top_k_indices = (
            torch.topk(similarity_scores, k=top_k, dim=1).indices.squeeze().tolist()
        )

        # Handle the case where top_k == 1 and top_k_indices is not a list
        if isinstance(top_k_indices, int):
            top_k_indices = [top_k_indices]

        # Return the corresponding target class values for the top matches
        return [self._target_class.values[idx] for idx in top_k_indices]
