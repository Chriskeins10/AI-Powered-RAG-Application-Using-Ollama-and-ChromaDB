import json
from pathlib import Path

from ollama import Client

from config import OLLAMA_HOST
from rag import RAGEngine

HISTORY_FILE = Path(__file__).resolve().parent / "conversation_history.json"

def load_history():
    if not HISTORY_FILE.exists():
        return []

    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return []

def save_history(history):
    HISTORY_FILE.write_text(
        json.dumps(history, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

def main():
    client = Client(host=OLLAMA_HOST)
    rag = RAGEngine(client)
    history = load_history()

    print("RAG Document Q&A")
    print("Type 'exit' to quit or 'clear' to clear history.")

    while True:
        question = input("\nYou: ").strip()

        if not question:
            continue

        if question.lower() == "exit":
            break

        if question.lower() == "clear":
            history = []
            save_history(history)
            print("Conversation history cleared.")
            continue

        try:
            result = rag.answer(question, history)

            print(f"\nAssistant: {result['answer']}")

            if result["sources"]:
                print("\nSources:")
                seen = set()

                for source in result["sources"]:
                    key = (source["source"], source["page"])
                    if key not in seen:
                        print(f"- {source['source']} (page {source['page']})")
                        seen.add(key)

            history.append({"role": "user", "content": question})
            history.append({"role": "assistant", "content": result["answer"]})
            save_history(history)

        except Exception as exc:
            print(f"Error: {exc}")

if __name__ == "__main__":
    main()
