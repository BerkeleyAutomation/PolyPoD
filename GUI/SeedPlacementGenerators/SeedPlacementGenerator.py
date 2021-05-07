import SeedPlacement

class SeedPlacementGenerator:
    def __init__(self, *args, **kwargs):
        super().__init__()

    def generate_seed_placement(self):
        print("This SPG didn't override generate_seed_placement!")
        raise AttributeError

    @classmethod
    def unpack_args(cls, clargs):
        print("This SPG didn't override unpack_args!")
        raise AttributeError

