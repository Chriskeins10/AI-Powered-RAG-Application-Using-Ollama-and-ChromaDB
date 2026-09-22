# RAG-Based Document Q&A System

RAG application for answering questions from company PDF documents.

## Stack

- Python
- Ollama local LLM
- Ollama embeddings
- ChromaDB
- PyPDF
- python-dotenv

## Project structure

```text
rag_openai_chromadb/
├── data/
│   └── put_company_pdfs_here.pdf
├── chroma_db/
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
├── config.py
├── pdf_loader.py
├── chunker.py
├── vector_store.py
├── ingest.py
├── rag.py
├── chat.py
└── conversation_history.json
```

## Setup

### 1. Create virtual environment

Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Ollama

Install Ollama, start it, and pull the models used by the application:

```bash
ollama pull llama3.2
ollama pull nomic-embed-text
```

Copy `.env.example` to `.env` if you want to customize the Ollama host or model names.

### 4. Add PDFs

Put company PDF files inside:

```text
data/
```

### 5. Ingest documents

```bash
python ingest.py
```

This extracts PDF text, creates chunks, generates Ollama embeddings, and stores them in ChromaDB.

### 6. Start Q&A

```bash
python chat.py
```

Example:

```text
You: What is the leave policy?

Assistant: ...

Sources:
- employee_handbook.pdf (page 12)
```

## RAG flow

```text
PDF
 ↓
Extract text
 ↓
Clean text
 ↓
Chunk text
 ↓
Ollama Embedding
 ↓
ChromaDB
 ↓
User question
 ↓
Ollama Embedding
 ↓
Similarity search
 ↓
Top-K chunks
 ↓
Ollama LLM
 ↓
Answer + source
```

## Requirements covered

1. PDF extraction
2. Preprocessing
3. Chunking
4. Embeddings
5. Vector database
6. Relevant chunk retrieval
7. LLM context
8. Answer generation
9. Out-of-document handling
10. Source/page references
11. Conversation history
12. Error handling
