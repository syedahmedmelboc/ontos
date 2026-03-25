"""
Order data generator for restaurant sample data.

Generates realistic order data including:
- Order headers with customer and timing information
- Order line items with menu item references
- Realistic order patterns (lunch/dinner rushes)
- Order status distribution
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple

from faker import Faker

from config import (
    FAKER_SEED, EntityCounts, 
    ORDER_TYPE_DISTRIBUTION, 
    ORDER_STATUS_DISTRIBUTION
)
from utils import (
    generate_short_id,
    weighted_choice,
    weighted_choice_int,
    generate_order_timestamp,
    calculate_order_total,
    write_json,
    write_csv
)

# Initialize Faker with fixed seed
fake = Faker()
Faker.seed(FAKER_SEED)
random.seed(FAKER_SEED)


def select_order_items(
    menu_items: List[Dict[str, Any]], 
    min_items: int = 1, 
    max_items: int = 6
) -> List[Dict[str, Any]]:
    """
    Select random menu items for an order.
    
    Realistic ordering patterns:
    - Most orders have 2-4 items
    - Entrees are usually ordered
    - Sides and drinks are common additions
    - Desserts are less common
    
    Args:
        menu_items: List of available menu items
        min_items: Minimum number of items
        max_items: Maximum number of items
        
    Returns:
        List of selected items with quantities
    """
    # Weight items by category (entrees more likely than desserts)
    category_weights = {
        "Mains": 1.0,
        "Pizza": 0.8,
        "Pasta": 0.8,
        "Appetizers": 0.6,
        "Sides": 0.5,
        "Beverages": 0.7,
        "Desserts": 0.3,
        "Soups & Salads": 0.4,
        "Alcoholic": 0.5,
    }
    
    # Calculate weights for each item
    weights = []
    for item in menu_items:
        # Extract category from category_id (simplified)
        category = item.get("category_id", "").replace("CAT-", "")
        weight = 0.5  # default
        for cat_key, cat_weight in category_weights.items():
            if cat_key.lower() in category.lower():
                weight = cat_weight
                break
        weights.append(weight)
    
    # Determine number of items (weighted towards 2-4)
    num_items_dist = {1: 0.10, 2: 0.25, 3: 0.30, 4: 0.20, 5: 0.10, 6: 0.05}
    num_items = weighted_choice_int(num_items_dist)
    num_items = max(min_items, min(num_items, max_items))
    
    # Select items with replacement (can order multiple of same item)
    selected_items = []
    selected_indices = set()
    
    attempts = 0
    while len(selected_items) < num_items and attempts < 20:
        # Select an item using weights
        idx = random.choices(range(len(menu_items)), weights=weights, k=1)[0]
        item = menu_items[idx]
        
        # Create order item
        quantity = random.choices([1, 2, 3], weights=[0.85, 0.12, 0.03])[0]
        
        order_item = {
            "item_id": item["item_id"],
            "item_name": item["name"],
            "quantity": quantity,
            "unit_price": item["price"],
            "special_requests": generate_special_requests() if random.random() < 0.25 else None,
        }
        
        selected_items.append(order_item)
        attempts += 1
    
    return selected_items


def generate_special_requests() -> str:
    """Generate a random special request."""
    requests = [
        "No onions",
        "Extra sauce on the side",
        "Dressing on the side",
        "No cheese",
        "Extra spicy",
        "Well done",
        "Medium rare",
        "No salt",
        "Gluten-free preparation",
        "Dairy-free please",
        "Allergies: nuts",
        "Substitute fries for salad",
        "Extra vegetables",
        "No cilantro",
        "Light on the dressing",
    ]
    return random.choice(requests)


def generate_order(
    order_id: str,
    customers: List[Dict[str, Any]],
    menu_items: List[Dict[str, Any]],
    order_date: datetime
) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
    """
    Generate a single order with line items.
    
    Args:
        order_id: Unique identifier for the order
        customers: List of customers to select from
        menu_items: List of menu items to select from
        order_date: Date/time of the order
        
    Returns:
        Tuple of (order, order_items)
    """
    # Select customer (80% of orders have registered customer)
    if random.random() < 0.80 and customers:
        customer = random.choice(customers)
        customer_id = customer["customer_id"]
    else:
        customer_id = None  # Walk-in or guest order
    
    # Select order type
    order_type = weighted_choice(ORDER_TYPE_DISTRIBUTION)
    
    # Select order status
    status = weighted_choice(ORDER_STATUS_DISTRIBUTION)
    
    # Select items
    items = select_order_items(menu_items)
    
    # Calculate totals
    subtotal, tax, total = calculate_order_total(items)
    
    # Generate timestamps based on status
    created_at = generate_order_timestamp(order_date)
    
    # Completion time depends on status
    completed_at = None
    if status == "completed":
        # Orders take 15-45 minutes to complete
        completion_minutes = random.randint(15, 45)
        completed_at = created_at + timedelta(minutes=completion_minutes)
    
    # Generate table number for dine-in orders
    table_number = None
    if order_type == "dine_in":
        table_number = random.randint(1, 30)
    
    # Generate delivery address for delivery orders
    delivery_address = None
    if order_type == "delivery":
        delivery_address = fake.address().replace("\n", ", ")
    
    # Build order record
    order = {
        "order_id": order_id,
        "customer_id": customer_id,
        "order_type": order_type,
        "status": status,
        "table_number": table_number,
        "delivery_address": delivery_address,
        "subtotal": subtotal,
        "tax": tax,
        "total": total,
        "payment_method": random.choice(["credit_card", "debit_card", "cash", "mobile_payment"]),
        "created_at": created_at.isoformat(),
        "completed_at": completed_at.isoformat() if completed_at else None,
        "server_id": None,  # Will be populated when staff is generated
        "notes": fake.sentence(nb_words=6) if random.random() < 0.15 else None,
    }
    
    # Build order items with order_id reference
    order_items = []
    item_counter = 1
    for item in items:
        order_item = {
            "order_item_id": f"{order_id}-{item_counter:03d}",
            "order_id": order_id,
            "item_id": item["item_id"],
            "item_name": item["item_name"],
            "quantity": item["quantity"],
            "unit_price": item["unit_price"],
            "line_total": round(item["quantity"] * item["unit_price"], 2),
            "special_requests": item["special_requests"],
        }
        order_items.append(order_item)
        item_counter += 1
    
    return order, order_items


def generate_orders(
    customers: List[Dict[str, Any]],
    menu_items: List[Dict[str, Any]],
    count: int = None
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Generate multiple orders with line items.
    
    Args:
        customers: List of customers
        menu_items: List of menu items
        count: Number of orders to generate
        
    Returns:
        Tuple of (orders, order_items) lists
    """
    if count is None:
        count = EntityCounts.orders
    
    orders = []
    all_order_items = []
    used_order_ids = set()
    
    # Generate orders over the past year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)
    
    # Calculate orders per day (roughly even distribution with some variance)
    days = (end_date - start_date).days
    orders_per_day = count / days
    
    current_date = start_date
    orders_generated = 0
    
    while orders_generated < count and current_date <= end_date:
        # Vary orders per day (weekends busier)
        day_of_week = current_date.weekday()
        if day_of_week >= 5:  # Weekend
            daily_orders = int(orders_per_day * random.uniform(1.3, 1.8))
        else:  # Weekday
            daily_orders = int(orders_per_day * random.uniform(0.8, 1.2))
        
        # Generate orders for this day
        for _ in range(min(daily_orders, count - orders_generated)):
            # Generate unique order ID
            order_id = f"ORD-{generate_short_id(length=7)}"
            while order_id in used_order_ids:
                order_id = f"ORD-{generate_short_id(length=7)}"
            used_order_ids.add(order_id)
            
            order, order_items = generate_order(order_id, customers, menu_items, current_date)
            orders.append(order)
            all_order_items.extend(order_items)
            orders_generated += 1
        
        current_date += timedelta(days=1)
    
    return orders, all_order_items


def main(
    customers: List[Dict[str, Any]], 
    menu_items: List[Dict[str, Any]], 
    output_dir: str = "output"
) -> Tuple[List[Dict], List[Dict]]:
    """
    Main function to generate and save order data.
    
    Args:
        customers: List of customers (for references)
        menu_items: List of menu items (for references)
        output_dir: Directory to save output files
        
    Returns:
        Tuple of (orders, order_items) lists
    """
    print("\n🧾 Generating order data...")
    
    orders, order_items = generate_orders(customers, menu_items)
    
    # Save to files
    write_json(orders, "orders.json", output_dir)
    write_csv(orders, "orders.csv", output_dir)
    write_json(order_items, "order_items.json", output_dir)
    write_csv(order_items, "order_items.csv", output_dir)
    
    # Print summary stats
    print(f"  📊 Generated {len(orders)} orders with {len(order_items)} line items")
    
    # Order type breakdown
    type_counts = {}
    for order in orders:
        order_type = order["order_type"]
        type_counts[order_type] = type_counts.get(order_type, 0) + 1
    
    print("  📊 Order types:")
    for order_type, count in sorted(type_counts.items()):
        pct = (count / len(orders)) * 100
        print(f"     {order_type}: {count} ({pct:.1f}%)")
    
    # Status breakdown
    status_counts = {}
    for order in orders:
        status = order["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("  📊 Order status:")
    for status, count in sorted(status_counts.items()):
        pct = (count / len(orders)) * 100
        print(f"     {status}: {count} ({pct:.1f}%)")
    
    # Revenue stats
    total_revenue = sum(order["total"] for order in orders if order["status"] == "completed")
    avg_order = total_revenue / status_counts.get("completed", 1)
    print(f"  📊 Total revenue (completed orders): ${total_revenue:,.2f}")
    print(f"  📊 Average order value: ${avg_order:.2f}")
    
    return orders, order_items


if __name__ == "__main__":
    # This module requires customers and menu_items to be generated first
    print("This module requires customers and menu_items data.")
    print("Run generate_all.py instead.")
