import uuid

from typing import List
from spyder_index.core.document import Document
from spyder_index.core.embeddings import BaseEmbedding
from spyder_index.core.vector_stores import VectorStoreQueryResult


class ChromaVectorStore:
    """Chroma is the AI-native open-source vector database. Embeddings are stored within a ChromaDB collection.

    Args:
        collection_name (str): Name of the ChromaDB collection.
        embed_model (BaseEmbedding): Embedding model to use.
        distance_strategy (str, optional): Distance strategy for similarity search. Defaults to ``cosine``.
    """

    def __init__(self, collection_name: str = "chroma-index-" + str(uuid.uuid4())[:8],
                 embed_model: BaseEmbedding = None,
                 distance_strategy: str = "cosine") -> None:
        try:
            import chromadb
            import chromadb.config

        except ImportError:
            raise ImportError("chromadb package not found, please install it with `pip install chromadb`")

        self._embed_model = embed_model
        self._client_settings = chromadb.config.Settings()
        self._client = chromadb.Client(self._client_settings)

        if distance_strategy not in ["cosine", "ip", "l2"]:
            raise ValueError(f"Similarity {distance_strategy} not supported.")

        self._collection = self._client.get_or_create_collection(
            name=collection_name,
            embedding_function=None,
            metadata={"hnsw:space": distance_strategy}
        )

    def add_documents(self, documents: List[Document]) -> List:
        """Add documents to the ChromaDB collection.

        Args:
            documents (List[Document]): List of ``Document`` objects to add to the collection.
        """

        embeddings = []
        metadatas = []
        ids = []
        chroma_documents = []

        for doc in documents:
            embeddings.append(self._embed_model.get_query_embedding(doc.get_content()))
            metadatas.append(doc.get_metadata() if doc.get_metadata() else None)
            ids.append(doc.doc_id if doc.doc_id else str(uuid.uuid4()))
            chroma_documents.append(doc.get_content())

        self._collection.add(embeddings=embeddings,
                             ids=ids,
                             metadatas=metadatas,
                             documents=chroma_documents)

        return ids

    def query(self, query: str, top_k: int = 4) -> List[VectorStoreQueryResult]:
        """Performs a similarity search for top-k most similar documents.

        Args:
            query (str): Query text.
            top_k (int, optional): Number of top results to return. Defaults to ``4``.
        """

        query_embedding = self._embed_model.get_query_embedding(query)

        results = self._collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )

        docs_and_scores = [
            VectorStoreQueryResult(document=Document(
                doc_id=result[0],
                text=result[1],
                metadata=result[2]
            ), confidence=result[3])
            for result in zip(
                results["ids"][0],
                results["documents"][0],
                results["metadatas"][0],
                results["distances"][0],
            )
        ]

        return docs_and_scores

    def delete(self, ids: List[str] = None) -> None:
        """Delete documents from the ChromaDB collection.

        Args:
            ids (List[str]): List of ``Document`` IDs to delete. Defaults to ``None``.
        """

        if not ids:
            raise ValueError("No ids provided to delete.")

        self._collection.delete(ids=ids)
