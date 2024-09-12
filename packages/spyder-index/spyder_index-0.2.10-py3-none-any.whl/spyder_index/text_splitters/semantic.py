from typing import Literal, List

from spyder_index.core.document import Document
from spyder_index.core.embeddings import BaseEmbedding
from pydantic.v1 import BaseModel

from langchain_experimental.text_splitter import SemanticChunker


class SemanticSplitter(BaseModel):
    """Python class designed to split text into chunks using semantic understanding.

    Note:
        Credit to Greg Kamradt's notebook: `5 Levels Of Text Splitting <https://github.com/FullStackRetrieval-com/RetrievalTutorials/blob/main/tutorials/LevelsOfTextSplitting/5_Levels_Of_Text_Splitting.ipynb>`_.

    Args:
        embed_model (BaseEmbedding): Embedding model to use.
        buffer_size (int, optional): Size of the buffer for semantic chunking. Default is ``1``.
        breakpoint_threshold_amount (int, optional): Threshold percentage for detecting breakpoints. Default is ``95``.
        device (str, optional): Device to use for processing, either "cpu" or "cuda". Default is ``cpu``.
    """

    embed_model: BaseEmbedding
    buffer_size: int = 1
    breakpoint_threshold_amount: int = 95
    device: Literal["cpu", "cuda"] = "cpu"

    class Config:
        arbitrary_types_allowed = True

    def from_text(self, text: str) -> List[str]:
        """Split text into chunks.
        
        Args:
            text (str): Input text to split.
        """

        text_splitter = SemanticChunker(
            embeddings=self.embed_model,
            buffer_size=self.buffer_size,
            breakpoint_threshold_amount=self.breakpoint_threshold_amount)

        return text_splitter.split_text(text)

    def from_documents(self, documents: List[Document]) -> List[Document]:
        """Split documents into chunks.
        
        Args:
            documents (List[Document]): List of ``Document``
        """

        chunks = []

        for document in documents:
            texts = self.from_text(document.get_content())

            for text in texts:
                chunks.append(Document(text=text, metadata=document.get_metadata()))

        return chunks
