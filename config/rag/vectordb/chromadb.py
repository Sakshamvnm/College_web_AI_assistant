from pathlib import Path
import faiss
import numpy as np


BASE_DIR = Path(__file__).parent


class FAISSStore:

    def __init__(self):
        self.index = None
        self.index_path = BASE_DIR / "index.faiss"

    def build(self, embeddings):
        dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(dimension)

        self.index.add(
            embeddings.astype(np.float32)
        )

    def save(self):
        faiss.write_index(
            self.index,
            str(self.index_path)
        )

    def load(self):
        self.index = faiss.read_index(
            str(self.index_path)
        )

    def search(self, embedding, k=3):
        distances, indices = self.index.search(
            embedding.astype(np.float32),
            k
        )

        return distances, indices