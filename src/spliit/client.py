"""Spliit API client for managing shared expenses."""

import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import requests

from .utils import format_expense_payload


@dataclass
class Spliit:
    """Client for interacting with the Spliit API.
    
    Attributes:
        group_id: The ID of the Spliit group to interact with
        base_url: Base URL for the Spliit API (default: https://spliit.app/api/trpc)
    """
    
    group_id: str
    base_url: str = "https://spliit.app/api/trpc"
    
    def get_group(self) -> Dict:
        """Get group details including participants.
        
        Returns:
            Dictionary containing group information
        """
        params_input = {
            "0": {"json": {"groupId": self.group_id}},
            "1": {"json": {"groupId": self.group_id}}
        }
        
        params = {
            "batch": "1",
            "input": json.dumps(params_input)
        }
        
        response = requests.get(
            f"{self.base_url}/groups.get,groups.getDetails",
            params=params
        )
        response.raise_for_status()
        return response.json()[0]["result"]["data"]["json"]["group"]
    
    def get_username_id(self, name: str) -> Optional[str]:
        """Get participant ID by their display name.
        
        Args:
            name: The display name of the participant
            
        Returns:
            The participant ID if found, None otherwise
        """
        group = self.get_group()
        for participant in group["participants"]:
            if name == participant["name"]:
                return participant["id"]
        return None
    
    def get_participants(self) -> Dict[str, str]:
        """Get all participants with their IDs.
        
        Returns:
            Dictionary mapping participant names to their IDs
        """
        group = self.get_group()
        return {
            participant["name"]: participant["id"]
            for participant in group["participants"]
        }
    
    def get_expenses(self, limit: Optional[int] = None) -> List[Dict]:
        """Get all expenses from the group.
        
        Args:
            limit: Optional maximum number of expenses to return.
                   If None, fetches all expenses (with pagination).
        
        Returns:
            List of expense dictionaries containing:
                - id: Expense ID
                - title: Expense title
                - amount: Amount in cents
                - category: Category info (id, grouping, name)
                - paidBy: Participant who paid (id, name)
                - paidFor: List of participants sharing the expense
                - expenseDate: Date of the expense
                - createdAt: When the expense was created
                - splitMode: How the expense is split
                - isReimbursement: Whether this is a reimbursement
        """
        all_expenses = []
        cursor = 0
        
        while True:
            params_input = {
                "0": {
                    "json": {
                        "groupId": self.group_id,
                        "cursor": cursor
                    }
                }
            }
            
            params = {
                "batch": "1",
                "input": json.dumps(params_input)
            }
            
            response = requests.get(
                f"{self.base_url}/groups.expenses.list",
                params=params
            )
            response.raise_for_status()
            
            data = response.json()[0]["result"]["data"]["json"]
            expenses = data["expenses"]
            all_expenses.extend(expenses)
            
            # Check if we've hit the limit
            if limit and len(all_expenses) >= limit:
                return all_expenses[:limit]
            
            # Check if there are more pages
            if not data.get("hasMore", False):
                break
            
            cursor = data.get("nextCursor", cursor + 10)
        
        return all_expenses
    
    def add_expense(
        self,
        title: str,
        paid_by: str,
        paid_for: List[Tuple[str, int]],
        amount: int,
        category: int = 0
    ) -> str:
        """Add a new expense to the group.
        
        Args:
            title: Title/description of the expense
            paid_by: Participant ID who paid for the expense
            paid_for: List of tuples (participant_id, shares) for splitting
            amount: Total amount in cents
            category: Category ID from CATEGORIES (default: 0 for General)
            
        Returns:
            Response content from the API
        """
        params = {"batch": "1"}
        
        json_data = format_expense_payload(
            self.group_id,
            title,
            paid_by,
            paid_for,
            amount,
            category
        )
        
        response = requests.post(
            f"{self.base_url}/groups.expenses.create",
            params=params,
            json=json_data
        )
        response.raise_for_status()
        return response.content.decode()