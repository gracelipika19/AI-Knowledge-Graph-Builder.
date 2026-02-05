# rag_hybrid.py

class HybridRAG:
    def __init__(self, vec, graph):
        self.vec = vec
        self.graph = graph

    def query(self, q, topk=8):
        # Vector retrieval
        v_hits = self.vec.search(q, topk=topk)

        # Graph retrieval
        graph_hits = []
        for h in v_hits[:3]:
            # naive entity extraction (first token)
            ent = h["meta"]["text"].split()[0]
            nbrs = self.graph.neighbors(ent, limit=6)
            graph_hits.extend(nbrs)

        return {
            "vector": v_hits,
            "graph": graph_hits
        }
