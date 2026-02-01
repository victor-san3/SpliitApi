import os
from dotenv import load_dotenv
from spliit import Spliit

# Load environment variables from .env file
load_dotenv()

# Initialize client using SPLIIT_GROUP_ID from environment
client = Spliit()

# Get all expenses
expenses = client.get_expenses()

# Or limit the results
recent_5 = client.get_expenses(limit=5)

# Access expense data
for expense in expenses:
    print(f"{expense['title']}: R${expense['amount']/100:.2f}")
    print(f"  Paid by: {expense['paidBy']['name']}")
    print(f"  Category: {expense['category']['grouping']} > {expense['category']['name']}")