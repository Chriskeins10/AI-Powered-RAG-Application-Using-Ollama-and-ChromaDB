import chromadb
from ollama import Client

from config import CHROMA_DIR, COLLECTION_NAME, EMBEDDING_MODEL

class VectorStore:
    def __init__(self, ollama_client: Client):
        self.ollama_client = ollama_client

        self.chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))
        self.collection = self.chroma.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        response = self.ollama_client.embed(
            model=EMBEDDING_MODEL,
            input=texts,
        )
        return response["embeddings"]

    def add_chunks(self, chunks: list[dict], batch_size: int = 100):
        for start in range(0, len(chunks), batch_size):
            batch = chunks[start:start + batch_size]
            texts = [item["text"] for item in batch]
            embeddings = self.embed_texts(texts)

            self.collection.upsert(
                ids=[item["id"] for item in batch],
                documents=texts,
                embeddings=embeddings,
                metadatas=[item["metadata"] for item in batch],
            )

    def search(self, query: str, top_k: int):
        query_embedding = self.embed_texts([query])[0]

        return self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents", "metadatas", "distances"],
        )
