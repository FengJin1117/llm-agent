# core/rag.py

import os

DOC_PATH = "data/docs.txt"


def load_docs():
    if not os.path.exists(DOC_PATH):
        return []

    with open(DOC_PATH, "r", encoding="utf-8") as f:
        docs = f.readlines()

    return [d.strip() for d in docs if d.strip()]


docs = load_docs()


def simple_retrieval(query):

    results = []

    for doc in docs:
        for word in query:
            if word in doc:
                results.append(doc)
                break

    return results[:2]