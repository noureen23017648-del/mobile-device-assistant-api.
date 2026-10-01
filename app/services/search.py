from app.data.devices import DEVICES
from app.utils.bm25_index import bm25_search
from app.utils.embeddings import dense_search


def hybrid_search(query: str, k: int = 3):
    bm25_results = bm25_search(query, k=len(DEVICES))
    dense_results = dense_search(query, k=len(DEVICES))

    rrf_k = 60
    scores = {}

    for rank, (index, _) in enumerate(bm25_results, start=1):
        scores[index] = scores.get(index, 0.0) + (
            1 / (rrf_k + rank)
        )

    for rank, (index, _) in enumerate(dense_results, start=1):
        scores[index] = scores.get(index, 0.0) + (
            1 / (rrf_k + rank)
        )

    ranked_results = sorted(
        scores.items(),
        key=lambda item: item[1],
        reverse=True
    )[:k]

    return [
        (DEVICES[index], float(score))
        for index, score in ranked_results
    ]