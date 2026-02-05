import faiss
import numpy as np
import json
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(BASE_DIR, "output")

EMB_FILE = os.path.join(OUT_DIR, "embeddings.npy")
IDS_FILE = os.path.join(OUT_DIR, "ids.npy")
META_FILE = os.path.join(OUT_DIR, "meta.jsonl")
INDEX_FILE = os.path.join(OUT_DIR, "faiss.index")

def main():
    print("\n📦 Loading embeddings...")
    embs = np.load(EMB_FILE).astype('float32')
    print(f"Embeddings shape: {embs.shape}")

    dim = embs.shape[1]
    print(f"Dimension: {dim}")

    print("\n🔧 Building FAISS index...")
    index = faiss.IndexFlatL2(dim)
    index.add(embs)

    print(f"Indexed vectors: {index.ntotal}")
    faiss.write_index(index, INDEX_FILE)

    print(f"\n💾 Saved FAISS index to: {INDEX_FILE}\n")

if __name__ == "__main__":
    main()
