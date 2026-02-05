# ============================
# RAG CONFIGURATION
# ============================

NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "graph123"
NEO4J_DB = "graphrag"

# Entity normalization rules
NORMALIZE_ENTITIES = True

# Max hops for multi-hop answers
MAX_HOPS = 3

# Short-term memory window
MEMORY_SPAN = 1   # For M1
