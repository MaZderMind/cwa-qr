import random


def construct_seed(seed) -> bytes:
    if seed is None:
        seed = b''

    if type(seed) not in [int, float, str, bytes]:
        seed = str(seed)

    r = random.Random()
    r.seed(seed)
    return bytes([r.randrange(0, 256) for _ in range(0, 16)])
