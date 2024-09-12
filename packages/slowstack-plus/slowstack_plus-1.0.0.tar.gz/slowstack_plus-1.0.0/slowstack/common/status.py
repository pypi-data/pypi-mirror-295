from enum import Enum


class RateLimitStatus(Enum):
    """
    The status of a rate limiter

    Attributes:
        LOCKED:
            The rate limiter is locked and cannot be acquired
        UNLOCKED:
            The rate limiter is ready to be acquired
    """

    LOCKED = "locked"
    UNLOCKED = "unlocked"
