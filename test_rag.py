from rag_embed import EmbeddingStore
from rag_index import VectorIndex
from rag_graph2 import GraphSearch
from rag_hybrid import HybridRAG
from rag_query import RagAnswer

store = EmbeddingStore("output/embeddings.npy","output/ids.npy","output/meta.jsonl")
vec = VectorIndex(store)
graph = GraphSearch()
hybrid = HybridRAG(vec, graph)
rag = RagAnswer(hybrid)

print(rag.ask("Who founded Intel?"))
