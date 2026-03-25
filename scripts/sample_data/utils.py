"""
Utility functions for restaurant sample data generation.

This module provides helper functions for generating consistent,
realistic restaurant business data.
"""

import uuid
import random
import json
import csv
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional, Tuple

from faker import Faker

# Import configuration
from config import FAKER_SEED, EntityCounts, LOYALTY_DISTRIBUTION

# Initialize Faker with fixed seed for reproducibility
fake = Faker()
Faker.seed(FAKER_SEED)
random.seed(FAKER_SEED)


def generate_uuid() -> str:
    """Generate a deterministic UUID string."""
    return str(uuid.uuid4())


def generate_short_id(prefix: str = "", length: int = 8) -> str:
    """Generate a short alphanumeric ID with optional prefix."""
    chars = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"  # Remove ambiguous characters
    suffix = "".join(random.choices(chars, k=length))
    return f"{prefix}{suffix}" if prefix else suffix


def weighted_choice(distribution: Dict[str, float]) -> str:
    """Select a key from a dictionary based on weighted probabilities."""
    choices = list(distribution.keys())
    weights = list(distribution.values())
    return random.choices(choices, weights=weights, k=1)[0]


def weighted_choice_int(distribution: Dict[int, float]) -> int:
    """Select an integer key from a dictionary based on weighted probabilities."""
    choices = list(distribution.keys())
    weights = list(distribution.values())
    return random.choices(choices, weights=weights, k=1)[0]


def random_date_range(
    start_date: datetime, 
    end_date: datetime, 
    weighted_towards_recent: bool = False
) -> datetime:
    """
    Generate a random datetime within a range.
    
    Args:
        start_date: Start of the date range
        end_date: End of the date range
        weighted_towards_recent: If True, bias towards more recent dates
        
    Returns:
        A random datetime within the specified range
    """
    delta = end_date - start_date
    if weighted_towards_recent:
        # Use exponential distribution to bias towards recent dates
        random_days = random.expovariate(3 / delta.days)  # Lambda for ~33% recency bias
        random_days = min(random_days, delta.days)
    else:
        random_days = random.uniform(0, delta.days)
    
    return start_date + timedelta(days=random_days)


def generate_order_timestamp(base_date: datetime) -> datetime:
    """
    Generate a realistic order timestamp with lunch/d dinner rush patterns.
    
    Restaurant orders follow time-of-day patterns:
    - Lunch rush: 11:30 - 14:00
    - Dinner rush: 17:30 - 21:00
    - Bar/late night: 21:00 - 23:00
    - Other times: lower volume
    """
    # Define time slots with their probability weights
    time_slots = [
        (11.5, 14.0, 0.30),   # Lunch rush - 30% of orders
        (17.5, 21.0, 0.40),   # Dinner rush - 40% of orders
        (21.0, 23.0, 0.15),   # Late night - 15% of orders
        (8.0, 11.5, 0.08),    # Morning - 8% of orders
        (14.0, 17.5, 0.05),   # Afternoon - 5% of orders
        (23.0, 24.0, 0.02),   # Very late - 2% of orders
    ]
    
    # Select a time slot based on weights
    slot = random.choices(time_slots, weights=[s[2] for s in time_slots], k=1)[0]
    
    # Generate random time within the slot
    hour = random.uniform(slot[0], slot[1])
    
    # Create the timestamp
    order_time = base_date.replace(
        hour=int(hour),
        minute=int((hour % 1) * 60),
        second=random.randint(0, 59)
    )
    
    return order_time


def generate_reservation_datetime(base_date: datetime) -> datetime:
    """
    Generate a realistic reservation datetime.
    
    Reservations are typically for:
    - Dinner: 18:00 - 21:00 (70%)
    - Lunch: 12:00 - 14:00 (25%)
    - Weekend brunch: 10:00 - 13:00 (5%)
    """
    if random.random() < 0.70:
        # Dinner reservation
        hour = random.randint(18, 20)
        minute = random.choice([0, 15, 30, 45])
    elif random.random() < 0.95:
        # Lunch reservation
        hour = random.randint(12, 13)
        minute = random.choice([0, 15, 30, 45])
    else:
        # Brunch reservation
        hour = random.randint(10, 12)
        minute = random.choice([0, 15, 30, 45])
    
    return base_date.replace(hour=hour, minute=minute, second=0)


def format_currency(amount: float) -> str:
    """Format a float as currency string."""
    return f"${amount:.2f}"


def calculate_order_total(items: List[Dict[str, Any]]) -> Tuple[float, float, float]:
    """
    Calculate order subtotal, tax, and total.
    
    Args:
        items: List of order items with 'quantity' and 'unit_price'
        
    Returns:
        Tuple of (subtotal, tax, total)
    """
    subtotal = sum(item["quantity"] * item["unit_price"] for item in items)
    tax_rate = 0.08875  # Example tax rate (8.875%)
    tax = round(subtotal * tax_rate, 2)
    total = round(subtotal + tax, 2)
    return subtotal, tax, total


def write_json(data: List[Dict[str, Any]], filename: str, output_dir: str = "output"):
    """Write data to a JSON file."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, default=json_serializer, ensure_ascii=False)
    print(f"  ✓ Written {len(data)} records to {filepath}")


def json_serializer(obj):
    """Custom JSON serializer for datetime objects."""
    if isinstance(obj, (datetime,)):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def write_csv(data: List[Dict[str, Any]], filename: str, output_dir: str = "output"):
    """Write data to a CSV file."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)
    
    if not data:
        print(f"  ⚠ No data to write to {filepath}")
        return
    
    # Flatten nested structures for CSV
    flat_data = []
    for record in data:
        flat_record = {}
        for key, value in record.items():
            if isinstance(value, (list, dict)):
                flat_record[key] = json.dumps(value) if value else ""
            elif isinstance(value, datetime):
                flat_record[key] = value.isoformat()
            else:
                flat_record[key] = value
        flat_data.append(flat_record)
    
    # Get field names from the first record
    fieldnames = list(flat_data[0].keys())
    
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(flat_data)
    
    print(f"  ✓ Written {len(data)} records to {filepath}")


def write_summary(summary: Dict[str, Any], output_dir: str = "output"):
    """Write generation summary to JSON file."""
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, "summary.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2, default=str)
    print(f"\n📊 Summary written to {filepath}")


def print_summary(summary: Dict[str, Any]):
    """Print a formatted summary of generated data."""
    print("\n" + "=" * 60)
    print("📊 RESTAURANT SAMPLE DATA GENERATION SUMMARY")
    print("=" * 60)
    
    for entity, count in summary.get("entities", {}).items():
        print(f"  {entity.replace('_', ' ').title():.<30} {count:>8,} records")
    
    print("\n📁 Output Files:")
    for filename in summary.get("files", []):
        print(f"    • {filename}")
    
    print(f"\n⏱️  Generation Time: {summary.get('generation_time_seconds', 0):.2f}s")
    print(f"🌱 Faker Seed: {summary.get('seed', 'N/A')}")
    print("=" * 60 + "\n")


def validate_referential_integrity(
    orders: List[Dict], 
    customers: List[Dict], 
    menu_items: List[Dict]
) -> Dict[str, Any]:
    """
    Validate that all foreign key references are valid.
    
    Returns a dict with validation results.
    """
    customer_ids = {c["customer_id"] for c in customers}
    menu_item_ids = {m["item_id"] for m in menu_items}
    
    issues = []
    
    # Check order customer references
    for order in orders:
        if order.get("customer_id") and order["customer_id"] not in customer_ids:
            issues.append(f"Order {order['order_id']} references non-existent customer {order['customer_id']}")
    
    # Check order item menu references
    for order in orders:
        for item in order.get("items", []):
            if item.get("item_id") and item["item_id"] not in menu_item_ids:
                issues.append(f"Order {order['order_id']} references non-existent menu item {item['item_id']}")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "total_checks": len(orders) + sum(len(o.get("items", [])) for o in orders)
    }
