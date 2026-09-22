def split_text(text: str, chunk_size: int, chunk_overlap: int) -> list[str]:
    text = " ".join(text.split())

    if not text:
        return []

    if chunk_overlap >= chunk_size:
        raise ValueError("chunk_overlap must be smaller than chunk_size")

    chunks = []
    start = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - chunk_overlap

    return chunks


def create_chunks(documents: list[dict], chunk_size: int, chunk_overlap: int) -> list[dict]:
    chunks = []

    for document in documents:
        page_text = document["page_content"]
        metadata = document["metadata"]

        for chunk_index, text in enumerate(
            split_text(page_text, chunk_size, chunk_overlap)
        ):
            chunks.append({
                "id": f'{metadata["source"]}_page_{metadata["page"]}_chunk_{chunk_index}',
                "text": text,
                "metadata": {
                    **metadata,
                    "chunk": chunk_index,
                },
            })

    return chunks
