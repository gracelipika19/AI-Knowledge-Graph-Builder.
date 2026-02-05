# rag_eval.py
import numpy as np

def hit_rate(result, gold):
    hits = sum([1 for r in result if gold.lower() in r["meta"]["text"].lower()])
    return hits / len(result) if result else 0.0
