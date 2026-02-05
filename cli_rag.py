from rag_embed import EmbeddingStore
from rag_index import VectorIndex
from rag_graph import GraphSearch
from rag_hybrid import HybridRAG
from rag_query import RagAnswer
import os

GROQ_KEY = os.getenv("GROQ_API_KEY")

store = EmbeddingStore("output/embeddings.npy","output/ids.npy","output/meta.jsonl")
vec = VectorIndex(store)
graph = GraphSearch()
hybrid = HybridRAG(vec, graph)
rag = RagAnswer(hybrid, api_key=GROQ_KEY)

print("\n=== GRAPH-RAG CLI ===")

while True:
    q = input("\nQ: ")
    if q.lower() in ["exit","quit"]:
        break
    print("\nA:", rag.ask(q))
