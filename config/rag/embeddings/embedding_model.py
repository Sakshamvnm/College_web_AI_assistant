from sentence_transformers import SentenceTransformer
import numpy as np


class Embedder:

    def __init__(self):
        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

    def encode(self, texts, batch_size=8):

        all_embeddings = []

        total = len(texts)

        for start in range(0, total, batch_size):

            end = min(start + batch_size, total)

            batch = texts[start:end]

            print(
                f"Embedding chunks {start + 1}-{end} "
                f"of {total}...",
                flush=True
            )

            embeddings = self.model.encode(
                batch,
                batch_size=batch_size,
                convert_to_numpy=True,
                show_progress_bar=False
            )

            all_embeddings.append(embeddings)

        return np.vstack(all_embeddings)