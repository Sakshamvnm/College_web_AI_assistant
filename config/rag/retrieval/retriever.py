import pickle
from pathlib import Path

from ..vectordb.search import FAISSStore
from ..embeddings.embedding_model import Embedder


BASE_DIR = Path(__file__).resolve().parent.parent


class Retriever:

    def __init__(self):

        self.embedder = Embedder()

        self.db = FAISSStore()
        self.db.load()

        chunks_path = BASE_DIR / "vectordb" / "chunks.pkl"

        with open(chunks_path, "rb") as f:
            self.chunks = pickle.load(f)


    def retrieve(self, query, k=3):

        query_embedding = self.embedder.encode([query])

        distances, indices = self.db.search(
            query_embedding,
            k
        )

        results = []

        for distance, idx in zip(distances[0], indices[0]):

            # Ignore invalid FAISS results
            if idx < 0 or idx >= len(self.chunks):
                continue

            chunk = self.chunks[idx].copy()

            # Keep similarity distance for debugging/source ranking
            chunk["distance"] = float(distance)

            results.append(chunk)

        return results