import json
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
from tqdm import tqdm

# === Config ===
BATCH_SIZE = 256
MIN_CHAR_LENGTH = 10
DEVICE = "cpu"   # change to "cuda" if you later run on GPU

# === Load filtered docs ===
with open("ingested_storage/filtered_documents.json", "r", encoding="utf-8") as f:
    raw_docs = json.load(f)

# === Filter docs (skip very tiny/noisy rows) ===
docs = []
for d in raw_docs:
    text = d["text"].strip()
    if len(text) >= MIN_CHAR_LENGTH:
        docs.append(d)

# === Remove duplicates ===
seen = set()
unique_docs = []
for d in docs:
    txt = d["text"]
    if txt not in seen:
        seen.add(txt)
        unique_docs.append(d)

print(f"Total raw docs: {len(raw_docs)}")
print(f"After filtering short rows: {len(docs)}")
print(f"After deduplication: {len(unique_docs)}")

# === Prepare for embedding ===
texts = [d["text"] for d in unique_docs]
metadata = [{
    "doc_id": d["doc_id"],
    "source_type": d["source_type"],
    "source_name": d["source_name"],
} for d in unique_docs]

# === Load embedding model ===
print("Loading embedding model...")
model = SentenceTransformer("BAAI/bge-small-en", device=DEVICE)

# === Encode in batches ===
print("Encoding embeddings (optimized)...")

all_embeddings = []
for i in tqdm(range(0, len(texts), BATCH_SIZE)):
    batch = texts[i:i+BATCH_SIZE]
    emb = model.encode(batch, convert_to_numpy=True, device=DEVICE)
    all_embeddings.append(emb)

embeddings = np.vstack(all_embeddings)

# === Build FAISS index ===
dimension = embeddings.shape[1]
index = faiss.IndexFlatL2(dimension)
index.add(embeddings)

# === Save artifacts ===
faiss.write_index(index, "vector_index.faiss")
with open("vector_metadata.json", "w", encoding="utf-8") as f:
    json.dump(metadata, f, indent=2)

print("\n=== Embedding pipeline COMPLETE ===")
print(f"Indexed {len(embeddings)} vectors into FAISS")
