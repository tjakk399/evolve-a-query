from __future__ import annotations

import logging

from abc import ABC, abstractmethod
from typing import Dict, List, Optional

class Population(ABC):
    def __init__(self, individuals: List[Individual] = []):
        super().__init__()

        self._individuals = individuals

    def add(self, individual: Individual) -> None:
        """Add individual to population"""
        self._individuals.add(individual)

    def individuals(self) -> Individual:
        """Return individuals as iterable."""
        for individual in self._individuals:
            yield individual

    @abstractmethod
    def recombine(self, mode: int=0) -> None:
        """
        Recombine individuals and add their offspring to the population.
        """
        pass

    @abstractmethod
    def mutate(self) -> None:
        """Apply mutations to population members."""
        pass

    @abstractmethod
    def select(self, n: int=1) -> None:
        """Reduce population to fittest members."""
        pass

    @abstractmethod
    def random_purge(self, n: int=1) -> None:
        """Remove n random members."""
        pass

    @abstractmethod
    def remove_duplicates(self):
        pass


