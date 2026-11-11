"""A playful password checker with a score to back up its roasts."""

from .scoring import score_password
from .crack_time import crack_time
from .roasting import roast_password
from .generator import generate_password
from .comparison import compare_passwords

__all__ = ["score_password", "crack_time", "roast_password", "generate_password", "compare_passwords"]
