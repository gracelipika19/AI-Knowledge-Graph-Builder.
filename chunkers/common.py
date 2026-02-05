# import os
# import re

# DATA_PATH = r"D:\Desktop\ML\info_pro"  # CHANGE IF NEEDED
# STORAGE = os.path.join(DATA_PATH, "ingested_storage")
# OUTPUT = os.path.join(DATA_PATH, "output")

# CHUNK_SIZE = 800  # confirmed choice

# os.makedirs(OUTPUT, exist_ok=True)


# def sentence_split(text):
#     text = text.replace("\n", " ")
#     parts = re.split(r'(?<=[.!?]) +', text)
#     return [p.strip() for p in parts if len(p.strip()) > 0]


# def chunk_text(text, max_len=CHUNK_SIZE):
#     sentences = sentence_split(text)
#     buf = ""
#     for s in sentences:
#         if len(buf) + len(s) <= max_len:
#             buf += s + " "
#         else:
#             yield buf.strip()
#             buf = s + " "
#     if buf:
#         yield buf.strip()
import re

MAX_CHUNK = 800   # from your choice earlier

def normalize(text: str):
    if not isinstance(text, str):
        return ""
    text = text.strip().replace("\n", " ")
    text = re.sub(r"\s+", " ", text)
    return text

def split_sentences(text: str):
    # simple fast split, avoids spacy
    return re.split(r"(?<=[.!?])\s+", text)
