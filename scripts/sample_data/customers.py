"""
Customer data generator for restaurant sample data.

Generates realistic customer profiles including:
- Personal information (name, email, phone)
- Loyalty program membership
- Registration dates
- Order statistics (placeholder for linking)
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from faker import Faker

from config import FAKER_SEED, EntityCounts, LOYALTY_DISTRIBUTION
from utils import (
    generate_short_id, 
    weighted_choice, 
    random_date_range,
    write_json, 
    write_csv
)

# Initialize Faker with fixed seed
fake = Faker()
Faker.seed(FAKER_SEED)
random.seed(FAKER_SEED)


def generate_customer(customer_id: str, registration_start: datetime, registration_end: datetime) -> Dict[str, Any]:
    """
    Generate a single customer record.
    
    Args:
        customer_id: Unique identifier for the customer
        registration_start: Earliest possible registration date
        registration_end: Latest possible registration date
        
    Returns:
        Dictionary containing customer data
    """
    # Generate personal information
    first_name = fake.first_name()
    last_name = fake.last_name()
    
    # Generate email (sometimes uses name, sometimes random)
    if random.random() < 0.7:
        email_base = f"{first_name.lower()}.{last_name.lower()}"
        email_domain = random.choice(["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "icloud.com"])
        email = f"{email_base}@{email_domain}"
        # Handle duplicates by adding numbers
        if random.random() < 0.3:
            email = f"{email_base}{random.randint(1, 999)}@{email_domain}"
    else:
        email = fake.email()
    
    # Generate phone number (US format)
    phone = fake.phone_number()
    
    # Assign loyalty tier based on distribution
    loyalty_tier = weighted_choice(LOYALTY_DISTRIBUTION)
    
    # Generate registration date (weighted towards recent)
    registration_date = random_date_range(
        registration_start, 
        registration_end, 
        weighted_towards_recent=True
    )
    
    return {
        "customer_id": customer_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "loyalty_tier": loyalty_tier,
        "registration_date": registration_date.strftime("%Y-%m-%d"),
        # These will be populated when orders are generated
        "total_orders": 0,
        "total_spent": 0.0,
        "last_order_date": None,
        "preferred_order_type": None,
    }


def generate_customers(count: int = None) -> List[Dict[str, Any]]:
    """
    Generate a list of customer records.
    
    Args:
        count: Number of customers to generate (default from config)
        
    Returns:
        List of customer dictionaries
    """
    if count is None:
        count = EntityCounts.customers
    
    # Registration dates: past 3 years
    registration_end = datetime.now()
    registration_start = registration_end - timedelta(days=3 * 365)
    
    customers = []
    used_ids = set()
    
    for i in range(count):
        # Generate unique customer ID
        customer_id = f"CUST-{generate_short_id(length=6)}"
        while customer_id in used_ids:
            customer_id = f"CUST-{generate_short_id(length=6)}"
        used_ids.add(customer_id)
        
        customer = generate_customer(customer_id, registration_start, registration_end)
        customers.append(customer)
    
    return customers


def update_customer_stats(customers: List[Dict], orders: List[Dict]) -> List[Dict]:
    """
    Update customer statistics based on order data.
    
    This function should be called after orders are generated to
    populate order counts, totals, and preferences.
    
    Args:
        customers: List of customer records
        orders: List of order records
        
    Returns:
        Updated list of customers
    """
    # Create customer lookup
    customer_map = {c["customer_id"]: c for c in customers}
    
    # Initialize stats
    for customer in customers:
        customer["total_orders"] = 0
        customer["total_spent"] = 0.0
        customer["last_order_date"] = None
        customer["preferred_order_type"] = None
        customer["order_types"] = {"dine_in": 0, "takeout": 0, "delivery": 0}
    
    # Aggregate order data
    for order in orders:
        customer_id = order.get("customer_id")
        if customer_id and customer_id in customer_map:
            customer = customer_map[customer_id]
            customer["total_orders"] += 1
            customer["total_spent"] += order.get("total", 0)
            customer["order_types"][order.get("order_type", "dine_in")] += 1
            
            order_date = order.get("created_at")
            if order_date:
                if customer["last_order_date"] is None or order_date > customer["last_order_date"]:
                    customer["last_order_date"] = order_date
    
    # Determine preferred order type and clean up
    for customer in customers:
        if customer["total_orders"] > 0:
            order_types = customer.pop("order_types")
            customer["preferred_order_type"] = max(order_types, key=order_types.get)
            customer["total_spent"] = round(customer["total_spent"], 2)
        else:
            customer.pop("order_types")
            customer["preferred_order_type"] = None
    
    return customers


def main(output_dir: str = "output") -> List[Dict[str, Any]]:
    """
    Main function to generate and save customer data.
    
    Args:
        output_dir: Directory to save output files
        
    Returns:
        List of generated customer records
    """
    print("\n👥 Generating customer data...")
    
    customers = generate_customers()
    
    # Save to files
    write_json(customers, "customers.json", output_dir)
    write_csv(customers, "customers.csv", output_dir)
    
    # Print summary stats
    loyalty_counts = {}
    for c in customers:
        tier = c["loyalty_tier"]
        loyalty_counts[tier] = loyalty_counts.get(tier, 0) + 1
    
    print(f"  📊 Loyalty distribution:")
    for tier in ["Bronze", "Silver", "Gold", "Platinum"]:
        count = loyalty_counts.get(tier, 0)
        pct = (count / len(customers)) * 100
        print(f"     {tier}: {count} ({pct:.1f}%)")
    
    return customers


if __name__ == "__main__":
    main()
