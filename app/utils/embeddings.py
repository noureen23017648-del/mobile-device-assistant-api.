from sentence_transformers import SentenceTransformer

from app.data.devices import DEVICES


MODEL_NAME = "BAAI/bge-small-en-v1.5"

model = SentenceTransformer(MODEL_NAME)


DOCUMENT_EMBEDDINGS = model.encode(
    DEVICES,
    normalize_embeddings=True
)


def dense_search(query: str, k: int = 3):
    query_embedding = model.encode(
        query,
        normalize_embeddings=True
    )

    scores = DOCUMENT_EMBEDDINGS @ query_embedding

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: float(scores[i]),
        reverse=True
    )[:k]

    return [
        (index, float(scores[index]))
        for index in ranked_indices
    ]