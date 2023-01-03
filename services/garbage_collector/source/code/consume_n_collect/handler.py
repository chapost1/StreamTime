from shared.models.garbage.garbage import Garbage
from shared.models.bag.bagger import Bagger
from shared.models.bag.bag import GarbageBag

def handle(garbage: Garbage) -> None:
    """Collects garbage."""

    garbage_bag: GarbageBag = Bagger.bag(garbage=garbage)

    garbage_bag.collect()
