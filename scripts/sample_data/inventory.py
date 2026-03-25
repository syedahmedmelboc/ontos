"""
Inventory and supplier data generator for restaurant sample data.

Generates realistic inventory data including:
- Supplier records with contact info
- Inventory items with quantities and reorder levels
- Supplier-item relationships
- Cost tracking
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from faker import Faker

from config import FAKER_SEED, EntityCounts, SUPPLIER_CATEGORIES, INVENTORY_UNITS
from utils import generate_short_id, write_json, write_csv

# Initialize Faker with fixed seed
fake = Faker()
Faker.seed(FAKER_SEED)
random.seed(FAKER_SEED)


# Inventory item templates by category
INVENTORY_TEMPLATES = {
    "Fresh Produce": [
        {"name": "Tomatoes", "unit": "kg", "base_cost": 3.50, "typical_qty": (20, 50)},
        {"name": "Onions", "unit": "kg", "base_cost": 1.50, "typical_qty": (15, 30)},
        {"name": "Lettuce", "unit": "piece", "base_cost": 2.00, "typical_qty": (20, 40)},
        {"name": "Bell Peppers", "unit": "kg", "base_cost": 4.00, "typical_qty": (10, 25)},
        {"name": "Garlic", "unit": "kg", "base_cost": 8.00, "typical_qty": (2, 5)},
        {"name": "Fresh Herbs", "unit": "bunch", "base_cost": 1.50, "typical_qty": (15, 30)},
        {"name": "Mushrooms", "unit": "kg", "base_cost": 12.00, "typical_qty": (5, 15)},
    ],
    "Meat & Poultry": [
        {"name": "Ground Beef", "unit": "kg", "base_cost": 12.00, "typical_qty": (20, 40)},
        {"name": "Chicken Breast", "unit": "kg", "base_cost": 9.00, "typical_qty": (25, 50)},
        {"name": "Ribeye Steak", "unit": "kg", "base_cost": 28.00, "typical_qty": (10, 20)},
        {"name": "Pork Loin", "unit": "kg", "base_cost": 11.00, "typical_qty": (10, 20)},
        {"name": "Italian Sausage", "unit": "kg", "base_cost": 10.00, "typical_qty": (10, 15)},
        {"name": "Bacon", "unit": "kg", "base_cost": 14.00, "typical_qty": (5, 10)},
    ],
    "Seafood": [
        {"name": "Salmon Fillet", "unit": "kg", "base_cost": 22.00, "typical_qty": (10, 20)},
        {"name": "Shrimp (21/25)", "unit": "kg", "base_cost": 18.00, "typical_qty": (8, 15)},
        {"name": "Cod Fillet", "unit": "kg", "base_cost": 16.00, "typical_qty": (10, 15)},
        {"name": "Calamari", "unit": "kg", "base_cost": 14.00, "typical_qty": (5, 10)},
        {"name": "Sea Bass", "unit": "kg", "base_cost": 26.00, "typical_qty": (5, 10)},
    ],
    "Dairy Products": [
        {"name": "Whole Milk", "unit": "liter", "base_cost": 1.20, "typical_qty": (40, 80)},
        {"name": "Heavy Cream", "unit": "liter", "base_cost": 4.50, "typical_qty": (10, 20)},
        {"name": "Mozzarella", "unit": "kg", "base_cost": 10.00, "typical_qty": (10, 20)},
        {"name": "Parmesan", "unit": "kg", "base_cost": 18.00, "typical_qty": (3, 6)},
        {"name": "Butter", "unit": "kg", "base_cost": 8.00, "typical_qty": (5, 10)},
        {"name": "Eggs (large)", "unit": "dozen", "base_cost": 4.00, "typical_qty": (20, 40)},
    ],
    "Dry Goods": [
        {"name": "All-Purpose Flour", "unit": "kg", "base_cost": 0.80, "typical_qty": (25, 50)},
        {"name": "Pasta (various)", "unit": "kg", "base_cost": 2.00, "typical_qty": (20, 40)},
        {"name": "Rice", "unit": "kg", "base_cost": 2.50, "typical_qty": (15, 30)},
        {"name": "Olive Oil", "unit": "liter", "base_cost": 8.00, "typical_qty": (10, 20)},
        {"name": "Canned Tomatoes", "unit": "case", "base_cost": 15.00, "typical_qty": (5, 10)},
        {"name": "Breadcrumbs", "unit": "kg", "base_cost": 3.00, "typical_qty": (3, 6)},
    ],
    "Beverages": [
        {"name": "Soft Drinks (assorted)", "unit": "case", "base_cost": 12.00, "typical_qty": (10, 20)},
        {"name": "Orange Juice", "unit": "liter", "base_cost": 3.00, "typical_qty": (15, 30)},
        {"name": "Coffee Beans", "unit": "kg", "base_cost": 18.00, "typical_qty": (5, 10)},
        {"name": "Tea (assorted)", "unit": "box", "base_cost": 8.00, "typical_qty": (5, 10)},
    ],
    "Alcohol": [
        {"name": "House Wine (red)", "unit": "bottle", "base_cost": 12.00, "typical_qty": (24, 48)},
        {"name": "House Wine (white)", "unit": "bottle", "base_cost": 12.00, "typical_qty": (24, 48)},
        {"name": "Draft Beer Keg", "unit": "keg", "base_cost": 120.00, "typical_qty": (2, 4)},
        {"name": "Vodka", "unit": "bottle", "base_cost": 22.00, "typical_qty": (6, 12)},
        {"name": "Whiskey", "unit": "bottle", "base_cost": 35.00, "typical_qty": (4, 8)},
    ],
}


def generate_supplier(supplier_id: str, category_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Generate a single supplier record.
    
    Args:
        supplier_id: Unique identifier
        category_data: Category info with name and lead_days
        
    Returns:
        Dictionary containing supplier data
    """
    company_name = fake.company()
    lead_days = random.randint(category_data["lead_days"][0], category_data["lead_days"][1])
    
    return {
        "supplier_id": supplier_id,
        "name": f"{company_name} {category_data['name']}",
        "category": category_data["name"],
        "contact_name": fake.name(),
        "contact_email": fake.company_email(),
        "contact_phone": fake.phone_number(),
        "address": fake.address().replace("\n", ", "),
        "lead_days": lead_days,
        "payment_terms": random.choice(["Net 30", "Net 15", "COD", "Net 45"]),
        "rating": round(random.uniform(3.5, 5.0), 1),
        "is_active": True,
        "created_at": fake.date_time_between(start_date="-3y", end_date="-6m").isoformat(),
    }


def generate_inventory_item(
    item_id: str,
    template: Dict[str, Any],
    supplier_id: str,
    category: str
) -> Dict[str, Any]:
    """
    Generate a single inventory item record.
    
    Args:
        item_id: Unique identifier
        template: Item template with name, unit, base_cost, typical_qty
        supplier_id: Primary supplier ID
        category: Category name
        
    Returns:
        Dictionary containing inventory item data
    """
    typical_min, typical_max = template["typical_qty"]
    quantity = random.randint(typical_min, typical_max)
    reorder_level = int(typical_min * 0.4)  # Reorder at 40% of min
    
    # Cost varies +/- 20% from base
    cost_per_unit = round(template["base_cost"] * random.uniform(0.85, 1.15), 2)
    
    return {
        "item_id": item_id,
        "name": template["name"],
        "category": category,
        "quantity": quantity,
        "unit": template["unit"],
        "reorder_level": reorder_level,
        "cost_per_unit": cost_per_unit,
        "total_value": round(quantity * cost_per_unit, 2),
        "primary_supplier_id": supplier_id,
        "storage_location": random.choice(["Walk-in Cooler", "Walk-in Freezer", "Dry Storage", "Bar Storage"]),
        "last_received_date": fake.date_between(start_date="-30d", end_date="today").isoformat(),
        "last_counted_date": fake.date_between(start_date="-7d", end_date="today").isoformat(),
        "is_active": True,
    }


def generate_inventory() -> tuple[List[Dict], List[Dict]]:
    """
    Generate complete inventory with suppliers.
    
    Returns:
        Tuple of (suppliers, inventory_items) lists
    """
    suppliers = []
    inventory_items = []
    used_supplier_ids = set()
    used_item_ids = set()
    
    # Generate one supplier per category
    for category_data in SUPPLIER_CATEGORIES:
        supplier_id = f"SUP-{generate_short_id(length=4)}"
        while supplier_id in used_supplier_ids:
            supplier_id = f"SUP-{generate_short_id(length=4)}"
        used_supplier_ids.add(supplier_id)
        
        supplier = generate_supplier(supplier_id, category_data)
        suppliers.append(supplier)
        
        # Generate inventory items for this category
        category_name = category_data["name"]
        templates = INVENTORY_TEMPLATES.get(category_name, [])
        
        for template in templates:
            item_id = f"INV-{generate_short_id(length=5)}"
            while item_id in used_item_ids:
                item_id = f"INV-{generate_short_id(length=5)}"
            used_item_ids.add(item_id)
            
            item = generate_inventory_item(item_id, template, supplier_id, category_name)
            inventory_items.append(item)
    
    return suppliers, inventory_items


def main(output_dir: str = "output") -> tuple[List[Dict], List[Dict]]:
    """
    Main function to generate and save inventory data.
    
    Args:
        output_dir: Directory to save output files
        
    Returns:
        Tuple of (suppliers, inventory_items) lists
    """
    print("\n📦 Generating inventory and supplier data...")
    
    suppliers, inventory_items = generate_inventory()
    
    # Save to files
    write_json(suppliers, "suppliers.json", output_dir)
    write_csv(suppliers, "suppliers.csv", output_dir)
    write_json(inventory_items, "inventory.json", output_dir)
    write_csv(inventory_items, "inventory.csv", output_dir)
    
    # Print summary stats
    print(f"  📊 Generated {len(suppliers)} suppliers")
    print(f"  📊 Generated {len(inventory_items)} inventory items")
    
    # Category breakdown
    category_counts = {}
    for item in inventory_items:
        cat = item["category"]
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    print("  📊 Inventory by category:")
    for cat, count in sorted(category_counts.items()):
        print(f"     {cat}: {count}")
    
    # Total inventory value
    total_value = sum(item["total_value"] for item in inventory_items)
    print(f"  📊 Total inventory value: ${total_value:,.2f}")
    
    # Items below reorder level
    below_reorder = sum(1 for item in inventory_items if item["quantity"] < item["reorder_level"])
    print(f"  📊 Items below reorder level: {below_reorder}")
    
    return suppliers, inventory_items


if __name__ == "__main__":
    main()
