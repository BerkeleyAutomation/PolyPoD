from abc import ABC, abstractmethod
import SeedPlacement

class SeedPlacementGenerator(ABC, SeedPlacement):
    def __init__(self, *args, **kwargs):
        super().__init__()

    @abstractmethod
    def generate_seed_placement(self, *args, **kwargs):
        pass

