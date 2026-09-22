from pathlib import Path
from pypdf import PdfReader

def load_pdf(path: Path) -> list[dict]:
    reader = PdfReader(str(path))
    documents = []

    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()

        if text:
            documents.append({
                "page_content": text,
                "metadata": {
                    "page": page_number,
                    "source": path.name,
                },
            })

    return documents

def load_all_pdfs(data_dir: Path) -> list[dict]:
    documents = []

    for pdf_path in sorted(data_dir.glob("*.pdf")):
        documents.extend(load_pdf(pdf_path))

    return documents
