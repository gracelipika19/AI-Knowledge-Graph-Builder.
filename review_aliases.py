import json

INPUT = "output/clusters.json"
ALIAS = "output/alias_map.json"

with open(INPUT, "r", encoding="utf-8") as f:
    clusters = json.load(f)

alias_map = {}

for group in clusters:
    if len(group) == 1:
        alias_map[group[0]] = group[0]
        continue

    print("\n=== AMBIGUOUS CLUSTER ===")
    for i, item in enumerate(group):
        print(f"{i+1}. {item}")
    choice = input("Pick canonical (default=1): ").strip()
    choice = int(choice) if choice.isdigit() else 1
    canonical = group[choice-1]

    for item in group:
        alias_map[item] = canonical

with open(ALIAS, "w", encoding="utf-8") as f:
    json.dump(alias_map, f, indent=4)

print(f"[✓] alias_map saved -> {ALIAS}")
