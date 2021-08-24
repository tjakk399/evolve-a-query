import pytest

import elasticsearch

from index import Index
from vocabulary import Vocabulary
from query import Query

index_name = "test_index"

texts = [
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.",
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.",
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.",
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
        ]

def new_index():
    return Index(index_name)

def test_add():
    index = new_index()

    n_documents = 2

    word_set = set()

    # Add n documents
    for i in range(1, n_documents+1):
        word_set.update(
                set(
                    texts[0].split()
                    )
                )

        result_add = index.add(
                text = texts[0]
                )

        assert result_add['_index'] == index_name
        assert result_add['_shards']['successful'] == 1
        assert result_add['_shards']['failed'] == 0

        assert sorted(index.vocabulary.wordlist()) \
                == sorted(Vocabulary._tokenized(texts[0]))

        result_search = index.es.search(
                index = index_name,
                body = {"query":{"match_all":{}}},
                )

        assert len(result_search['hits']['hits']) == i
        assert result_search['hits']['hits'][0]['_source']['full_text'] == texts[0]

        # Identitical vocabulary after processing?
        assert word_set == set(index.vocabulary.wordlist())

def test_add_bulk():
    index = new_index()

    result = index.add_bulk(texts)

    result_search = index.es.search(
            index = index_name,
            body = {"query":{"match_all":{}}},
            )

    assert len(result_search['hits']['hits']) == len(texts)

    result_texts = [
            hit['_source']['full_text']
            for hit in result_search['hits']['hits']
            ]

    assert len(result_texts) == len(texts)

    for result_text, text in zip(sorted(result_texts), sorted(texts)):
        assert result_text == text

    # Identitical vocabulary after processing?
    assert set(
            [
                word
                for text in texts
                for word in text.split()
                ]
            ) \
            == set(
                    index.vocabulary.wordlist()
                    )

def test_search():
    index = new_index()

    index.es.index(
            index = index_name,
            id = 1,
            refresh = "wait_for",
            body = {
                'full_text': texts[0]
                },
            )

    result = index.search(
            Query(
                musts = [ texts[0].split()[0] ]
                )
            )

    assert len(result['hits']['hits']) == 1


