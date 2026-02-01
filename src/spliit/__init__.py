"""Spliit API client for managing shared expenses.

This package provides a Python client for interacting with the Spliit
expense splitting application (https://spliit.app).

Example:
    >>> from spliit import Spliit, CATEGORIES
    >>> client = Spliit(group_id="your-group-id")
    >>> participants = client.get_participants()
    >>> client.add_expense(
    ...     title="Dinner",
    ...     paid_by=participants["John"],
    ...     paid_for=[(participants["John"], 50), (participants["Jane"], 50)],
    ...     amount=5000,
    ...     category=CATEGORIES["Food and Drink"]["Dining Out"]
    ... )
"""

from .client import Spliit
from .utils import CATEGORIES, get_current_timestamp

__all__ = ["Spliit", "CATEGORIES", "get_current_timestamp"]
__version__ = "0.1.0"
