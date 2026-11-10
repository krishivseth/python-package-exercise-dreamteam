"""A playful password checker with a score to back up its roasts."""

from .scoring import score_password
from .feedback import password_feedback

__all__ = ["score_password", "password_feedback"]
