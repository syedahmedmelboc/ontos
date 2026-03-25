"""
Configuration for restaurant sample data generation.

This module contains all configuration parameters for generating
realistic restaurant business data using the Faker library.
"""

from dataclasses import dataclass
from typing import Dict, List

# Set a fixed seed for reproducible data generation
FAKER_SEED = 42

# Entity counts - realistic but manageable for tutorial purposes
@dataclass
class EntityCounts:
    customers: int = 1000
    menu_categories: int = 15
    menu_items: int = 100
    orders: int = 5000
    reservations: int = 2000
    inventory_items: int = 50
    suppliers: int = 10
    staff: int = 30
    reviews: int = 1500


# Menu categories with realistic names and item type hints
MENU_CATEGORIES: List[Dict[str, str]] = [
    {"name": "Appetizers", "description": "Starters and small plates to share"},
    {"name": "Soups & Salads", "description": "Fresh soups and garden salads"},
    {"name": "Pizza", "description": "Hand-tossed pizzas with premium toppings"},
    {"name": "Pasta", "description": "Traditional Italian pasta dishes"},
    {"name": "Mains - Chicken", "description": "Chicken entrées and specialties"},
    {"name": "Mains - Beef", "description": "Premium beef and steak dishes"},
    {"name": "Mains - Seafood", "description": "Fresh seafood and fish dishes"},
    {"name": "Mains - Vegetarian", "description": "Plant-based main courses"},
    {"name": "Sides", "description": "Accompaniments and side dishes"},
    {"name": "Desserts", "description": "Sweet treats and desserts"},
    {"name": "Beverages - Hot", "description": "Coffee, tea, and hot drinks"},
    {"name": "Beverages - Cold", "description": "Soft drinks and juices"},
    {"name": "Alcoholic - Wine", "description": "Wine selection by glass and bottle"},
    {"name": "Alcoholic - Beer", "description": "Craft beers and imports"},
    {"name": "Alcoholic - Cocktails", "description": "Signature cocktails and classics"},
]

# Sample menu item templates by category
MENU_ITEM_TEMPLATES: Dict[str, List[Dict[str, any]]] = {
    "Appetizers": [
        {"name": "Bruschetta", "price_range": (8, 12), "vegetarian": True},
        {"name": "Calamari", "price_range": (12, 16), "vegetarian": False},
        {"name": "Caprese Salad", "price_range": (10, 14), "vegetarian": True},
        {"name": "Garlic Bread", "price_range": (6, 9), "vegetarian": True},
        {"name": "Stuffed Mushrooms", "price_range": (10, 14), "vegetarian": True},
        {"name": "Spring Rolls", "price_range": (8, 11), "vegetarian": True},
        {"name": "Chicken Wings", "price_range": (12, 16), "vegetarian": False},
        {"name": "Nachos", "price_range": (11, 15), "vegetarian": True},
    ],
    "Soups & Salads": [
        {"name": "Caesar Salad", "price_range": (10, 14), "vegetarian": True},
        {"name": "Garden Salad", "price_range": (8, 11), "vegetarian": True},
        {"name": "Tomato Soup", "price_range": (7, 10), "vegetarian": True},
        {"name": "French Onion Soup", "price_range": (9, 12), "vegetarian": True},
        {"name": "Minestrone", "price_range": (7, 10), "vegetarian": True},
        {"name": "Greek Salad", "price_range": (11, 14), "vegetarian": True},
    ],
    "Pizza": [
        {"name": "Margherita", "price_range": (14, 18), "vegetarian": True},
        {"name": "Pepperoni", "price_range": (16, 20), "vegetarian": False},
        {"name": "Hawaiian", "price_range": (16, 20), "vegetarian": False},
        {"name": "BBQ Chicken", "price_range": (18, 22), "vegetarian": False},
        {"name": "Vegetarian", "price_range": (15, 19), "vegetarian": True},
        {"name": "Meat Lovers", "price_range": (19, 24), "vegetarian": False},
        {"name": "Four Cheese", "price_range": (16, 20), "vegetarian": True},
        {"name": "Seafood Pizza", "price_range": (20, 25), "vegetarian": False},
    ],
    "Pasta": [
        {"name": "Spaghetti Carbonara", "price_range": (16, 20), "vegetarian": False},
        {"name": "Fettuccine Alfredo", "price_range": (15, 19), "vegetarian": True},
        {"name": "Lasagna", "price_range": (18, 22), "vegetarian": False},
        {"name": "Penne Arrabbiata", "price_range": (14, 17), "vegetarian": True},
        {"name": "Linguine Pesto", "price_range": (15, 18), "vegetarian": True},
        {"name": "Ravioli", "price_range": (17, 21), "vegetarian": True},
        {"name": "Seafood Linguine", "price_range": (22, 27), "vegetarian": False},
        {"name": "Bolognese", "price_range": (17, 21), "vegetarian": False},
    ],
    "Mains - Chicken": [
        {"name": "Grilled Chicken Breast", "price_range": (18, 23), "vegetarian": False},
        {"name": "Chicken Parmesan", "price_range": (20, 25), "vegetarian": False},
        {"name": "Lemon Herb Chicken", "price_range": (19, 24), "vegetarian": False},
        {"name": "Chicken Marsala", "price_range": (21, 26), "vegetarian": False},
        {"name": "Stuffed Chicken", "price_range": (22, 27), "vegetarian": False},
    ],
    "Mains - Beef": [
        {"name": "Ribeye Steak", "price_range": (32, 42), "vegetarian": False},
        {"name": "Filet Mignon", "price_range": (38, 48), "vegetarian": False},
        {"name": "New York Strip", "price_range": (30, 38), "vegetarian": False},
        {"name": "Beef Tenderloin", "price_range": (35, 45), "vegetarian": False},
        {"name": "Braised Short Ribs", "price_range": (28, 35), "vegetarian": False},
    ],
    "Mains - Seafood": [
        {"name": "Grilled Salmon", "price_range": (24, 30), "vegetarian": False},
        {"name": "Sea Bass", "price_range": (28, 35), "vegetarian": False},
        {"name": "Shrimp Scampi", "price_range": (22, 28), "vegetarian": False},
        {"name": "Lobster Tail", "price_range": (38, 48), "vegetarian": False},
        {"name": "Fish and Chips", "price_range": (18, 23), "vegetarian": False},
    ],
    "Mains - Vegetarian": [
        {"name": "Vegetable Stir Fry", "price_range": (15, 19), "vegetarian": True},
        {"name": "Eggplant Parmesan", "price_range": (17, 21), "vegetarian": True},
        {"name": "Stuffed Bell Peppers", "price_range": (16, 20), "vegetarian": True},
        {"name": "Mushroom Risotto", "price_range": (18, 22), "vegetarian": True},
        {"name": "Veggie Burger", "price_range": (14, 18), "vegetarian": True},
    ],
    "Sides": [
        {"name": "French Fries", "price_range": (5, 7), "vegetarian": True},
        {"name": "Mashed Potatoes", "price_range": (5, 7), "vegetarian": True},
        {"name": "Steamed Vegetables", "price_range": (6, 8), "vegetarian": True},
        {"name": "Rice Pilaf", "price_range": (5, 7), "vegetarian": True},
        {"name": "Coleslaw", "price_range": (4, 6), "vegetarian": True},
        {"name": "Garlic Bread", "price_range": (5, 7), "vegetarian": True},
    ],
    "Desserts": [
        {"name": "Tiramisu", "price_range": (9, 12), "vegetarian": True},
        {"name": "Cheesecake", "price_range": (9, 12), "vegetarian": True},
        {"name": "Chocolate Lava Cake", "price_range": (10, 13), "vegetarian": True},
        {"name": "Gelato", "price_range": (7, 9), "vegetarian": True},
        {"name": "Panna Cotta", "price_range": (8, 11), "vegetarian": True},
        {"name": "Apple Pie", "price_range": (8, 11), "vegetarian": True},
    ],
    "Beverages - Hot": [
        {"name": "Espresso", "price_range": (3, 4), "vegetarian": True},
        {"name": "Cappuccino", "price_range": (4, 5), "vegetarian": True},
        {"name": "Latte", "price_range": (4, 6), "vegetarian": True},
        {"name": "Americano", "price_range": (3, 4), "vegetarian": True},
        {"name": "Hot Tea", "price_range": (3, 4), "vegetarian": True},
        {"name": "Hot Chocolate", "price_range": (4, 5), "vegetarian": True},
    ],
    "Beverages - Cold": [
        {"name": "Soft Drink", "price_range": (3, 4), "vegetarian": True},
        {"name": "Fresh Juice", "price_range": (5, 7), "vegetarian": True},
        {"name": "Iced Tea", "price_range": (3, 5), "vegetarian": True},
        {"name": "Lemonade", "price_range": (4, 5), "vegetarian": True},
        {"name": "Smoothie", "price_range": (6, 8), "vegetarian": True},
    ],
    "Alcoholic - Wine": [
        {"name": "House Red (Glass)", "price_range": (9, 12), "vegetarian": True},
        {"name": "House White (Glass)", "price_range": (9, 12), "vegetarian": True},
        {"name": "Premium Red (Glass)", "price_range": (14, 18), "vegetarian": True},
        {"name": "Premium White (Glass)", "price_range": (14, 18), "vegetarian": True},
        {"name": "Prosecco (Glass)", "price_range": (10, 13), "vegetarian": True},
        {"name": "Rosé (Glass)", "price_range": (10, 14), "vegetarian": True},
    ],
    "Alcoholic - Beer": [
        {"name": "Draft Beer", "price_range": (6, 8), "vegetarian": True},
        {"name": "Craft IPA", "price_range": (8, 10), "vegetarian": True},
        {"name": "Imported Lager", "price_range": (7, 9), "vegetarian": True},
        {"name": "Stout", "price_range": (8, 10), "vegetarian": True},
        {"name": "Wheat Beer", "price_range": (7, 9), "vegetarian": True},
    ],
    "Alcoholic - Cocktails": [
        {"name": "Margarita", "price_range": (11, 14), "vegetarian": True},
        {"name": "Mojito", "price_range": (11, 14), "vegetarian": True},
        {"name": "Old Fashioned", "price_range": (13, 16), "vegetarian": True},
        {"name": "Martini", "price_range": (13, 16), "vegetarian": True},
        {"name": "Cosmopolitan", "price_range": (12, 15), "vegetarian": True},
        {"name": "Negroni", "price_range": (12, 15), "vegetarian": True},
        {"name": "Signature Cocktail", "price_range": (14, 18), "vegetarian": True},
    ],
}

# Loyalty tier distribution (realistic percentages)
LOYALTY_DISTRIBUTION = {
    "Bronze": 0.50,    # 50% of customers
    "Silver": 0.30,   # 30% of customers
    "Gold": 0.15,     # 15% of customers
    "Platinum": 0.05, # 5% of customers
}

# Order type distribution
ORDER_TYPE_DISTRIBUTION = {
    "dine_in": 0.55,   # 55% dine-in
    "takeout": 0.30,   # 30% takeout
    "delivery": 0.15,  # 15% delivery
}

# Order status distribution
ORDER_STATUS_DISTRIBUTION = {
    "completed": 0.75,    # 75% completed
    "cancelled": 0.08,    # 8% cancelled
    "confirmed": 0.05,    # 5% confirmed (pending prep)
    "preparing": 0.05,    # 5% preparing
    "ready": 0.04,        # 4% ready for pickup
    "pending": 0.03,      # 3% just placed
}

# Staff roles and their typical hourly rates
STAFF_ROLES = {
    "Executive Chef": {"hourly_rate": (35, 50), "count": 1},
    "Sous Chef": {"hourly_rate": (25, 35), "count": 2},
    "Line Cook": {"hourly_rate": (18, 25), "count": 6},
    "Prep Cook": {"hourly_rate": (15, 20), "count": 4},
    "Head Server": {"hourly_rate": (12, 18), "count": 2},
    "Server": {"hourly_rate": (10, 15), "count": 8},
    "Bartender": {"hourly_rate": (12, 18), "count": 3},
    "Host/Hostess": {"hourly_rate": (12, 16), "count": 2},
    "Manager": {"hourly_rate": (25, 35), "count": 2},
}

# Supplier categories
SUPPLIER_CATEGORIES = [
    {"name": "Fresh Produce", "lead_days": (1, 2)},
    {"name": "Meat & Poultry", "lead_days": (2, 4)},
    {"name": "Seafood", "lead_days": (1, 3)},
    {"name": "Dairy Products", "lead_days": (1, 2)},
    {"name": "Dry Goods", "lead_days": (3, 7)},
    {"name": "Beverages", "lead_days": (2, 5)},
    {"name": "Alcohol", "lead_days": (3, 7)},
    {"name": "Cleaning Supplies", "lead_days": (5, 10)},
    {"name": "Packaging", "lead_days": (5, 10)},
    {"name": "Specialty Items", "lead_days": (7, 14)},
]

# Inventory unit types
INVENTORY_UNITS = [
    "kg", "lb", "liter", "gallon", "piece", "case", "dozen", "box", "bottle", "can"
]

# Reservation status distribution
RESERVATION_STATUS_DISTRIBUTION = {
    "completed": 0.70,      # 70% showed up and completed
    "confirmed": 0.10,      # 10% confirmed but future
    "cancelled": 0.12,      # 12% cancelled
    "no_show": 0.08,        # 8% no-show
}

# Review rating distribution (realistic - most reviews are positive)
REVIEW_RATING_DISTRIBUTION = {
    5: 0.35,   # 35% five stars
    4: 0.30,   # 30% four stars
    3: 0.20,   # 20% three stars
    2: 0.10,   # 10% two stars
    1: 0.05,   # 5% one star
}
