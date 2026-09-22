from ollama import Client

from config import LLM_MODEL, TOP_K
from vector_store import VectorStore

SYSTEM_PROMPT = """You are a company-document Q&A assistant.

Answer questions using only the supplied document context.

Rules:
1. Do not invent facts that are not supported by the context.
2. If the answer is not present in the context, say:
   "I couldn't find that information in the provided documents."
3. Keep answers clear and concise.
4. Use the conversation history only to understand follow-up questions.
"""

class RAGEngine:
    def __init__(self, client: Client):
        self.client = client
        self.store = VectorStore(client)

    def retrieve(self, question: str):
        return self.store.search(question, TOP_K)

    def answer(self, question: str, history: list[dict]):
        results = self.retrieve(question)

        documents = results.get("documents", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        distances = results.get("distances", [[]])[0]

        if not documents:
            return {
                "answer": "I couldn't find that information in the provided documents.",
                "sources": [],
            }

        context_parts = []
        sources = []

        for document, metadata, distance in zip(documents, metadatas, distances):
            context_parts.append(
                f'Source: {metadata.get("source")}, '
                f'Page: {metadata.get("page")}\n{document}'
            )
            sources.append({
                "source": metadata.get("source"),
                "page": metadata.get("page"),
                "distance": distance,
            })

        context = "\n\n---\n\n".join(context_parts)

        recent_history = history[-6:]
        history_text = "\n".join(
            f'{item["role"]}: {item["content"]}'
            for item in recent_history
        )

        user_input = f"""Conversation history:
{history_text or "(none)"}

Retrieved document context:
{context}

Current question:
{question}

Answer the current question using only the retrieved context."""

        response = self.client.chat(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
        )

        return {
            "answer": response["message"]["content"],
            "sources": sources,
        }
