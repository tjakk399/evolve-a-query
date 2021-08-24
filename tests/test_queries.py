import pytest

from queries import Queries, RecombinationMode
from query import Query

from decorators import repeater

"""
Note:

Unit tests on functions involving random.* are repeated several times
to ensure that test is deterministic.
"""

def new_queries():
    return Queries(
            queries = [
                Query(
                    musts = [
                        "must11",
                        "must12",
                        ],
                    must_nots = [
                        "must_not11",
                        "must_not12",
                        ],
                    fitness = 1.1,
                    ),
                Query(
                    musts = [
                        "must21",
                        "must22",
                        ],
                    must_nots = [
                        "must_not21",
                        "must_not22",
                        ],
                    fitness = 2.4,
                    ),
                Query(
                    musts = [
                        "must31",
                        "must32",
                        ],
                    must_nots = [
                        "must_not31",
                        "must_not32",
                        ],
                    fitness = 3.7,
                    ),
                ],
            words = [
                "word1",
                "word2",
                "word3",
                "word4",
                "word5",
                ]
            )

def test_average_score():
    queries = new_queries()

    assert queries.average_score() == 2.4

def test_recombine_clone():
    queries = new_queries()

    size_original = len(queries.queries)

    queries.recombine(
            mode = RecombinationMode.CLONE
            )

    assert len(queries.queries) == size_original * 2

    assert len(
            set(
                [
                    repr(query)
                    for query in queries.queries
                    ]
                )
            ) == size_original

@repeater(5)
def test_mutate():
    queries = new_queries()

    size_original = len(queries.queries)

    queries.mutate()

    assert len(queries.queries) == size_original

def test_sorted_queries():
    queries = new_queries()

    sorted_queries = queries.sorted_queries()

    assert sorted_queries[0] == queries.queries[2]
    assert sorted_queries[1] == queries.queries[1]
    assert sorted_queries[2] == queries.queries[0]

def test_select():
    queries = new_queries()

    sorted_queries = queries.sorted_queries()

    queries.select()

    assert len(queries.sorted_queries()) == 2

    assert queries.sorted_queries()[0].body \
            == sorted_queries[0].body

    assert queries.sorted_queries()[1].body \
            == sorted_queries[1].body

def test__without_lowest():
    assert Queries._without_lowest(
            [
                {
                    'field1': True,
                    'field2': 0.1,
                    },
                {
                    'field1': True,
                    'field2': 1.2,
                    },
                {
                    'field1': True,
                    'field2': 0.1,
                    },
                {
                    'field1': True,
                    'field2': 2.2,
                    },
                ],
            key = lambda x: x['field2'],
            ) == [
                    {
                        'field1': True,
                        'field2': 1.2,
                        },
                    {
                        'field1': True,
                        'field2': 2.2,
                        },
                    ]

def test__without_lowest_from_equally_valued_elements():
    assert Queries._without_lowest(
            [
                {
                    'field1': True,
                    'field2': 0.1,
                    },
                {
                    'field1': True,
                    'field2': 0.1,
                    },
                {
                    'field1': True,
                    'field2': 0.1,
                    },
                {
                    'field1': True,
                    'field2': 0.1,
                    },
                ],
            key = lambda x: x['field2'],
            ) == []

@repeater(5)
def test_random_purge():
    queries = new_queries()

    size_original = len(queries.queries)

    with pytest.raises(ValueError):
        queries.random_purge(
                k = len(queries.queries) + 1
                )

    k = len(queries.queries) - 1

    queries.random_purge(
            k = k
            )

    assert len(queries.queries) == size_original - k

def test_remove_duplicates():
    queries = new_queries()

    queries.queries.append(queries.queries[0])
    queries.queries.append(queries.queries[2])

    queries.remove_duplicates()

    assert len(queries.queries) == 3
    assert len(
            set(
                [
                    repr(query) for query in queries.queries
                    ]
                )
            ) == len(queries.queries)

