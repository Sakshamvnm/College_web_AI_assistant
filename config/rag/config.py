from pathlib import Path

# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Folder containing PDFs and downloaded webpages
DATA_DIR = BASE_DIR / "rag" / "data"

# Chroma database location
CHROMA_DB_DIR = BASE_DIR / "chroma_db"

# Embedding model
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

# Chunk settings
CHUNK_SIZE = 800
CHUNK_OVERLAP = 150

# Number of documents retrieved
TOP_K = 3