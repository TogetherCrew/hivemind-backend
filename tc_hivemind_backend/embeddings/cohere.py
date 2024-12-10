import os

import cohere
from dotenv import load_dotenv
from llama_index.core.base.embeddings.base import BaseEmbedding
from tc_hivemind_backend.db.utils.preprocess_text import BasePreprocessor


class CohereEmbedding(BaseEmbedding):
    def __init__(self):
        super().__init__()

    def prepare_cohere(
        self,
    ) -> cohere.Client:
        """
        setup cohere client
        https://cohere.com/


        Returns
        --------
        client : cohere.Client
            the cohere client to query anything
        """
        load_dotenv()
        key = os.getenv("COHERE_API_KEY")

        client = cohere.Client(key)
        return client

    def get_text_embedding(
        self, text: str | None = None, texts: list[str] | None = None
    ) -> list[float] | list[list[float]]:
        co = self.prepare_cohere()
        processor = BasePreprocessor()

        if text is not None:
            cleaned_text = self._clean_text(text, processor)
            response = co.embed(
                texts=[cleaned_text],
                model="embed-multilingual-v3.0",
                input_type="classification",
                truncate=None,
            )
            # checking the output to be right
            assert len(response.embeddings) == 1

            return response.embeddings[0]
        elif texts is not None:
            cleaned_texts = [self._clean_text(text, processor) for text in texts]
            response = co.embed(
                texts=cleaned_texts,
                model="embed-multilingual-v3.0",
                input_type="classification",
                truncate=None,
            )
            return response.embeddings
        else:
            raise ValueError("Both inputs cannot be None")

    def _get_text_embeddings(self, texts: list[str]) -> list[list[float]]:
        """Get text embeddings.

        By default, this is a wrapper around _get_text_embedding.
        Can be overridden for batch queries.

        """
        return self.get_text_embedding(texts=texts)  # type: ignore

    def _get_text_embedding(self, text: str) -> list[float]:
        """Get text embedding."""
        return self.get_text_embedding(text=text)  # type: ignore

    def _get_query_embedding(self, query: str) -> list[float]:
        """Get query embedding."""
        return self.get_text_embedding(text=query)  # type: ignore

    async def _aget_query_embedding(self, query: str) -> list[float]:
        """The asynchronous version of _get_query_embedding."""
        raise NotImplementedError("Not implemented!")

    def _clean_text(self, text: str, processor: BasePreprocessor) -> str:
        """
        clean the provided text by removing
        stop words, removing urls, ascii codes, ...

        Parameters
        ------------
        text : str
            the text data to be cleaned

        Returns
        ---------
        cleaned_text : str
            the cleaned text data
        """
        cleaned_text = processor.extract_main_content(text)
        return cleaned_text
