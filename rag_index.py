from sentence_transformers import SentenceTransformer
import numpy as np
import faiss

class VectorIndex:
    def __init__(self, store):
        self.store = store
        self.model = SentenceTransformer("intfloat/multilingual-e5-base")
        dim = store.emb.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(store.emb)

    def search(self, q, topk=10):
        q_emb = self.model.encode([q])
        D,I = self.index.search(q_emb, topk)
        results=[]
        for idx in I[0]:
            results.append({
                "id": self.store.ids[idx],
                "meta": self.store.meta[idx]
            })
        return results
