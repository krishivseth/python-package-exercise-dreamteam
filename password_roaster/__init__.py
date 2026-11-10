"""A playful password checker with a score to back up its roasts."""

from .scoring import score_password
from .crack_time import crack_time


__all__ = ["score_password", "crack_time"]
