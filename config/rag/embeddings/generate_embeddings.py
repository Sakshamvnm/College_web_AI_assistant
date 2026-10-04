from .embedding_model import Embedder


embedder = Embedder()

texts = [
    "Welcome to Academia International College.",
    "Admissions are open."
]

embeddings = embedder.encode(texts)

print(embeddings.shape)