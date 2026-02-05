import json
import re

INPUT = "D:\Desktop\ML\info_pro\ingested_storage\clean_relations.json"
OUTPUT = "filtered_relations.json"


DROP_METADATA = {
    "mimeversion", "charset", "xorigin", "xfilename", "messageid",
    "pst", "sent_mail", "folder", "xfolder", "pdt", "apr"
}

DROP_STOPWORDS = {
    "this","that","these","those","who","which","him","her","they",
    "someone","anyone","what","much","any","date","meeting","thu","tue","sun"
}

DROP_VERBS = {
    "have","contain","send","make","include","hold","need","require",
    "use","say","print","write","receive","provide","get","give"
}

def is_bad_token(t):
    t = t.lower()
    if t in DROP_STOPWORDS:
        return True
    for m in DROP_METADATA:
        if m in t:
            return True
    return False

def is_bad_predicate(p):
    p = p.lower()
    if p in DROP_VERBS:
        return True
    for m in DROP_METADATA:
        if m in p:
            return True
    return False

cleaned = []

with open(INPUT, "r") as f:
    triples = json.load(f)

for r in triples:
    s = r["subject"].strip()
    p = r["predicate"].strip()
    o = r["object"].strip()

    if is_bad_token(s) or is_bad_token(o):
        continue
    if is_bad_predicate(p):
        continue
    if len(s) < 3 or len(o) < 3:
        continue
    if s == o:
        continue

    cleaned.append(r)

with open(OUTPUT, "w") as f:
    json.dump(cleaned, f, indent=4)

print("Before:", len(triples))
print("After:", len(cleaned))
print("Saved:", OUTPUT)
