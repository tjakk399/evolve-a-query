from __future__ import annotations

from typing import Dict, List, Optional, Callable, Any
from enum import Enum, auto

import copy
import logging
import random

from population import Population
from individual import Individual
from query import Query

from decorators import sorter


class AutoNameEnum(Enum):
    def _generate_next_value_(name, start, count, last_values):
        return name


class RecombinationMode(AutoNameEnum):
    CLONE = auto()


class Queries(Population):
    def __init__(self,
            words: list[str],
            queries: List[Query] = [],
            ):
        super().__init__(queries)

        # Just a different view with better name
        self.queries = self._individuals

        self._words = words

    def size(self):
        return len(self.queries)

    @sorter(key=lambda x: x.fitness, reverse=True)
    def sorted_queries(self) -> List[Query]:
        return self.queries

    def average_score(self):
        if len(self.queries) == 0:
            return 0.0
        else:
            return sum(
                    [
                        query.fitness
                        for query in self.queries
                        ]
                    ) / len(self.queries)

    def recombine(self, mode: RecombinationMode=RecombinationMode.CLONE) -> None:
        """
        Recombine individuals and add their offspring to the population.
        """

        if mode == RecombinationMode.CLONE:
            self.queries.extend(
                    [
                        copy.deepcopy(query)
                        for query in self.queries
                        ]
                    )
        else:
            logging.ERROR("Recombination mode {mode} not implemented.")
            exit(1)

    @staticmethod
    def _without_lowest(
            l: List,
            key: Callable[[Any], float] = lambda x: x,
            ) -> List:
        """
        Return sublist without lowest elements,
        as defined per key callable.

        Note that in a list of equally valued elements,
        all elements are lowest per definition,
        so this would return an empty list.
        """
        l_sorted = sorted(
                l,
                key = key,
                )
        return [
                e
                for e in l
                if key(e) > key(l_sorted[0])
                ]

    def mutate(self):
        new_queries = []

        for query in self.queries:
            query.mutate(self._words)
            if query.size() > 0:
                new_queries.append(query)

        self.queries = new_queries

    def select(self):
        self.queries = Queries._without_lowest(
                self.queries,
                key = lambda x: x.fitness
                )

    def random_purge(self, k: int=1):
        """Remove k random members."""
        logging.debug("Removing random members from population")

        # assert k <= self.size()

        random_indices = random.sample(
                list(
                    range(
                        0,
                        len(self.queries)
                        )
                    ),
                k
                )

        try:
            self.queries = [
                    query
                    for index, query in enumerate(self.queries)
                    if index not in random_indices
                    ]

        except ValueError as e:
            logging.ERROR(str(e))
            raise e

    def remove_duplicates(self):
        new_queries = []
        seen_queries = {}

        for query in self.queries:
            if repr(query) not in seen_queries:
                new_queries.append(query)
                seen_queries[repr(query)] = True

        self.queries = new_queries

