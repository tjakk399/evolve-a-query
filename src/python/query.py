from __future__ import annotations

import logging
import random
import json

from typing import Dict, List, Optional

import copy

from individual import Individual

random.seed(10)

class Query(Individual):
    """Class for managing a query as individual.

    :param musts: List of positive terms,
        defaults to None
    :type musts: List[str], optional

    :param must_nots: List of negative terms,
        defaults to None
    :type must_nots: List[str], optional

    :param fitness: Fitness score,
        defaults to 0.0
    :type fitness: float, optional
    """

    def __init__(
            self,
            musts: List[str]=[],
            must_nots: List[str]=[],
            fitness: float = 0.0,
            ):
        super().__init__()

        # Last index explanation w.r.t. target sentence.
        self._last_explanation = None

        self.fitness = fitness

        # Genotype
        self._musts = musts
        self._must_nots = must_nots

        # Phenotype
        self._update_body()

    def _update_body(self) -> None:
        """Updates query body with current terms.

        :rtype: None
        """
        self.body = {
                'query': {
                    'bool': {
                        'must': [
                            {
                                'match': {
                                    'full_text': term
                                    }
                                } for term in self._musts
                            ],
                        'must_not': [
                            {
                                'match': {
                                    'full_text': term
                                    }
                                } for term in self._must_nots
                            ]
                        }
                    }
                }

    def __str__(self):
        return "[" \
                + ",".join(
                        sorted(
                            [ "+" + term for term in self._musts ] \
                            + [ "-" + term for term in self._must_nots ]
                            )
                        ) \
                + "]"

    def __repr__(self):
        return json.dumps(
                self.body,
                indent = 4
                )

    def size(self) -> int:
        """Returns total number of terms.

        :rtype: int
        """
        return len(self._musts) \
                + len(self._must_nots)

    def update_with_explanation(self, explanation: Dict) -> None:
        """Updates query with explanation from Elasticsearch.

        :param explanation: Result from Elasticsearch explanation call
        :type explanation: Dict

        :rtype: None
        """
        assert('value' in explanation['explanation'])
        self._last_explanation = explanation
        self.fitness = explanation['explanation']['value']

    @staticmethod
    def _random_element(
            terms: List,
            blacklist: Optional[List] = None
            ) -> Any:
        """Returns random element from list.

        :param terms: List
        :type terms: List

        :param blacklist: List of elements to not return,
            defaults to None
        :type blacklist: List, optional

        :rtype: Any

        :raises Exception: if there are elements in ``terms``
        """
        if len(terms) == 0:
            raise Exception()
        else:
            terms_shuffled = copy.copy(terms)
            random.shuffle(terms_shuffled)

            if blacklist is not None:
                for term in terms_shuffled:
                    if term not in blacklist:
                        return term
                return None
            else:
                return terms_shuffled[0]

    def _mutate_terms(self, words: List[str]) -> None:
        random.choice(
                [
                    lambda l: l.append(
                        Query._random_element(
                            terms = words,
                            blacklist = l,
                            )
                        ),
                    lambda l: l.pop(
                        random.randrange(
                            len(l)
                            )
                        )
                        if len(l) > 0
                        else [],
                    ]
                )(
                        random.choice(
                            [
                                self._musts,
                                self._must_nots,
                                ]
                            )
                        )

    def mutate(self, words: List[str]) -> None:
        """Mutates itself.

        :param words: List of words from which to draw new terms
        :type words: List[str]

        :rtype: None
        """
        assert(len(words) > 0)

        self._mutate_terms(words)

        logging.debug("mutated positive terms: " + str(self._musts))
        logging.debug("mutated negative terms: " + str(self._must_nots))

        self._update_body()
        self.n_mutations += 1

    def recombine(self, other_query: Query) -> Query:
        """Recombines genotype with genotype from another query.

        :param other_query: Other :class:`Query` object
        :type other_query: Query

        :return: New offspring query
        :rtype: Query
        """
        # TODO
        pass

    def update_fitness(
            self,
            n_hits: int,
            n_total: int,
            ) -> None:
        """Updates fitness score. If ``n_total`` is 0, updates with 0.0.

        :param n_hits: Number of hits
        :type n_hits: int

        :param n_total: Number of total
        :type n_total: int

        :rtype: None
        """
        assert(n_hits <= n_total)

        if n_total == 0:
            self.fitness = 0.0
        else:
            self.fitness = float(n_hits) / float(n_total)

