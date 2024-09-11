import random
import string


def randomString(N) -> str:
    return str(
        "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(N))
    )
