import os
import json
import numpy as np
from tqdm import tqdm
from sentence_transformers import SentenceTransformer

DATA_DIR = "D:/Desktop/ML/info_pro/output"

CHUNK_FILES = [
    "email_chunks.jsonl",
    "csv_chunks.jsonl",
    "excel_chunks.jsonl",
    "relations_sentences.jsonl"
]

EMB_FILE = os.path.join(DATA_DIR, "embeddings.npy")
IDS_FILE = os.path.join(DATA_DIR, "ids.npy")
META_FILE = os.path.join(DATA_DIR, "meta.jsonl")

MODEL_NAME = "BAAI/bge-base-en-v1.5"  # local, no API keys
BATCH = 64

MAX = 5000
PER = MAX // len(CHUNK_FILES)   # → 1250 each


def load_chunks():
    texts, ids, meta = [], [], []
    for fn in CHUNK_FILES:
        path = os.path.join(DATA_DIR, fn)
        count = 0
        with open(path, "r", encoding="utf-8") as f:
            for line in f:
                obj = json.loads(line)
                texts.append(obj["text"])
                ids.append(obj["id"])
                meta.append(obj)
                count += 1
                if count >= PER:
                    break
    return texts, ids, meta


def main():
    print("📦 Loading chunks...")
    texts, ids, meta = load_chunks()
    print(f"Loaded: {len(texts)} chunks")

    print("🔍 Loading embedding model...")
    model = SentenceTransformer(MODEL_NAME, device="cpu")

    print("✳ Embedding...")
    embeddings = model.encode(texts, batch_size=BATCH, show_progress_bar=True)

    print("💾 Saving artifacts...")
    np.save(EMB_FILE, embeddings)
    np.save(IDS_FILE, np.array(ids))

    with open(META_FILE, "w", encoding="utf-8") as f:
        for m in meta:
            f.write(json.dumps(m) + "\n")

    print("🎉 DONE!")
    print(f"Embeddings: {embeddings.shape}")
    print(f"Saved to: {EMB_FILE}, {IDS_FILE}, {META_FILE}")


if __name__ == "__main__":
    main()
