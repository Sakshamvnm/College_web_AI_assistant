from pathlib import Path
import faiss
import numpy as np


BASE_DIR = Path(__file__).parent


class FAISSStore:

    def __init__(self):
        self.index = None
        self.index_path = BASE_DIR / "index.faiss"

    def load(self):
        """
        Load the FAISS index from disk.
        """
        if not self.index_path.exists():
            raise FileNotFoundError(
                f"FAISS index not found: {self.index_path}"
            )

        self.index = faiss.read_index(str(self.index_path))

    def search(self, query_embedding, k=3):
        """
        Search the FAISS index.

        Returns:
            distances, indices
        """
        if self.index is None:
            raise ValueError("FAISS index has not been loaded.")

        query_embedding = np.asarray(
            query_embedding,
            dtype=np.float32
        )

        distances, indices = self.index.search(
            query_embedding,
            k
        )

        return distances, indices