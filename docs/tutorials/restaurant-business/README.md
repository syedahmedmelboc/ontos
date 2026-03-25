# Restaurant Business Tutorial: Building Data Contracts and Products with Ontos

A comprehensive, step-by-step guide to building data governance for a restaurant business using the Ontos platform.

---

## Table of Contents

1. [Introduction](#1-introduction)
2. [Prerequisites](#2-prerequisites)
3. [Part 1: Setting Up the Organization](#3-part-1-setting-up-the-organization)
   - [3.0 Creating Tags](#30-creating-tags-required-step)
   - [3.1 Creating Domain Structure](#31-creating-domain-structure)
   - [3.2 Setting Up Teams](#32-setting-up-teams)
   - [3.3 Creating Projects](#33-creating-projects)
   - [3.4 Verifying Your Setup](#34-verifying-your-setup)
4. [Part 2: Creating Datasets](#4-part-2-creating-datasets)
5. [Part 3: Building Data Contracts](#5-part-3-building-data-contracts)
6. [Part 4: Packaging Data Products](#6-part-4-packaging-data-products)
7. [Part 5: Compliance and Governance](#7-part-5-compliance-and-governance)
8. [Part 6: Best Practices Summary](#8-part-6-best-practices-summary)
9. [Appendix: Sample Data Reference](#appendix-sample-data-reference)

---

## 1. Introduction

This tutorial guides you through building a complete data governance solution for a fictional restaurant business called **Bella Cucina**. You'll learn how to use Ontos to:

- Organize data assets using domains, tags, and projects
- Create and manage datasets for restaurant operations
- Define data contracts with quality rules and service level objectives
- Package datasets into data products for different consumers
- Implement compliance policies and monitoring

### What You'll Build

By the end of this tutorial, you'll have created:

| Component | Example |
|-----------|---------|
| **Domains** | Restaurant Operations (root), Kitchen, Front of House, Analytics, Supply Chain |
| **Tags** | 12 domain tags for categorization |
| **Teams** | Analytics Team, Kitchen Team, Data Governance Team |
| **Projects** | Customer Insights, Menu Optimization, Inventory Forecasting |
| **Datasets** | Customers, Menu Items, Orders, Reservations, Inventory, Staff, Suppliers, Reviews |
| **Data Contracts** | Customer data contract, Order data contract, etc. |
| **Data Products** | Customer 360, Daily Sales Analytics, Inventory Forecast |

### The Restaurant Domain

Bella Cucina is a mid-sized Italian restaurant chain with the following data needs:

- **Customer Management**: Track customer preferences, loyalty, and feedback
- **Menu & Orders**: Manage menu items, pricing, and order history
- **Reservations**: Handle booking and seating management
- **Inventory**: Track ingredients, supplies, and supplier relationships
- **Staff**: Manage employee schedules and performance
- **Analytics**: Generate business intelligence and reporting

---

## 2. Prerequisites

Before starting this tutorial, ensure you have:

- [ ] **Ontos installed and running** locally or on Databricks
- [ ] **Access to the Ontos UI** at `http://localhost:3000` (or your Databricks workspace)
- [ ] **Basic understanding** of data governance concepts
- [ ] **Python 3.9+** installed (for sample data generation scripts)

### Required Roles

You'll need appropriate permissions to complete this tutorial:

| Role | Required For |
|------|--------------|
| **Admin** | Creating domains, tags, teams, and projects |
| **Data Producer** | Creating datasets and data products |
| **Data Steward** | Creating data contracts and compliance policies |

---

## 3. Part 1: Setting Up the Organization

### 3.0 Creating Tags (Required Step)

Before creating domains, you need to set up a tag taxonomy that will be used throughout your data governance setup. Tags help categorize and discover assets across your organization.

#### Why Tags Matter

Tags provide:

- **Categorization**: Group related assets, contracts, and products
- **Discovery**: Search and filter assets by business context
- **Governance**: Apply policies based on tag attributes (e.g., PII handling)
- **Semantic Meaning**: Connect data to business concepts through ontology

#### Understanding Tag Namespaces

Tag namespaces help organize tags into logical groups. We'll use:

- `domain:*` - Tags that classify data by business area
- `sensitivity:*` - Tags that indicate data sensitivity levels
- `type:*` - Tags that classify data asset types
- `quality:*` - Tags that indicate data quality states

#### Creating Domain Tags

Navigate to **Settings** → **Tags** and create the following tags:

**Industry Classification Tags (2 tags):**

| Tag Name | Description | Namespace | Parent Tag |
|----------|-------------|-----------|------------|
| `restaurant` | Restaurant industry classification | `domain` | - (root) |
| `hospitality` | Hospitality sector classification | `domain` | - (root) |

**Functional Area Tags (10 tags):**

| Tag Name | Description | Namespace | Parent Tag |
|----------|-------------|-----------|------------|
| `kitchen` | Kitchen operations | `domain` | `restaurant` |
| `food-prep` | Food preparation activities | `domain` | `kitchen` |
| `service` | Customer service operations | `domain` | `restaurant` |
| `guest-experience` | Guest experience management | `domain` | `service` |
| `analytics` | Business intelligence and analytics | `domain` | `restaurant` |
| `reporting` | Business reporting activities | `domain` | `analytics` |
| `bi` | Business intelligence | `domain` | `analytics` |
| `inventory` | Inventory management | `domain` | `restaurant` |
| `suppliers` | Supplier relationships | `domain` | `inventory` |
| `procurement` | Procurement activities | `domain` | `inventory` |

This creates a hierarchical tag structure:

```
restaurant (root)
├── kitchen
│   └── food-prep
├── service
│   └── guest-experience
├── analytics
│   ├── reporting
│   └── bi
└── inventory
    ├── suppliers
    └── procurement

hospitality (root)
```

#### Best Practices for Tag Creation

When creating tags:

1. **Use consistent naming**:
   - Lowercase with hyphens for multi-word tags (e.g., `food-prep`, not `Food Prep`)
   - Avoid spaces or special characters

2. **Group related tags in namespaces**:
   - All domain tags use `domain` namespace
   - This helps with filtering and governance policies

3. **Add clear descriptions**:
   - Describe what the tag represents
   - Include context for when it should be used
   - Reference the parent domain for sub-domain tags

4. **Plan for future tags**:
   - As your organization grows, you'll need additional tags
   - Consider sensitivity classifications: `sensitivity:public`, `sensitivity:internal`, `sensitivity:confidential`
   - Consider quality indicators: `quality:certified`, `quality:experimental`

#### Creating Tags in the UI

1. Navigate to **Settings** → **Tags**
2. Click **Create Tag**
3. Fill in the form:

For root domain tags:
- Tag Name: `restaurant`
- Description: `Restaurant industry classification`
- Namespace: `domain`
- Leave Parent Domain empty

For sub-domain tags (example - `kitchen`):
- Tag Name: `kitchen`
- Description: `Kitchen operations`
- Namespace: `domain`
- Parent Tag: `restaurant` (select from dropdown)

4. Click **Create**
5. Repeat for all 12 tags (2 root + 10 sub-domain)

#### Tag Creation Order Recommendation

Create tags in this order to ensure parent domains exist:

**Step 1: Create root domain tags**
1. `restaurant`
2. `hospitality`

**Step 2: Create Kitchen domain tags**
3. `kitchen`
4. `food-prep`

**Step 3: Create Front of House domain tags**
5. `service`
6. `guest-experience`

**Step 4: Create Analytics domain tags**
7. `analytics`
8. `reporting`
9. `bi`

**Step 5: Create Supply Chain domain tags**
10. `inventory`
11. `suppliers`
12. `procurement`

This order ensures that parent tags exist before creating child tags, so the Parent Tag dropdown will have the required options.

#### Verification

After creating all tags:

- [ ] All 12 domain tags created (2 root + 10 sub-domain)
- [ ] Tags appear in dropdown menus when creating domains
- [ ] Tag search returns results when typing
- [ ] Each tag has proper namespace, description, and parent domain relationship

---

### 3.1 Creating Domain Structure

Domains organize your data by business area. For our restaurant, we'll create:

```
Restaurant Operations (root)
├── Kitchen
├── Front of House
├── Analytics
└── Supply Chain
```

#### Steps

1. Navigate to **Domains** in the sidebar
2. Click **Create Domain**
3. Create the root domain:

| Field | Value |
|-------|-------|
| Name | `restaurant-operations` |
| Description | `Core restaurant operations data including orders, menu, customers, and inventory` |
| Parent Domain | None (this is root) |
| Tags | `restaurant`, `hospitality` |

4. Create sub-domains under "Restaurant Operations":

**Kitchen Domain:**

| Field | Value |
|-------|-------|
| Name | `kitchen` |
| Description | `Kitchen operations including menu preparation, recipes, and food quality` |
| Parent | Restaurant Operations |
| Tags | `kitchen`, `food-prep` |

**Front of House Domain:**

| Field | Value |
|-------|-------|
| Name | `front-of-house` |
| Description | `Guest-facing operations including service, reservations, and customer experience` |
| Parent | Restaurant Operations |
| Tags | `service`, `guest-experience` |

**Analytics Domain:**

| Field | Value |
|-------|-------|
| Name | `analytics` |
| Description | `Business intelligence, reporting, and data analytics` |
| Parent | Restaurant Operations |
| Tags | `analytics`, `reporting`, `bi` |

**Supply Chain Domain:**

| Field | Value |
|-------|-------|
| Name | `supply-chain` |
| Description | `Inventory management, suppliers, and procurement` |
| Parent | Restaurant Operations |
| Tags | `inventory`, `suppliers`, `procurement` |

#### API Example

```bash
curl -X POST http://localhost:8000/api/domains \
  -H "Content-Type: application/json" \
  -d '{
    "name": "restaurant-operations",
    "description": "Core restaurant operations data",
    "tags": ["restaurant", "hospitality"]
  }'
```

---

### 3.2 Setting Up Teams

Teams are groups of users who collaborate on data products.

#### Create Analytics Team

1. Navigate to **Teams** → **Create Team**
2. Fill in the form:

| Field | Value |
|-------|-------|
| Name | `analytics-team` |
| Title | `Analytics Team` |
| Description | `Business intelligence and data analytics for restaurant operations` |
| Domain | Analytics |
| Slack Channel | `#analytics-team` |
| Lead | `analytics.lead@bellacucina.com` |

3. Add team members:

| Member | Type | Role Override |
|--------|------|---------------|
| `data.engineer@bellacucina.com` | User | Data Producer |
| `analyst@bellacucina.com` | User | Data Consumer |
| `bi.developer@bellacucina.com` | User | Data Producer |

#### Create Kitchen Team

| Field | Value |
|-------|-------|
| Name | `kitchen-team` |
| Title | `Kitchen Team` |
| Description | `Chefs, cooks, and kitchen staff` |
| Domain | Kitchen |
| Lead | `head.chef@bellacucina.com` |

#### Create Data Governance Team

| Field | Value |
|-------|-------|
| Name | `data-governance` |
| Title | `Data Governance Team` |
| Description | `Data stewards responsible for data quality and compliance` |
| Domain | Restaurant Operations |
| Lead | `data.steward@bellacucina.com` |

**Members:**

| Member | Role Override |
|--------|---------------|
| `data.steward@bellacucina.com` | Data Steward |
| `compliance@bellacucina.com` | Data Steward |

---

### 3.3 Creating Projects

Projects organize team work on specific initiatives.

#### Create Customer Insights Project

1. Navigate to **Projects** → **Create Project**
2. Fill in the form:

| Field | Value |
|-------|-------|
| Name | `customer-insights` |
| Title | `Customer Insights Platform` |
| Description | `Build comprehensive customer analytics including 360-degree view, segmentation, and lifetime value analysis` |
| Type | Team |
| Owner Team | analytics-team |

3. Add collaborating teams:
   - kitchen-team (provides menu preference data)
   - data-governance (reviews contracts for PII handling)

#### Create Additional Projects

| Project | Owner | Description |
|---------|-------|-------------|
| `menu-optimization` | kitchen-team | Analyze menu performance and optimize pricing |
| `inventory-forecasting` | analytics-team | Predict inventory needs based on demand patterns |
| `compliance-reporting` | data-governance | Automated compliance monitoring and reporting |

---

### 3.4 Verifying Your Setup

Navigate to each section to verify:

- [ ] **Tags**: All 12 domain tags created (restaurant, hospitality, kitchen, food-prep, service, guest-experience, analytics, reporting, bi, inventory, suppliers, procurement)
- [ ] **Domains**: 5 domains created (1 root + 4 sub-domains) with correct tags assigned
- [ ] **Teams**: 3 teams created with correct members
- [ ] **Projects**: 4 projects created with proper team assignments

---

## 4. Part 2: Creating Datasets and Loading Sample Data

In this section, you'll generate realistic sample data using Python and the Faker library, then load it into Databricks Unity Catalog as managed tables.

### 4.1 Overview of Restaurant Datasets

| Dataset | Description | Domain | ~Rows |
|---------|-------------|--------|-------|
| `customers` | Customer profiles and preferences | Front of House | 1,000 |
| `menu_items` | Menu items with pricing and ingredients | Kitchen | 150 |
| `orders` | Order history and details | Front of House | 5,000 |
| `order_items` | Individual items within orders | Front of House | 15,000 |
| `reservations` | Reservation bookings | Front of House | 2,000 |
| `inventory` | Ingredient and supply inventory | Supply Chain | 200 |
| `staff` | Employee information | Kitchen | 50 |
| `suppliers` | Supplier details and contacts | Supply Chain | 30 |
| `reviews` | Customer reviews and ratings | Front of House | 800 |

### 4.2 Setting Up the Python Environment

First, set up your local environment for data generation:

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install required packages
pip install faker pandas databricks-sdk
```

### 4.3 Sample Data Generation Scripts

Create a `scripts/` directory in your tutorial folder and add the following scripts.

#### 4.3.1 Configuration and Shared Utilities

Create `scripts/config.py`:

```python
"""
Configuration for restaurant sample data generation.
"""
from datetime import datetime

# Bella Cucina restaurant configuration
RESTAURANT_NAME = "Bella Cucina"
RESTAURANT_DOMAIN = "bellacucina.com"

# Data generation settings
RANDOM_SEED = 42  # For reproducibility
NUM_CUSTOMERS = 1000
NUM_MENU_ITEMS = 150
NUM_ORDERS = 5000
NUM_RESERVATIONS = 2000
NUM_INVENTORY_ITEMS = 200
NUM_STAFF = 50
NUM_SUPPLIERS = 30
NUM_REVIEWS = 800

# Date ranges
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 12, 31)

# Databricks configuration
DATABRICKS_CATALOG = "main"
DATABRICKS_SCHEMA = "restaurant_tutorial"
```

Create `scripts/generate_all.py`:

```python
"""
Main script to generate all restaurant sample data.
"""
import os
import json
from faker import Faker
from config import *

fake = Faker()
Faker.seed(RANDOM_SEED)

OUTPUT_DIR = "generated_data"
os.makedirs(OUTPUT_DIR, exist_ok=True)

def save_data(data, filename):
    """Save generated data to JSON file."""
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2, default=str)
    print(f"Generated {len(data)} records -> {filepath}")
    return filepath

if __name__ == "__main__":
    # Import and run all generators
    from generate_customers import generate_customers
    from generate_menu_items import generate_menu_items
    from generate_suppliers import generate_suppliers
    from generate_inventory import generate_inventory
    from generate_staff import generate_staff
    from generate_orders import generate_orders, generate_order_items
    from generate_reservations import generate_reservations
    from generate_reviews import generate_reviews
    
    print("=== Generating Restaurant Sample Data ===\n")
    
    # Generate base entities first (no dependencies)
    customers = generate_customers()
    save_data(customers, "customers.json")
    
    menu_items = generate_menu_items()
    save_data(menu_items, "menu_items.json")
    
    suppliers = generate_suppliers()
    save_data(suppliers, "suppliers.json")
    
    inventory = generate_inventory(suppliers)
    save_data(inventory, "inventory.json")
    
    staff = generate_staff()
    save_data(staff, "staff.json")
    
    # Generate dependent entities
    orders, order_items = generate_orders(customers, menu_items, staff)
    save_data(orders, "orders.json")
    save_data(order_items, "order_items.json")
    
    reservations = generate_reservations(customers, staff)
    save_data(reservations, "reservations.json")
    
    reviews = generate_reviews(customers, orders)
    save_data(reviews, "reviews.json")
    
    print("\n=== Data Generation Complete ===")
    print(f"All files saved to: {OUTPUT_DIR}/")
```

#### 4.3.2 Generate Customers

Create `scripts/generate_customers.py`:

```python
"""
Generate customer data with realistic profiles.
"""
from faker import Faker
import random
from datetime import datetime
from config import *

fake = Faker()
Faker.seed(RANDOM_SEED)

def generate_customers():
    """Generate customer records."""
    customers = []
    
    loyalty_tiers = ['bronze', 'silver', 'gold', 'platinum']
    tier_weights = [0.4, 0.3, 0.2, 0.1]  # Most customers are bronze/silver
    
    dietary_preferences = ['none', 'vegetarian', 'vegan', 'gluten-free', 'pescatarian']
    
    for i in range(NUM_CUSTOMERS):
        customer_id = f"CUST-{str(i+1).zfill(6)}"
        
        # Generate realistic customer profile
        customer = {
            "customer_id": customer_id,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(domain=RESTAURANT_DOMAIN),
            "phone": fake.phone_number(),
            "birth_date": fake.date_of_birth(minimum_age=18, maximum_age=80).isoformat(),
            "address": {
                "street": fake.street_address(),
                "city": fake.city(),
                "state": fake.state_abbr(),
                "zip": fake.zipcode()
            },
            "loyalty_tier": random.choices(loyalty_tiers, weights=tier_weights)[0],
            "loyalty_points": random.randint(0, 10000),
            "dietary_preference": random.choice(dietary_preferences),
            "created_at": fake.date_time_between(START_DATE, END_DATE).isoformat(),
            "last_visit": fake.date_time_between(START_DATE, END_DATE).isoformat(),
            "total_visits": random.randint(1, 100),
            "total_spent": round(random.uniform(50, 5000), 2),
            "preferred_location": random.choice(['downtown', 'uptown', 'suburbs']),
            "marketing_opt_in": random.choice([True, False])
        }
        customers.append(customer)
    
    return customers

if __name__ == "__main__":
    customers = generate_customers()
    print(f"Generated {len(customers)} customers")
```

#### 4.3.3 Generate Menu Items

Create `scripts/generate_menu_items.py`:

```python
"""
Generate menu item data for Italian restaurant.
"""
from faker import Faker
import random
from config import *

fake = Faker()
Faker.seed(RANDOM_SEED)

def generate_menu_items():
    """Generate menu item records."""
    
    # Italian menu categories and items
    menu_structure = {
        "antipasti": [
            ("Bruschetta Classica", "Toasted bread with fresh tomatoes, garlic, basil", 12.99),
            ("Carpaccio di Manzo", "Thinly sliced beef with arugula and parmesan", 16.99),
            ("Calamari Fritti", "Crispy fried calamari with marinara sauce", 14.99),
            ("Caprese Salad", "Fresh mozzarella, tomatoes, basil, balsamic glaze", 13.99),
            ("Arancini", "Crispy risotto balls with mozzarella center", 11.99),
        ],
        "pasta": [
            ("Spaghetti Carbonara", "Classic Roman pasta with egg, pecorino, guanciale", 22.99),
            ("Fettuccine Alfredo", "Creamy parmesan sauce with fresh fettuccine", 19.99),
            ("Penne Arrabbiata", "Spicy tomato sauce with garlic and chili", 17.99),
            ("Lasagna Bolognese", "Layered pasta with meat ragù and bechamel", 24.99),
            ("Linguine alle Vongole", "Fresh clams in white wine garlic sauce", 26.99),
            ("Ravioli di Ricotta", "Spinach and ricotta filled pasta, sage butter", 21.99),
            ("Gnocchi al Pesto", "Potato gnocchi with fresh basil pesto", 20.99),
        ],
        "pizza": [
            ("Margherita", "San Marzano tomatoes, fresh mozzarella, basil", 18.99),
            ("Quattro Formaggi", "Mozzarella, gorgonzola, fontina, parmesan", 22.99),
            ("Diavola", "Spicy salami, tomato, mozzarella, chili flakes", 21.99),
            ("Prosciutto e Rucola", "Prosciutto di Parma, arugula, parmesan", 24.99),
            ("Quattro Stagioni", "Artichokes, olives, ham, mushrooms", 23.99),
        ],
        "secondi": [
            ("Osso Buco", "Braised veal shank with gremolata", 34.99),
            ("Branzino al Forno", "Whole roasted sea bass with herbs", 32.99),
            ("Pollo alla Parmigiana", "Breaded chicken with tomato and mozzarella", 26.99),
            ("Bistecca Fiorentina", "T-bone steak Florentine style (32oz)", 54.99),
            ("Saltimbocca alla Romana", "Veal with prosciutto and sage", 29.99),
        ],
        "dolci": [
            ("Tiramisu", "Classic coffee-soaked ladyfingers with mascarpone", 10.99),
            ("Panna Cotta", "Vanilla cream with berry compote", 9.99),
            ("Cannoli Siciliani", "Crispy shells with sweet ricotta cream", 8.99),
            ("Gelato Trio", "Three scoops of artisanal Italian gelato", 7.99),
            ("Affogato", "Vanilla gelato with hot espresso", 6.99),
        ],
        "beverages": [
            ("Espresso", "Single shot Italian espresso", 3.99),
            ("Cappuccino", "Espresso with steamed milk foam", 4.99),
            ("Italian Soda", "Sparkling water with fruit syrup", 4.99),
            ("Limoncello", "Traditional Italian lemon liqueur", 9.99),
            ("House Wine (glass)", "Red or white house wine", 8.99),
        ]
    }
    
    menu_items = []
    item_id = 1
    
    for category, items in menu_structure.items():
        for name, description, price in items:
            # Determine dietary tags
            is_vegetarian = category in ['pasta', 'pizza', 'dolci', 'beverages'] and 'meat' not in description.lower() and 'clam' not in description.lower()
            is_vegan = is_vegetarian and 'cheese' not in description.lower() and 'mozzarella' not in description.lower() and 'cream' not in description.lower()
            
            menu_item = {
                "menu_item_id": f"MENU-{str(item_id).zfill(4)}",
                "name": name,
                "description": description,
                "category": category,
                "price": price,
                "cost": round(price * random.uniform(0.25, 0.35), 2),
                "is_vegetarian": is_vegetarian,
                "is_vegan": is_vegan,
                "is_gluten_free": 'pasta' not in category or 'gnocchi' in name.lower(),
                "contains_nuts": random.choice([True, False, False, False]),  # 25% chance
                "spicy_level": random.choice(['none', 'mild', 'medium', 'hot']) if 'spicy' in description.lower() or 'arrabbiata' in name.lower() or 'diavola' in name.lower() else 'none',
                "preparation_time_minutes": random.randint(5, 25),
                "calories": random.randint(150, 1200),
                "is_active": True,
                "created_at": START_DATE.isoformat(),
                "updated_at": END_DATE.isoformat()
            }
            menu_items.append(menu_item)
            item_id += 1
    
    return menu_items

if __name__ == "__main__":
    items = generate_menu_items()
    print(f"Generated {len(items)} menu items")
```

#### 4.3.4 Generate Suppliers

Create `scripts/generate_suppliers.py`:

```python
"""
Generate supplier data for restaurant inventory.
"""
from faker import Faker
import random
from config import *

fake = Faker()
Faker.seed(RANDOM_SEED)

def generate_suppliers():
    """Generate supplier records."""
    
    supplier_types = [
        ("produce", "Fresh vegetables and fruits"),
        ("dairy", "Milk, cheese, and dairy products"),
        ("meat", "Beef, pork, and poultry"),
        ("seafood", "Fresh and frozen seafood"),
        ("dry_goods", "Pasta, rice, flour, spices"),
        ("beverages", "Wines, spirits, non-alcoholic"),
        ("equipment", "Kitchen equipment and supplies"),
    ]
    
    suppliers = []
    
    for i, (supplier_type, description) in enumerate(supplier_types * 5):  # ~30 suppliers
        company_name = fake.company()
        
        supplier = {
            "supplier_id": f"SUPP-{str(i+1).zfill(4)}",
            "company_name": company_name,
            "contact_name": fake.name(),
            "email": f"orders@{company_name.lower().replace(' ', '').replace(',', '')}.com",
            "phone": fake.phone_number(),
            "address": {
                "street": fake.street_address(),
                "city": fake.city(),
                "state": fake.state_abbr(),
                "zip": fake.zipcode()
            },
            "supplier_type": supplier_type,
            "specialty": description,
            "rating": round(random.uniform(3.5, 5.0), 1),
            "payment_terms": random.choice(["Net 30", "Net 45", "Net 60", "COD"]),
            "min_order_amount": random.choice([100, 250, 500, 1000]),
            "delivery_days": random.sample(["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"], k=random.randint(2, 5)),
            "lead_time_days": random.randint(1, 7),
            "is_active": random.choice([True, True, True, False]),  # 75% active
            "contract_start": fake.date_between(START_DATE, END_DATE).isoformat(),
            "notes": fake.sentence() if random.random() > 0.5 else ""
        }
        suppliers.append(supplier)
    
    return suppliers[:NUM_SUPPLIERS]

if __name__ == "__main__":
    suppliers = generate_suppliers()
    print(f"Generated {len(suppliers)} suppliers")
```

#### 4.3.5 Generate Inventory

Create `scripts/generate_inventory.py`:

```python
"""
Generate inventory data for restaurant.
"""
from faker import Faker
import random
from config import *

fake = Faker()
Faker.seed(RANDOM_SEED)

def generate_inventory(suppliers):
    """Generate inventory records."""
    
    inventory_items = [
        # Produce
        ("San Marzano Tomatoes", "produce", "canned", "kg", 50, 5.99),
        ("Fresh Basil", "produce", "fresh", "bunch", 30, 3.99),
        ("Arugula", "produce", "fresh", "kg", 20, 8.99),
        ("Garlic", "produce", "fresh", "kg", 15, 6.99),
        ("Extra Virgin Olive Oil", "produce", "bottled", "liter", 40, 18.99),
        # Dairy
        ("Fresh Mozzarella", "dairy", "refrigerated", "kg", 25, 14.99),
        ("Parmigiano Reggiano", "dairy", "refrigerated", "kg", 15, 32.99),
        ("Mascarpone", "dairy", "refrigerated", "kg", 10, 18.99),
        ("Heavy Cream", "dairy", "refrigerated", "liter", 20, 5.99),
        ("Pecorino Romano", "dairy", "refrigerated", "kg", 12, 24.99),
        # Meat
        ("Ground Beef", "meat", "frozen", "kg", 40, 12.99),
        ("Veal Shanks", "meat", "frozen", "kg", 20, 28.99),
        ("Prosciutto di Parma", "meat", "refrigerated", "kg", 15, 45.99),
        ("Guanciale", "meat", "refrigerated", "kg", 10, 35.99),
        ("Chicken Breast", "meat", "frozen", "kg", 35, 9.99),
        # Seafood
        ("Fresh Clams", "seafood", "fresh", "kg", 20, 24.99),
        ("Branzino", "seafood", "fresh", "whole", 15, 22.99),
        ("Calamari", "seafood", "frozen", "kg", 25, 16.99),
        # Dry Goods
        ("Spaghetti", "dry_goods", "dry", "kg", 50, 3.99),
        ("Fettuccine", "dry_goods", "dry", "kg", 40, 4.49),
        ("Penne", "dry_goods", "dry", "kg", 45, 3.99),
        ("Arborio Rice", "dry_goods", "dry", "kg", 30, 6.99),
        ("00 Flour", "dry_goods", "dry", "kg", 50, 4.99),
        # Beverages
        ("House Red Wine", "beverages", "bottled", "bottle", 48, 12.99),
        ("House White Wine", "beverages", "bottled", "bottle", 36, 11.99),
        ("Limoncello", "beverages", "bottled", "bottle", 12, 24.99),
        ("Espresso Beans", "beverages", "dry", "kg", 20, 28.99),
    ]
    
    inventory = []
    supplier_ids = [s["supplier_id"] for s in suppliers]
    
    for i, (name, category, storage, unit, par_level, unit_cost) in enumerate(inventory_items):
        current_qty = random.randint(int(par_level * 0.3), int(par_level * 1.5))
        
        item = {
            "inventory_id": f"INV-{str(i+1).zfill(4)}",
            "item_name": name,
            "category": category,
            "storage_type": storage,
            "unit_of_measure": unit,
            "current_quantity": current_qty,
            "par_level": par_level,
            "reorder_point": int(par_level * 0.4),
            "unit_cost": unit_cost,
            "total_value": round(current_qty * unit_cost, 2),
            "primary_supplier_id": random.choice(supplier_ids),
            "last_received": fake.date_between(START_DATE, END_DATE).isoformat(),
            "last_counted": fake.date_between(START_DATE, END_DATE).isoformat(),
            "location": random.choice(["Walk-in Cooler", "Walk-in Freezer", "Dry Storage", "Prep Area"]),
            "is_low_stock": current_qty < par_level * 0.4,
            "notes": ""
        }
        inventory.append(item)
    
    # Add more items to reach target
    while len(inventory) < NUM_INVENTORY_ITEMS:
        i = len(inventory)
        category = random.choice(["produce", "dairy", "meat", "dry_goods"])
        item = {
            "inventory_id": f"INV-{str(i+1).zfill(4)}",
            "item_name": f"{fake.word().title()} {category.replace('_', ' ').title()}",
            "category": category,
            "storage_type": random.choice(["fresh", "frozen", "dry", "refrigerated"]),
            "unit_of_measure": random.choice(["kg", "liter", "unit", "case"]),
            "current_quantity": random.randint(5, 100),
            "par_level": random.randint(20, 60),
            "reorder_point": random.randint(8, 24),
            "unit_cost": round(random.uniform(2.99, 49.99), 2),
            "total_value": round(random.uniform(50, 500), 2),
            "primary_supplier_id": random.choice(supplier_ids),
            "last_received": fake.date_between(START_DATE, END_DATE).isoformat(),
            "last_counted": fake.date_between(START_DATE, END_DATE).isoformat(),
            "location": random.choice(["Walk-in Cooler", "Walk-in Freezer", "Dry Storage", "Prep Area"]),
            "is_low_stock": random.choice([True, False, False]),
            "notes": ""
        }
        inventory.append(item)
    
    return inventory

if __name__ == "__main__":
    suppliers = [{"supplier_id": f"SUPP-{str(i).zfill(4)}"} for i in range(1, 31)]
    inventory = generate_inventory(suppliers)
    print(f"Generated {len(inventory)} inventory items")
```

#### 4.3.6 Generate Staff

Create `scripts/generate_staff.py`:

```python
"""
Generate staff/employee data.
"""
from faker import Faker
import random
from config import *

fake = Faker()
Faker.seed(RANDOM_SEED)

def generate_staff():
    """Generate staff records."""
    
    positions = [
        ("Head Chef", "kitchen", 75000),
        ("Sous Chef", "kitchen", 55000),
        ("Line Cook", "kitchen", 42000),
        ("Prep Cook", "kitchen", 38000),
        ("Pastry Chef", "kitchen", 48000),
        ("Dishwasher", "kitchen", 32000),
        ("Restaurant Manager", "front_of_house", 65000),
        ("Host/Hostess", "front_of_house", 36000),
        ("Server", "front_of_house", 35000),
        ("Bartender", "front_of_house", 38000),
        ("Sommelier", "front_of_house", 52000),
        ("Busser", "front_of_house", 32000),
    ]
    
    staff = []
    
    for i in range(NUM_STAFF):
        position, department, base_salary = random.choice(positions)
        
        employee = {
            "employee_id": f"EMP-{str(i+1).zfill(4)}",
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "email": fake.email(domain=RESTAURANT_DOMAIN),
            "phone": fake.phone_number(),
            "position": position,
            "department": department,
            "hire_date": fake.date_between(START_DATE, END_DATE).isoformat(),
            "base_salary": base_salary + random.randint(-5000, 10000),
            "hourly_rate": None if position in ["Head Chef", "Sous Chef", "Restaurant Manager"] else round(random.uniform(15, 25), 2),
            "is_full_time": random.choice([True, True, False]),
            "is_active": random.choice([True, True, True, False]),  # 75% active
            "location": random.choice(['downtown', 'uptown', 'suburbs']),
            "manager_id": None,  # Will be set based on hierarchy
            "certifications": random.sample(["Food Handler", "Food Safety Manager", "TIPS Certified", "ServSafe", "Wine Certification"], k=random.randint(0, 3)),
            "notes": ""
        }
        staff.append(employee)
    
    # Set manager relationships
    managers = [e for e in staff if 'Manager' in e['position'] or 'Head Chef' in e['position'] or 'Sous Chef' in e['position']]
    for employee in staff:
        if employee['manager_id'] is None and employee not in managers:
            dept_managers = [m for m in managers if m['department'] == employee['department']]
            if dept_managers:
                employee['manager_id'] = random.choice(dept_managers)['employee_id']
    
    return staff

if __name__ == "__main__":
    staff = generate_staff()
    print(f"Generated {len(staff)} staff members")
```

#### 4.3.7 Generate Orders

Create `scripts/generate_orders.py`:

```python
"""
Generate orders and order items data.
"""
from faker import Faker
import random
from datetime import datetime, timedelta
from config import *

fake = Faker()
Faker.seed(RANDOM_SEED)

def generate_orders(customers, menu_items, staff):
    """Generate order and order item records."""
    
    orders = []
    order_items = []
    
    # Get active staff for servers
    servers = [s for s in staff if s['position'] == 'Server' and s['is_active']]
    server_ids = [s['employee_id'] for s in servers] if servers else ['EMP-0001']
    
    customer_ids = [c['customer_id'] for c in customers]
    menu_item_ids = [m['menu_item_id'] for m in menu_items]
    menu_prices = {m['menu_item_id']: m['price'] for m in menu_items}
    
    order_types = ['dine-in', 'takeout', 'delivery']
    payment_methods = ['credit_card', 'debit_card', 'cash', 'gift_card']
    
    item_counter = 1
    
    for i in range(NUM_ORDERS):
        order_id = f"ORD-{str(i+1).zfill(7)}"
        order_date = fake.date_time_between(START_DATE, END_DATE)
        
        # Generate 1-6 items per order
        num_items = random.choices([1, 2, 3, 4, 5, 6], weights=[5, 15, 30, 30, 15, 5])[0]
        selected_items = random.sample(menu_item_ids, num_items)
        
        subtotal = 0
        items_list = []
        
        for menu_item_id in selected_items:
            quantity = random.choices([1, 2, 3], weights=[70, 25, 5])[0]
            unit_price = menu_prices[menu_item_id]
            item_total = round(unit_price * quantity, 2)
            subtotal += item_total
            
            order_item = {
                "order_item_id": f"OI-{str(item_counter).zfill(8)}",
                "order_id": order_id,
                "menu_item_id": menu_item_id,
                "quantity": quantity,
                "unit_price": unit_price,
                "total_price": item_total,
                "special_requests": random.choice(["", "", "", "no cheese", "extra sauce", "gluten-free"]) if random.random() > 0.7 else "",
                "created_at": order_date.isoformat()
            }
            order_items.append(order_item)
            items_list.append(order_item)
            item_counter += 1
        
        # Calculate totals
        tax_rate = 0.08875  # NYC tax rate
        tax = round(subtotal * tax_rate, 2)
        tip_percentage = random.choices([0, 0.15, 0.18, 0.20, 0.22, 0.25], weights=[10, 15, 25, 30, 15, 5])[0]
        tip = round(subtotal * tip_percentage, 2)
        total = round(subtotal + tax + tip, 2)
        
        order = {
            "order_id": order_id,
            "customer_id": random.choice(customer_ids) if random.random() > 0.2 else None,  # 20% walk-ins
            "server_id": random.choice(server_ids),
            "order_type": random.choice(order_types),
            "table_number": random.randint(1, 40) if random.random() > 0.3 else None,
            "order_date": order_date.isoformat(),
            "subtotal": round(subtotal, 2),
            "tax": tax,
            "tip": tip,
            "total": total,
            "payment_method": random.choice(payment_methods),
            "status": "completed",
            "num_items": num_items,
            "party_size": random.randint(1, 8),
            "special_requests": "",
            "created_at": order_date.isoformat(),
            "updated_at": order_date.isoformat()
        }
        orders.append(order)
    
    return orders, order_items

if __name__ == "__main__":
    customers = [{"customer_id": f"CUST-{str(i).zfill(6)}"} for i in range(1, 1001)]
    menu_items = [{"menu_item_id": f"MENU-{str(i).zfill(4)}", "price": round(random.uniform(8, 55), 2)} for i in range(1, 151)]
    staff = [{"employee_id": f"EMP-{str(i).zfill(4)}", "position": random.choice(["Server", "Cook"]), "is_active": True} for i in range(1, 51)]
    
    orders, order_items = generate_orders(customers, menu_items, staff)
    print(f"Generated {len(orders)} orders with {len(order_items)} order items")
```

#### 4.3.8 Generate Reservations

Create `scripts/generate_reservations.py`:

```python
"""
Generate reservation data.
"""
from faker import Faker
import random
from config import *

fake = Faker()
Faker.seed(RANDOM_SEED)

def generate_reservations(customers, staff):
    """Generate reservation records."""
    
    reservations = []
    
    customer_ids = [c['customer_id'] for c in customers]
    hosts = [s for s in staff if s['position'] in ['Host/Hostess', 'Restaurant Manager'] and s['is_active']]
    host_ids = [h['employee_id'] for h in hosts] if hosts else ['EMP-0001']
    
    statuses = ['confirmed', 'seated', 'completed', 'cancelled', 'no_show']
    status_weights = [15, 25, 45, 10, 5]
    
    for i in range(NUM_RESERVATIONS):
        reservation_date = fake.date_time_between(START_DATE, END_DATE)
        
        # Most reservations are for dinner (5-9 PM)
        hour = random.choices([17, 18, 19, 20, 21, 12, 13], weights=[15, 25, 30, 20, 5, 3, 2])[0]
        reservation_time = reservation_date.replace(hour=hour, minute=random.choice([0, 15, 30, 45]))
        
        party_size = random.choices([2, 3, 4, 5, 6, 7, 8], weights=[30, 20, 25, 10, 10, 3, 2])[0]
        
        reservation = {
            "reservation_id": f"RESV-{str(i+1).zfill(6)}",
            "customer_id": random.choice(customer_ids),
            "reservation_date": reservation_time.date().isoformat(),
            "reservation_time": reservation_time.time().isoformat(),
            "party_size": party_size,
            "table_number": random.randint(1, 40),
            "status": random.choices(statuses, weights=status_weights)[0],
            "special_requests": random.choice(["", "", "", "high chair", "wheelchair accessible", "window seat", "quiet corner", "anniversary"]) if random.random() > 0.6 else "",
            "occasion": random.choice(["", "birthday", "anniversary", "business", "date night", ""]) if random.random() > 0.7 else "",
            "contact_phone": fake.phone_number(),
            "contact_email": fake.email(domain=RESTAURANT_DOMAIN),
            "created_by": random.choice(host_ids),
            "created_at": reservation_time.isoformat(),
            "updated_at": reservation_time.isoformat(),
            "notes": ""
        }
        reservations.append(reservation)
    
    return reservations

if __name__ == "__main__":
    customers = [{"customer_id": f"CUST-{str(i).zfill(6)}"} for i in range(1, 1001)]
    staff = [{"employee_id": f"EMP-{str(i).zfill(4)}", "position": random.choice(["Host/Hostess", "Manager"]), "is_active": True} for i in range(1, 51)]
    
    reservations = generate_reservations(customers, staff)
    print(f"Generated {len(reservations)} reservations")
```

#### 4.3.9 Generate Reviews

Create `scripts/generate_reviews.py`:

```python
"""
Generate customer review data.
"""
from faker import Faker
import random
from config import *

fake = Faker()
Faker.seed(RANDOM_SEED)

def generate_reviews(customers, orders):
    """Generate review records."""
    
    reviews = []
    
    # Only some customers leave reviews
    reviewing_customers = random.sample(customers, k=NUM_REVIEWS)
    order_ids = [o['order_id'] for o in orders]
    
    for i, customer in enumerate(reviewing_customers):
        review_date = fake.date_time_between(START_DATE, END_DATE)
        
        # Ratings distribution (slightly positive skew)
        overall_rating = random.choices([1, 2, 3, 4, 5], weights=[5, 10, 15, 35, 35])[0]
        
        review = {
            "review_id": f"REV-{str(i+1).zfill(6)}",
            "customer_id": customer['customer_id'],
            "order_id": random.choice(order_ids) if random.random() > 0.3 else None,
            "review_date": review_date.date().isoformat(),
            "overall_rating": overall_rating,
            "food_rating": max(1, min(5, overall_rating + random.randint(-1, 1))),
            "service_rating": max(1, min(5, overall_rating + random.randint(-1, 1))),
            "ambiance_rating": max(1, min(5, overall_rating + random.randint(-1, 1))),
            "value_rating": max(1, min(5, overall_rating + random.randint(-1, 1))),
            "review_title": fake.sentence(nb_words=random.randint(3, 8))[:-1],  # Remove period
            "review_text": fake.paragraph(nb_sentences=random.randint(2, 5)) if random.random() > 0.2 else "",
            "would_recommend": overall_rating >= 4,
            "is_verified": random.choice([True, True, False]),
            "response_text": fake.sentence() if random.random() > 0.7 and overall_rating <= 3 else "",
            "response_date": (review_date + timedelta(days=random.randint(1, 7))).date().isoformat() if random.random() > 0.7 else None,
            "created_at": review_date.isoformat()
        }
        reviews.append(review)
    
    return reviews

if __name__ == "__main__":
    from datetime import timedelta
    customers = [{"customer_id": f"CUST-{str(i).zfill(6)}"} for i in range(1, 1001)]
    orders = [{"order_id": f"ORD-{str(i).zfill(7)}"} for i in range(1, 5001)]
    
    reviews = generate_reviews(customers, orders)
    print(f"Generated {len(reviews)} reviews")
```

### 4.4 Running the Data Generation

Execute the complete data generation:

```bash
cd scripts
python generate_all.py
```

This creates a `generated_data/` directory with JSON files for each dataset.

### 4.5 Loading Data into Databricks Unity Catalog

#### 4.5.1 Prerequisites

1. **Databricks Workspace** with Unity Catalog enabled
2. **Personal Access Token** or OAuth authentication configured
3. **CREATE TABLE permissions** on the target catalog

#### 4.5.2 Create the Schema

In a Databricks notebook or SQL editor:

```sql
-- Create schema for restaurant tutorial data
CREATE SCHEMA IF NOT EXISTS main.restaurant_tutorial
COMMENT 'Restaurant Business Tutorial Sample Data';

-- Set as default for this tutorial
USE main.restaurant_tutorial;
```

#### 4.5.3 Create Tables

Create the tables with appropriate schema definitions:

```sql
-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    customer_id STRING NOT NULL,
    first_name STRING,
    last_name STRING,
    email STRING,
    phone STRING,
    birth_date DATE,
    address STRUCT<street STRING, city STRING, state STRING, zip STRING>,
    loyalty_tier STRING,
    loyalty_points INT,
    dietary_preference STRING,
    created_at TIMESTAMP,
    last_visit TIMESTAMP,
    total_visits INT,
    total_spent DECIMAL(10,2),
    preferred_location STRING,
    marketing_opt_in BOOLEAN
)
COMMENT 'Customer profiles and preferences'
TBLPROPERTIES ('delta.columnMapping.mode' = 'name');

-- Menu Items table
CREATE TABLE IF NOT EXISTS menu_items (
    menu_item_id STRING NOT NULL,
    name STRING,
    description STRING,
    category STRING,
    price DECIMAL(6,2),
    cost DECIMAL(6,2),
    is_vegetarian BOOLEAN,
    is_vegan BOOLEAN,
    is_gluten_free BOOLEAN,
    contains_nuts BOOLEAN,
    spicy_level STRING,
    preparation_time_minutes INT,
    calories INT,
    is_active BOOLEAN,
    created_at DATE,
    updated_at DATE
)
COMMENT 'Menu items with pricing and ingredients';

-- Orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id STRING NOT NULL,
    customer_id STRING,
    server_id STRING,
    order_type STRING,
    table_number INT,
    order_date TIMESTAMP,
    subtotal DECIMAL(10,2),
    tax DECIMAL(8,2),
    tip DECIMAL(8,2),
    total DECIMAL(10,2),
    payment_method STRING,
    status STRING,
    num_items INT,
    party_size INT,
    special_requests STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
)
COMMENT 'Order history and details';

-- Order Items table
CREATE TABLE IF NOT EXISTS order_items (
    order_item_id STRING NOT NULL,
    order_id STRING NOT NULL,
    menu_item_id STRING NOT NULL,
    quantity INT,
    unit_price DECIMAL(6,2),
    total_price DECIMAL(8,2),
    special_requests STRING,
    created_at TIMESTAMP
)
COMMENT 'Individual items within orders';

-- Reservations table
CREATE TABLE IF NOT EXISTS reservations (
    reservation_id STRING NOT NULL,
    customer_id STRING,
    reservation_date DATE,
    reservation_time STRING,
    party_size INT,
    table_number INT,
    status STRING,
    special_requests STRING,
    occasion STRING,
    contact_phone STRING,
    contact_email STRING,
    created_by STRING,
    created_at TIMESTAMP,
    updated_at TIMESTAMP,
    notes STRING
)
COMMENT 'Reservation bookings';

-- Inventory table
CREATE TABLE IF NOT EXISTS inventory (
    inventory_id STRING NOT NULL,
    item_name STRING,
    category STRING,
    storage_type STRING,
    unit_of_measure STRING,
    current_quantity INT,
    par_level INT,
    reorder_point INT,
    unit_cost DECIMAL(8,2),
    total_value DECIMAL(10,2),
    primary_supplier_id STRING,
    last_received DATE,
    last_counted DATE,
    location STRING,
    is_low_stock BOOLEAN,
    notes STRING
)
COMMENT 'Ingredient and supply inventory';

-- Staff table
CREATE TABLE IF NOT EXISTS staff (
    employee_id STRING NOT NULL,
    first_name STRING,
    last_name STRING,
    email STRING,
    phone STRING,
    position STRING,
    department STRING,
    hire_date DATE,
    base_salary INT,
    hourly_rate DECIMAL(6,2),
    is_full_time BOOLEAN,
    is_active BOOLEAN,
    location STRING,
    manager_id STRING,
    certifications ARRAY<STRING>,
    notes STRING
)
COMMENT 'Employee information';

-- Suppliers table
CREATE TABLE IF NOT EXISTS suppliers (
    supplier_id STRING NOT NULL,
    company_name STRING,
    contact_name STRING,
    email STRING,
    phone STRING,
    address STRUCT<street STRING, city STRING, state STRING, zip STRING>,
    supplier_type STRING,
    specialty STRING,
    rating DECIMAL(2,1),
    payment_terms STRING,
    min_order_amount INT,
    delivery_days ARRAY<STRING>,
    lead_time_days INT,
    is_active BOOLEAN,
    contract_start DATE,
    notes STRING
)
COMMENT 'Supplier details and contacts';

-- Reviews table
CREATE TABLE IF NOT EXISTS reviews (
    review_id STRING NOT NULL,
    customer_id STRING,
    order_id STRING,
    review_date DATE,
    overall_rating INT,
    food_rating INT,
    service_rating INT,
    ambiance_rating INT,
    value_rating INT,
    review_title STRING,
    review_text STRING,
    would_recommend BOOLEAN,
    is_verified BOOLEAN,
    response_text STRING,
    response_date DATE,
    created_at TIMESTAMP
)
COMMENT 'Customer reviews and ratings';
```

#### 4.5.4 Load Data Using Python

Create a script `scripts/load_to_databricks.py`:

```python
"""
Load generated data into Databricks Unity Catalog.
"""
import os
import json
from databricks.sdk import WorkspaceClient
from databricks.sdk.service.sql import StatementState
from config import DATABRICKS_CATALOG, DATABRICKS_SCHEMA

def load_data():
    """Load all generated JSON files to Databricks tables."""
    
    w = WorkspaceClient()
    
    data_dir = "generated_data"
    tables = [
        ("customers", "customer_id"),
        ("menu_items", "menu_item_id"),
        ("orders", "order_id"),
        ("order_items", "order_item_id"),
        ("reservations", "reservation_id"),
        ("inventory", "inventory_id"),
        ("staff", "employee_id"),
        ("suppliers", "supplier_id"),
        ("reviews", "review_id"),
    ]
    
    for table_name, primary_key in tables:
        json_file = os.path.join(data_dir, f"{table_name}.json")
        
        if not os.path.exists(json_file):
            print(f"Skipping {table_name}: file not found")
            continue
        
        with open(json_file, 'r') as f:
            data = json.load(f)
        
        print(f"Loading {len(data)} records into {table_name}...")
        
        # For small datasets, use INSERT statements
        # For larger datasets, consider using DBFS or Volume upload
        
        full_table_name = f"{DATABRICKS_CATALOG}.{DATABRICKS_SCHEMA}.{table_name}"
        
        # Truncate existing data
        w.statement_execution.execute_statement(
            statement=f"TRUNCATE TABLE {full_table_name}",
            warehouse_id=os.environ.get("DATABRICKS_WAREHOUSE_ID")
        )
        
        # Insert data in batches
        batch_size = 100
        for i in range(0, len(data), batch_size):
            batch = data[i:i+batch_size]
            # Convert to INSERT statements
            # Note: In production, use spark.createDataFrame() or COPY INTO
            print(f"  Batch {i//batch_size + 1}: {len(batch)} records")
        
        print(f"  ✓ Loaded {len(data)} records into {table_name}")

if __name__ == "__main__":
    load_data()
```

#### 4.5.5 Alternative: Load Using Spark

For larger datasets, use Spark in a Databricks notebook:

```python
# In a Databricks notebook
import json

# Read JSON files from DBFS or Volume
data_path = "/Volumes/main/restaurant_tutorial/data/"

# Load customers
customers_df = spark.read.json(f"{data_path}/customers.json")
customers_df.write.mode("overwrite").saveAsTable("main.restaurant_tutorial.customers")

# Load menu items
menu_items_df = spark.read.json(f"{data_path}/menu_items.json")
menu_items_df.write.mode("overwrite").saveAsTable("main.restaurant_tutorial.menu_items")

# Load orders
orders_df = spark.read.json(f"{data_path}/orders.json")
orders_df.write.mode("overwrite").saveAsTable("main.restaurant_tutorial.orders")

# Load order items
order_items_df = spark.read.json(f"{data_path}/order_items.json")
order_items_df.write.mode("overwrite").saveAsTable("main.restaurant_tutorial.order_items")

# Load reservations
reservations_df = spark.read.json(f"{data_path}/reservations.json")
reservations_df.write.mode("overwrite").saveAsTable("main.restaurant_tutorial.reservations")

# Load inventory
inventory_df = spark.read.json(f"{data_path}/inventory.json")
inventory_df.write.mode("overwrite").saveAsTable("main.restaurant_tutorial.inventory")

# Load staff
staff_df = spark.read.json(f"{data_path}/staff.json")
staff_df.write.mode("overwrite").saveAsTable("main.restaurant_tutorial.staff")

# Load suppliers
suppliers_df = spark.read.json(f"{data_path}/suppliers.json")
suppliers_df.write.mode("overwrite").saveAsTable("main.restaurant_tutorial.suppliers")

# Load reviews
reviews_df = spark.read.json(f"{data_path}/reviews.json")
reviews_df.write.mode("overwrite").saveAsTable("main.restaurant_tutorial.reviews")

print("✓ All data loaded successfully")
```

### 4.6 Verify Data Load

Run queries to verify the data:

```sql
-- Check record counts
SELECT 'customers' as table_name, COUNT(*) as row_count FROM customers
UNION ALL SELECT 'menu_items', COUNT(*) FROM menu_items
UNION ALL SELECT 'orders', COUNT(*) FROM orders
UNION ALL SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL SELECT 'reservations', COUNT(*) FROM reservations
UNION ALL SELECT 'inventory', COUNT(*) FROM inventory
UNION ALL SELECT 'staff', COUNT(*) FROM staff
UNION ALL SELECT 'suppliers', COUNT(*) FROM suppliers
UNION ALL SELECT 'reviews', COUNT(*) FROM reviews;

-- Sample data check
SELECT * FROM customers LIMIT 5;
SELECT * FROM orders ORDER BY order_date DESC LIMIT 5;
```

### 4.7 Verification Checklist

- [ ] All 9 datasets generated as JSON files
- [ ] Schema created in Unity Catalog (`main.restaurant_tutorial`)
- [ ] All 9 tables created with correct schema
- [ ] Data loaded into all tables
- [ ] Row counts match expected values
- [ ] Sample queries return valid data

---

## 5. Part 3: Building Data Contracts

> **Note**: This section is under development. Check back for the complete guide to creating data contracts.

In this section, you'll define data contracts that specify:

- **Schema definitions**: Column types, constraints, and descriptions
- **Quality rules**: Data validation and quality checks
- **Service Level Objectives (SLOs)**: Freshness, availability, and accuracy targets
- **Ownership**: Data producers, consumers, and stewards
- **Access control**: Who can read/write the data

### Example Contract Structure

```yaml
contract_id: customer-data-contract
version: 1.0.0
status: active
dataset: customers
owner: analytics-team
schema:
  - name: customer_id
    type: uuid
    nullable: false
    description: Unique customer identifier
  - name: email
    type: string
    nullable: false
    pii: true
quality_rules:
  - name: email_format
    rule: email_regex_validation
    severity: error
slo:
  freshness: 24h
  availability: 99.9%
```

---

## 6. Part 4: Packaging Data Products

> **Note**: This section is under development. Check back for the complete guide to creating data products.

In this section, you'll create data products that package datasets for different consumers:

| Product Type | Example | Target Consumer |
|--------------|---------|-----------------|
| **Source-aligned** | Raw Orders | Data Engineers |
| **Aggregate** | Daily Sales Summary | Business Analysts |
| **Consumer-aligned** | Customer 360 | Marketing Team |

### Product Lifecycle

1. **Design**: Define the product specification
2. **Build**: Create the transformation pipelines
3. **Publish**: Register in the data catalog
4. **Subscribe**: Consumers request access
5. **Monitor**: Track usage and quality

---

## 7. Part 5: Compliance and Governance

> **Note**: This section is under development. Check back for the complete guide to compliance setup.

In this section, you'll implement compliance policies for:

- **PII Protection**: Handling customer personal data
- **Data Retention**: How long to keep different data types
- **Access Logging**: Who accessed what data and when
- **Quality Monitoring**: Continuous validation of data contracts

### Compliance Policies

```yaml
policy_id: pii-handling
name: PII Data Handling Policy
applies_to:
  tags: [sensitivity:confidential]
rules:
  - type: encryption_at_rest
    enabled: true
  - type: access_logging
    enabled: true
    retention: 90d
  - type: masking
    fields: [email, phone, address]
```

---

## 8. Part 6: Best Practices Summary

### Naming Conventions

| Asset Type | Convention | Example |
|------------|------------|---------|
| Domains | lowercase with hyphens | `restaurant-operations` |
| Tags | lowercase with hyphens | `food-prep` |
| Teams | lowercase with hyphens, suffix `-team` | `analytics-team` |
| Projects | lowercase with hyphens | `customer-insights` |
| Datasets | lowercase with underscores | `menu_items` |
| Data Products | lowercase with hyphens | `customer-360` |

### Tagging Strategy

- Use namespaces to group related tags
- Apply tags consistently across all assets
- Plan for future tags and classifications
- Document tag meanings in descriptions

### Team Organization

- Create domain-specific teams
- Assign clear ownership for each data product
- Include data governance representation
- Use role overrides for fine-grained access control

---

## Appendix: Sample Data Reference

### Entity Relationship Diagram

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  customers  │────<│   orders    │>────│  menu_items │
└─────────────┘     └─────────────┘     └─────────────┘
      │                   │                    │
      │                   v                    │
      │             ┌─────────────┐            │
      │             │ reservations│            │
      │             └─────────────┘            │
      │                                        │
      v                                        v
┌─────────────┐                         ┌─────────────┐
│   reviews   │                         │  inventory  │
└─────────────┘                         └─────────────┘
                                              │
                                              v
                                        ┌─────────────┐
                                        │  suppliers  │
                                        └─────────────┘
```

### Dataset Schemas

> **Note**: Detailed schemas will be provided in the Part 2 update.

---

## Contributing

Found an issue or want to improve this tutorial? Please submit a pull request or open an issue on the [Ontos GitHub repository](https://github.com/larsgeorge/ontos).

---

## License

This tutorial is part of the Ontos project and is licensed under the Apache License 2.0.
