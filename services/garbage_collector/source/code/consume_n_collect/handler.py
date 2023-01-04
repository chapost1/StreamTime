from shared.models.garbage.garbage import Garbage
from shared.models.bag.bagger import Bagger
from shared.models.bag.bag import GarbageBag

async def handle(garbage: Garbage) -> None:
    """Collects garbage."""

    garbage_bag: GarbageBag = Bagger.bag(garbage=garbage)

    await garbage_bag.collect()
