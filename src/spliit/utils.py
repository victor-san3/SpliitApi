#!/usr/bin/env python3
"""Utility functions and constants for the Spliit client."""

import json
from datetime import datetime, UTC
from typing import Dict, List, Tuple, Any

# Category ID mappings for Spliit expenses
CATEGORIES: Dict[str, Dict[str, int]] = {
    "Uncategorized": {
        "General": 0,
        "Payment": 1
    },
    "Entertainment": {
        "Entertainment": 2,
        "Games": 3,
        "Movies": 4,
        "Music": 5,
        "Sports": 6
    },
    "Food and Drink": {
        "Food and Drink": 7,
        "Dining Out": 8,
        "Groceries": 9,
        "Liquor": 10
    },
    "Home": {
        "Home": 11,
        "Electronics": 12,
        "Furniture": 13,
        "Household Supplies": 14,
        "Maintenance": 15,
        "Mortgage": 16,
        "Pets": 17,
        "Rent": 18,
        "Services": 19
    },
    "Life": {
        "Childcare": 20,
        "Clothing": 21,
        "Education": 22,
        "Gifts": 23,
        "Insurance": 24,
        "Medical Expenses": 25,
        "Taxes": 26
    },
    "Transportation": {
        "Transportation": 27,
        "Bicycle": 28,
        "Bus/Train": 29,
        "Car": 30,
        "Gas/Fuel": 31,
        "Hotel": 32,
        "Parking": 33,
        "Plane": 34,
        "Taxi": 35
    },
    "Utilities": {
        "Utilities": 36,
        "Cleaning": 37,
        "Electricity": 38,
        "Heat/Gas": 39,
        "Trash": 40,
        "TV/Phone/Internet": 41,
        "Water": 42
    }
}


def get_current_timestamp() -> str:
    """Get current UTC timestamp in ISO format with milliseconds.
    
    Returns:
        Timestamp string in format '2024-11-14T22:26:58.244Z'
    """
    now = datetime.now(UTC)
    return now.strftime('%Y-%m-%dT%H:%M:%S.') + f"{now.microsecond // 1000:03d}Z"


def format_expense_payload(
    group_id: str,
    title: str,
    paid_by: str,
    paid_for: List[Tuple[str, int]],
    amount: int,
    category: int
) -> Dict[str, Any]:
    """Format the expense payload for the Spliit API.
    
    Args:
        group_id: The ID of the group
        title: Title/description of the expense
        paid_by: Participant ID who paid
        paid_for: List of tuples (participant_id, shares)
        amount: Total amount in cents
        category: Category ID from CATEGORIES
        
    Returns:
        Formatted payload dictionary for the API request
    """
    paid_for_format = [
        {"participant": participant_id, "shares": shares}
        for participant_id, shares in paid_for
    ]
    
    return {
        "0": {
            "json": {
                "groupId": group_id,
                "expenseFormValues": {
                    "expenseDate": get_current_timestamp(),
                    "title": title,
                    "category": category,
                    "amount": amount,
                    "paidBy": paid_by,
                    "paidFor": paid_for_format,
                    "splitMode": "EVENLY",
                    "saveDefaultSplittingOptions": False,
                    "isReimbursement": False,
                    "documents": [],
                    "notes": "",
                },
                "participantId": "None",
            },
            "meta": {
                "values": {
                    "expenseFormValues.expenseDate": ["Date"],
                },
            },
        },
    }
