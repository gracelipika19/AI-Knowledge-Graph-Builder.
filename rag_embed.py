import numpy as np
import json

class EmbeddingStore:
    def __init__(self, emb_path, id_path, meta_path):
        self.emb = np.load(emb_path)
        self.ids = np.load(id_path)
        self.meta = [json.loads(x) for x in open(meta_path, "r", encoding="utf-8")]
