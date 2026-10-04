import pickle
import numpy as np
import faiss
from pathlib import Path

from rag.ingestion.ingest import IngestionPipeline
from rag.embeddings.embedding_model import Embedder

BASE_DIR = Path(__file__).parent
VECTOR_DIR = BASE_DIR / "vectordb"

VECTOR_DIR.mkdir(exist_ok=True)


def build_index():
    print("Loading and chunking PDFs...")

    ingestion = IngestionPipeline()
    chunks = ingestion.run()

    print(f"Generated {len(chunks)} chunks")

    embedder = Embedder()

    texts = [chunk["text"] for chunk in chunks]

    print("Creating embeddings...")
    embeddings = embedder.encode(texts)

    embeddings = np.asarray(embeddings).astype(np.float32)

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(
        index,
        str(VECTOR_DIR / "index.faiss")
    )

    with open(VECTOR_DIR / "chunks.pkl", "wb") as f:
        pickle.dump(chunks, f)

    print("\nIndex successfully created!")
    print(VECTOR_DIR / "index.faiss")
    print(VECTOR_DIR / "chunks.pkl")


if __name__ == "__main__":
    build_index()