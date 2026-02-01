from spliit import Spliit

client = Spliit(group_id="zwi1rHAQ-G9PWSHb4Zy7I")

# Get all expenses
expenses = client.get_expenses()

# Or limit the results
recent_5 = client.get_expenses(limit=5)

# Access expense data
for expense in expenses:
    print(f"{expense['title']}: R${expense['amount']/100:.2f}")
    print(f"  Paid by: {expense['paidBy']['name']}")
    print(f"  Category: {expense['category']['grouping']} > {expense['category']['name']}")