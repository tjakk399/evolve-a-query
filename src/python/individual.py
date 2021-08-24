from abc import ABC, abstractmethod

class Individual(ABC):
    def __init__(self):
        super().__init__()

        self.fitness = None
        self.n_mutations = 0

    @abstractmethod
    def mutate(self):
        pass

    @abstractmethod
    def recombine(self, other):
        pass

    @abstractmethod
    def update_fitness(self):
        pass

