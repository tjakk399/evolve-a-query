import pytest

import random

random.seed(10)

from query import Query

from decorators import repeater

def new_query():
    return Query(
            musts = [
                "must1",
                "must2",
                ],
            must_nots = [
                "must_not1",
                "must_not2",
                ],
            )

def new_query_halfempty():
    return Query(
            musts = [
                "must1",
                "must2",
                ],
            )

@repeater(5)
def test_mutate():
    query = new_query()

    query._mutate_terms(
            words = [
                "foo",
                "bar",
                "biz",
                ]
            )

    # Are all elements strings?
    for l in [
            query._musts,
            query._must_nots
            ]:
        assert set(
                [
                    type(e)
                    for e in l + [""]
                    ]
                ) == { type("") }

    query = new_query_halfempty()

    query._mutate_terms(
            words = [
                "foo",
                "bar",
                "biz",
                ]
            )

    for l in [
            query._musts,
            query._must_nots
            ]:
        assert set(
                [
                    type(e)
                    for e in l + [""]
                    ]
                ) == { type("") }

@repeater(5)
def test_random_element():
    assert Query._random_element(
            terms = [1, 2, 3, 4, 5],
            blacklist = [1, 2, 3, 5],
            ) == 4

def test_update_fitness():
    query = new_query()

    query.update_fitness(
            n_hits = 5,
            n_total = 10
            )

    assert query.fitness == 0.5

    query.update_fitness(
            n_hits = 0,
            n_total = 10
            )

    assert query.fitness == 0.0

def test_recombine():
    # TODO
    pass

