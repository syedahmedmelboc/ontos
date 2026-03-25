"""
Menu data generator for restaurant sample data.

Generates realistic menu structure including:
- Menu categories
- Menu items with prices and descriptions
- Dietary flags (vegetarian, vegan, gluten-free)
- Availability status
"""

import random
from typing import List, Dict, Any

from faker import Faker

from config import FAKER_SEED, EntityCounts, MENU_CATEGORIES, MENU_ITEM_TEMPLATES
from utils import generate_short_id, write_json, write_csv

# Initialize Faker with fixed seed
fake = Faker()
Faker.seed(FAKER_SEED)
random.seed(FAKER_SEED)


def generate_menu_category(category_id: str, category_data: Dict[str, str], sort_order: int) -> Dict[str, Any]:
    """
    Generate a single menu category record.
    
    Args:
        category_id: Unique identifier for the category
        category_data: Dictionary with 'name' and 'description'
        sort_order: Display order on menu
        
    Returns:
        Dictionary containing category data
    """
    return {
        "category_id": category_id,
        "name": category_data["name"],
        "description": category_data["description"],
        "sort_order": sort_order,
        "is_active": True,
        "created_at": fake.date_time_between(start_date="-2y", end_date="now").isoformat(),
    }


def generate_menu_item(
    item_id: str,
    category_id: str,
    item_template: Dict[str, Any],
    category_name: str
) -> Dict[str, Any]:
    """
    Generate a single menu item record.
    
    Args:
        item_id: Unique identifier for the item
        category_id: ID of the parent category
        item_template: Template with name, price_range, vegetarian flag
        category_name: Name of the category for description generation
        
    Returns:
        Dictionary containing menu item data
    """
    # Generate price within range
    price_range = item_template["price_range"]
    price = round(random.uniform(price_range[0], price_range[1]), 2)
    
    # Determine dietary flags
    is_vegetarian = item_template.get("vegetarian", False)
    is_vegan = is_vegetarian and random.random() < 0.3  # 30% of vegetarian items are vegan
    is_gluten_free = random.random() < 0.15  # 15% are gluten-free
    
    # Generate description
    descriptions = [
        f"Our signature {item_template['name'].lower()}, prepared fresh daily with premium ingredients.",
        f"Delicious {item_template['name'].lower()} made with locally sourced ingredients.",
        f"Classic {item_template['name'].lower()}, a customer favorite for years.",
        f"Chef's special {item_template['name'].lower()}, crafted with care and attention to detail.",
    ]
    
    # Add dietary info to description if applicable
    description = random.choice(descriptions)
    if is_vegan:
        description += " Vegan-friendly."
    elif is_vegetarian:
        description += " Vegetarian option."
    if is_gluten_free:
        description += " Gluten-free."
    
    # Generate realistic preparation time
    prep_time_range = {
        "Appetizers": (5, 12),
        "Soups & Salads": (5, 10),
        "Pizza": (15, 25),
        "Pasta": (12, 20),
        "Mains - Chicken": (15, 25),
        "Mains - Beef": (18, 30),
        "Mains - Seafood": (15, 25),
        "Mains - Vegetarian": (12, 20),
        "Sides": (5, 10),
        "Desserts": (5, 15),
        "Beverages - Hot": (2, 5),
        "Beverages - Cold": (1, 3),
        "Alcoholic - Wine": (1, 2),
        "Alcoholic - Beer": (1, 2),
        "Alcoholic - Cocktails": (3, 7),
    }
    
    prep_range = prep_time_range.get(category_name, (10, 20))
    prep_time_minutes = random.randint(prep_range[0], prep_range[1])
    
    return {
        "item_id": item_id,
        "category_id": category_id,
        "name": item_template["name"],
        "description": description,
        "price": price,
        "cost": round(price * random.uniform(0.25, 0.40), 2),  # 25-40% food cost
        "preparation_time_minutes": prep_time_minutes,
        "is_vegetarian": is_vegetarian,
        "is_vegan": is_vegan,
        "is_gluten_free": is_gluten_free,
        "contains_allergens": generate_allergens(),
        "calories": random.randint(150, 1200) if category_name not in ["Beverages - Hot", "Beverages - Cold"] else random.randint(5, 300),
        "is_available": True,
        "is_featured": random.random() < 0.10,  # 10% are featured
        "created_at": fake.date_time_between(start_date="-2y", end_date="now").isoformat(),
        "updated_at": fake.date_time_between(start_date="-6m", end_date="now").isoformat(),
    }


def generate_allergens() -> List[str]:
    """Generate a list of allergens for a menu item."""
    allergens = ["dairy", "eggs", "fish", "shellfish", "tree_nuts", "peanuts", "wheat", "soy", "sesame"]
    # 60% of items have at least one allergen
    if random.random() < 0.60:
        num_allergens = random.choices([1, 2, 3, 4], weights=[0.5, 0.3, 0.15, 0.05])[0]
        return random.sample(allergens, min(num_allergens, len(allergens)))
    return []


def generate_menu() -> tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Generate complete menu with categories and items.
    
    Returns:
        Tuple of (categories, items) lists
    """
    categories = []
    items = []
    
    used_category_ids = set()
    used_item_ids = set()
    
    for sort_order, category_data in enumerate(MENU_CATEGORIES):
        # Generate unique category ID
        category_id = f"CAT-{generate_short_id(length=4)}"
        while category_id in used_category_ids:
            category_id = f"CAT-{generate_short_id(length=4)}"
        used_category_ids.add(category_id)
        
        # Generate category
        category = generate_menu_category(category_id, category_data, sort_order)
        categories.append(category)
        
        # Get item templates for this category
        category_name = category_data["name"]
        templates = MENU_ITEM_TEMPLATES.get(category_name, [])
        
        # Generate items from templates
        for template in templates:
            item_id = f"ITEM-{generate_short_id(length=5)}"
            while item_id in used_item_ids:
                item_id = f"ITEM-{generate_short_id(length=5)}"
            used_item_ids.add(item_id)
            
            item = generate_menu_item(item_id, category_id, template, category_name)
            items.append(item)
    
    return categories, items


def main(output_dir: str = "output") -> tuple[List[Dict], List[Dict]]:
    """
    Main function to generate and save menu data.
    
    Args:
        output_dir: Directory to save output files
        
    Returns:
        Tuple of (categories, items) lists
    """
    print("\n🍽️  Generating menu data...")
    
    categories, items = generate_menu()
    
    # Save to files
    write_json(categories, "menu_categories.json", output_dir)
    write_csv(categories, "menu_categories.csv", output_dir)
    write_json(items, "menu_items.json", output_dir)
    write_csv(items, "menu_items.csv", output_dir)
    
    # Print summary stats
    print(f"  📊 Generated {len(categories)} categories with {len(items)} items")
    
    # Category breakdown
    print("  📊 Items per category:")
    category_counts = {}
    for item in items:
        cat_id = item["category_id"]
        cat_name = next((c["name"] for c in categories if c["category_id"] == cat_id), "Unknown")
        category_counts[cat_name] = category_counts.get(cat_name, 0) + 1
    
    for cat_name, count in sorted(category_counts.items()):
        print(f"     {cat_name}: {count}")
    
    # Dietary stats
    veg_count = sum(1 for i in items if i["is_vegetarian"])
    vegan_count = sum(1 for i in items if i["is_vegan"])
    gf_count = sum(1 for i in items if i["is_gluten_free"])
    print(f"  📊 Dietary options: {veg_count} vegetarian, {vegan_count} vegan, {gf_count} gluten-free")
    
    return categories, items


if __name__ == "__main__":
    main()
