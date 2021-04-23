import random
from datetime import datetime
from typing import Union


def constructSeed(seed: Union[str, bytes, int, float, datetime, None]) -> bytes:
    if seed is None:
        seed = b''

    elif isinstance(seed, datetime):
        seed = str(seed)

    r = random.Random()
    r.seed(seed)
    return bytes([r.randrange(0, 256) for _ in range(0, 16)])
