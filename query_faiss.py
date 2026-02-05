import faiss
import json
from sentence_transformers import SentenceTransformer
import numpy as np

index = faiss.read_index("faiss_index.bin")

with open("entity_mapping.json", "r") as f:
    entities = json.load(f)

model = SentenceTransformer("all-MiniLM-L6-v2")

def search(query, k=5):
    emb = model.encode([query], convert_to_numpy=True)
    faiss.normalize_L2(emb)

    D, I = index.search(emb, k)

    print(f"\nQuery: {query}")
    for score, idx in zip(D[0], I[0]):
        print(f" → {entities[idx]}   (score={score:.3f})")

search("electricity outage", 5)
search("meeting appointment", 5)
search("payment invoice", 5)
