# 🧾 Spliit Python Client

An **unofficial** Python client for [Spliit](https://spliit.app) — the free, open-source expense splitting app.

> ⚠️ **Disclaimer**: This is not an official API. It reverse-engineers Spliit's internal tRPC endpoints. Use responsibly and be aware it may break if Spliit updates their backend.

## ✨ Features

- 📊 **Get group details** and participants
- 💰 **List all expenses** with automatic pagination
- ➕ **Add new expenses** with category support
- 🏷️ **43 expense categories** built-in
- 🔄 **No authentication required** — uses group ID only

---

## 📦 Installation

### Using uv (recommended)

```bash
# Add to your project
uv add git+https://github.com/victor-san3/SpliitApi.git

# Or install globally
uv tool install git+https://github.com/victor-san3/SpliitApi.git
```

### From source

```bash
git clone https://github.com/victor-san3/SpliitApi.git
cd SpliitApi
uv sync
```

---

## 🚀 Quick Start

### 1. Get your Group ID

Your group ID is in the URL when you open your Spliit group:
```
https://spliit.app/groups/zwi1rHAQ-G9PWSHb4Zy7I
                         └──────────────────────┘
                              This is your group ID
```

### 2. Basic Usage

```python
from spliit import Spliit, CATEGORIES

# Initialize the client with your group ID
client = Spliit(group_id="your-group-id-here")

# Get group info
group = client.get_group()
print(f"Group: {group['name']}")
print(f"Currency: {group['currency']}")

# List all participants
participants = client.get_participants()
for name, id in participants.items():
    print(f"  - {name}: {id}")

# Get all expenses
expenses = client.get_expenses()
for expense in expenses:
    print(f"{expense['title']}: {expense['amount']/100:.2f}")
```

---

## 📖 API Reference

### `Spliit(group_id, base_url=None)`

Initialize the client.

| Parameter | Type | Description |
|-----------|------|-------------|
| `group_id` | `str` | **Required.** Your Spliit group ID |
| `base_url` | `str` | Optional. API base URL (default: `https://spliit.app/api/trpc`) |

```python
client = Spliit(group_id="zwi1rHAQ-G9PWSHb4Zy7I")
```

---

### `client.get_group()` → `dict`

Fetch group details including name, currency, and participants.

**Returns:**
```python
{
    "id": "zwi1rHAQ-G9PWSHb4Zy7I",
    "name": "Trip to Paris",
    "currency": "€",
    "currencyCode": "EUR",
    "participants": [
        {"id": "abc123", "name": "Alice"},
        {"id": "def456", "name": "Bob"}
    ]
}
```

**Example:**
```python
group = client.get_group()
print(f"Group '{group['name']}' uses {group['currencyCode']}")
```

---

### `client.get_participants()` → `dict[str, str]`

Get a mapping of participant names to their IDs.

**Returns:**
```python
{
    "Alice": "abc123",
    "Bob": "def456"
}
```

**Example:**
```python
participants = client.get_participants()
alice_id = participants["Alice"]
```

---

### `client.get_username_id(name)` → `str | None`

Look up a single participant's ID by name.

| Parameter | Type | Description |
|-----------|------|-------------|
| `name` | `str` | Exact participant name (case-sensitive) |

**Returns:** The participant ID, or `None` if not found.

**Example:**
```python
alice_id = client.get_username_id("Alice")
if alice_id:
    print(f"Alice's ID: {alice_id}")
```

---

### `client.get_expenses(limit=None)` → `list[dict]`

Fetch all expenses from the group with automatic pagination.

| Parameter | Type | Description |
|-----------|------|-------------|
| `limit` | `int` | Optional. Maximum number of expenses to return |

**Returns:** List of expense dictionaries:
```python
{
    "id": "expense123",
    "title": "Dinner at restaurant",
    "amount": 5000,  # In cents (50.00)
    "category": {
        "id": 8,
        "grouping": "Food and Drink",
        "name": "Dining Out"
    },
    "paidBy": {
        "id": "abc123",
        "name": "Alice"
    },
    "paidFor": [
        {"participant": {"id": "abc123", "name": "Alice"}, "shares": 50},
        {"participant": {"id": "def456", "name": "Bob"}, "shares": 50}
    ],
    "expenseDate": "2024-01-15T00:00:00.000Z",
    "createdAt": "2024-01-15T18:30:00.000Z",
    "splitMode": "EVENLY",
    "isReimbursement": false
}
```

**Examples:**
```python
# Get all expenses
all_expenses = client.get_expenses()

# Get only the 10 most recent
recent = client.get_expenses(limit=10)

# Calculate total spent
total = sum(e['amount'] for e in all_expenses) / 100
print(f"Total: ${total:.2f}")
```

---

### `client.add_expense(...)` → `str`

Add a new expense to the group.

| Parameter | Type | Description |
|-----------|------|-------------|
| `title` | `str` | **Required.** Expense description |
| `paid_by` | `str` | **Required.** Participant ID who paid |
| `paid_for` | `list[tuple]` | **Required.** List of `(participant_id, shares)` tuples |
| `amount` | `int` | **Required.** Amount in cents (e.g., 1000 = $10.00) |
| `category` | `int` | Optional. Category ID (default: 0 = General) |

**Returns:** API response string.

**Example — Split evenly:**
```python
from spliit import Spliit, CATEGORIES

client = Spliit(group_id="your-group-id")
participants = client.get_participants()

alice = participants["Alice"]
bob = participants["Bob"]

# Add a $50 dinner, paid by Alice, split evenly
client.add_expense(
    title="Dinner at Italian place",
    paid_by=alice,
    paid_for=[
        (alice, 50),  # 50% share
        (bob, 50),    # 50% share
    ],
    amount=5000,  # $50.00 in cents
    category=CATEGORIES["Food and Drink"]["Dining Out"]
)
```

**Example — Uneven split:**
```python
# Alice paid $100 for groceries
# Alice gets $30 worth, Bob gets $70 worth
client.add_expense(
    title="Weekly groceries",
    paid_by=alice,
    paid_for=[
        (alice, 30),
        (bob, 70),
    ],
    amount=10000,  # $100.00
    category=CATEGORIES["Food and Drink"]["Groceries"]
)
```

**Example — One person only:**
```python
# Alice bought something just for herself
client.add_expense(
    title="Personal item",
    paid_by=alice,
    paid_for=[(alice, 100)],
    amount=2500,  # $25.00
    category=CATEGORIES["Uncategorized"]["General"]
)
```

---

## 🏷️ Categories

All 43 Spliit categories are available via the `CATEGORIES` constant:

```python
from spliit import CATEGORIES
```

### Category Structure

```python
CATEGORIES = {
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
```

### Usage

```python
# Use a specific category
category_id = CATEGORIES["Transportation"]["Gas/Fuel"]  # 31

# Or use the ID directly
client.add_expense(
    title="Gas",
    paid_by=alice,
    paid_for=[(alice, 50), (bob, 50)],
    amount=4500,
    category=31  # Same as CATEGORIES["Transportation"]["Gas/Fuel"]
)
```

---

## 🔧 Advanced Usage

### Custom Base URL

If you're self-hosting Spliit:

```python
client = Spliit(
    group_id="your-group-id",
    base_url="https://your-spliit-instance.com/api/trpc"
)
```

### Expense Analytics

```python
from collections import defaultdict

expenses = client.get_expenses()

# Group by category
by_category = defaultdict(float)
for exp in expenses:
    category = exp['category']['grouping']
    by_category[category] += exp['amount'] / 100

print("Spending by category:")
for cat, total in sorted(by_category.items(), key=lambda x: -x[1]):
    print(f"  {cat}: ${total:.2f}")
```

### Find Who Owes Whom

```python
expenses = client.get_expenses()
participants = client.get_participants()

# Calculate balances
balances = {name: 0.0 for name in participants}

for exp in expenses:
    if exp['isReimbursement']:
        continue
    
    payer = exp['paidBy']['name']
    amount = exp['amount'] / 100
    
    total_shares = sum(p['shares'] for p in exp['paidFor'])
    
    for p in exp['paidFor']:
        name = p['participant']['name']
        share = (p['shares'] / total_shares) * amount
        balances[name] -= share
    
    balances[payer] += amount

print("Balances (positive = owed money, negative = owes money):")
for name, balance in balances.items():
    print(f"  {name}: ${balance:+.2f}")
```

---

## 🛠️ Development

### Setup

```bash
git clone https://github.com/victor-san3/SpliitApi.git
cd SpliitApi
uv sync
```

### Run the example

```bash
uv run python main.py
```

### Run tests

```bash
uv run pytest
```

---

## 🔗 How It Works

This client uses Spliit's internal [tRPC](https://trpc.io/) API endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `groups.get,groups.getDetails` | Fetch group info |
| GET | `groups.expenses.list` | List expenses (paginated) |
| POST | `groups.expenses.create` | Create new expense |

Since Spliit groups are **public by URL design** (for easy sharing), no authentication is required — just the group ID.

---

## ⚠️ Limitations

- **Unofficial API**: May break if Spliit updates their backend
- **No auth**: Anyone with the group ID can read/write expenses
- **Rate limits**: Unknown — be careful with automated scripts
- **Read-only fields**: Can't edit or delete expenses via API

---

## 📄 License

This project is licensed under the AGPL-3.0 License — see the [LICENSE](src/spliit/LICENSE) file.

---

## 🙏 Credits

- [Spliit](https://spliit.app) — The amazing open-source expense splitting app
- Original reverse-engineering by [guysoft](https://github.com/guysoft/SpliitApi)

---

<p align="center">
  Made with ❤️ for splitting expenses fairly
</p>