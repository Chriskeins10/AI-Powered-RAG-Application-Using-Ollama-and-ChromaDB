from ollama import Client

from config import DATA_DIR, CHUNK_SIZE, CHUNK_OVERLAP, OLLAMA_HOST
from pdf_loader import load_all_pdfs
from chunker import create_chunks
from vector_store import VectorStore

def main():
    client = Client(host=OLLAMA_HOST)
    documents = load_all_pdfs(DATA_DIR)

    if not documents:
        raise FileNotFoundError(
            f"No PDF files found in: {DATA_DIR}"
        )

    chunks = create_chunks(
        documents,
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    store = VectorStore(client)
    store.add_chunks(chunks)

    print(f"Loaded pages : {len(documents)}")
    print(f"Created chunks: {len(chunks)}")
    print(f"Collection   : {store.collection.name}")
    print("Ingestion completed successfully.")

if __name__ == "__main__":
    main()
