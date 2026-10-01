from rank_bm25 import BM25Okapi

from app.data.devices import DEVICES


def tokenize(text: str) -> list[str]:
    return text.lower().split()


TOKENIZED_DOCUMENTS = [
    tokenize(document)
    for document in DEVICES
]

BM25 = BM25Okapi(TOKENIZED_DOCUMENTS)


def bm25_search(query: str, k: int = 3):
    query_tokens = tokenize(query)

    scores = BM25.get_scores(query_tokens)

    ranked_indices = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True
    )[:k]

    return [
        (index, float(scores[index]))
        for index in ranked_indices
    ]