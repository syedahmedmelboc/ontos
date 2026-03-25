"""
Reservation data generator for restaurant sample data.

Generates realistic reservation data including:
- Customer references
- Party sizes
- Reservation times (evening bias)
- Status distribution (completed, no-show, cancelled)
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from faker import Faker

from config import FAKER_SEED, EntityCounts, RESERVATION_STATUS_DISTRIBUTION
from utils import (
    generate_short_id,
    weighted_choice,
    generate_reservation_datetime,
    write_json,
    write_csv
)

# Initialize Faker with fixed seed
fake = Faker()
Faker.seed(FAKER_SEED)
random.seed(FAKER_SEED)


def generate_reservation(
    reservation_id: str,
    customers: List[Dict[str, Any]],
    reservation_date: datetime
) -> Dict[str, Any]:
    """
    Generate a single reservation record.
    
    Args:
        reservation_id: Unique identifier for the reservation
        customers: List of customers to select from
        reservation_date: Date of the reservation
        
    Returns:
        Dictionary containing reservation data
    """
    # Select customer (70% of reservations have registered customer)
    if random.random() < 0.70 and customers:
        customer = random.choice(customers)
        customer_id = customer["customer_id"]
        contact_name = f"{customer['first_name']} {customer['last_name']}"
        contact_phone = customer["phone"]
    else:
        customer_id = None
        contact_name = fake.name()
        contact_phone = fake.phone_number()
    
    # Generate reservation datetime
    reservation_datetime = generate_reservation_datetime(reservation_date)
    
    # Select party size (weighted towards 2-4)
    party_size_dist = {
        1: 0.05,   # Solo diners
        2: 0.35,   # Couples
        3: 0.15,   # Small groups
        4: 0.25,   # Families/small parties
        5: 0.08,   # Medium groups
        6: 0.06,   # Larger groups
        7: 0.03,   # Big groups
        8: 0.02,   # Large parties
        9: 0.01,   # Very large
        10: 0.005, # Special events
        11: 0.002,
        12: 0.003,
    }
    party_size = weighted_choice(party_size_dist)
    
    # Select status based on whether reservation is in past or future
    if reservation_date.date() > datetime.now().date():
        status = "confirmed"
    else:
        status = weighted_choice(RESERVATION_STATUS_DISTRIBUTION)
    
    # Generate special requests
    special_requests = None
    if random.random() < 0.25:
        requests = [
            "High chair needed",
            "Wheelchair accessible table",
            "Quiet corner table",
            "Window seat preferred",
            "Booth if available",
            "Birthday celebration",
            "Anniversary dinner",
            "Business meeting",
            "Romantic setting",
            "Gluten-free menu needed",
            "Child-friendly area",
            "Private dining room",
        ]
        special_requests = random.choice(requests)
    
    # Assign table based on party size (if completed)
    table_number = None
    if status == "completed":
        # Tables 1-10 are for 2-4 people, 11-20 for 4-6, 21-30 for 6+
        if party_size <= 2:
            table_number = random.randint(1, 10)
        elif party_size <= 4:
            table_number = random.randint(1, 20)
        else:
            table_number = random.randint(11, 30)
    
    # Created timestamp (reservation made 1-14 days in advance)
    days_in_advance = random.randint(1, 14)
    created_at = reservation_datetime - timedelta(days=days_in_advance)
    created_at = created_at.replace(
        hour=random.randint(9, 20),
        minute=random.randint(0, 59)
    )
    
    return {
        "reservation_id": reservation_id,
        "customer_id": customer_id,
        "contact_name": contact_name,
        "contact_phone": contact_phone,
        "party_size": party_size,
        "reservation_datetime": reservation_datetime.isoformat(),
        "table_number": table_number,
        "status": status,
        "special_requests": special_requests,
        "created_at": created_at.isoformat(),
        "updated_at": created_at.isoformat() if status == "confirmed" else reservation_datetime.isoformat(),
    }


def generate_reservations(
    customers: List[Dict[str, Any]],
    count: int = None
) -> List[Dict[str, Any]]:
    """
    Generate multiple reservations.
    
    Args:
        customers: List of customers
        count: Number of reservations to generate
        
    Returns:
        List of reservation dictionaries
    """
    if count is None:
        count = EntityCounts.reservations
    
    reservations = []
    used_ids = set()
    
    # Generate reservations over the past year and some future ones
    end_date = datetime.now() + timedelta(days=30)  # Include future reservations
    start_date = end_date - timedelta(days=365 + 30)
    
    # Calculate reservations per day
    days = (end_date - start_date).days
    reservations_per_day = count / days
    
    current_date = start_date
    reservations_generated = 0
    
    while reservations_generated < count and current_date <= end_date:
        # Vary reservations per day (weekends busier)
        day_of_week = current_date.weekday()
        if day_of_week >= 5:  # Weekend
            daily_reservations = int(reservations_per_day * random.uniform(1.4, 2.0))
        else:  # Weekday
            daily_reservations = int(reservations_per_day * random.uniform(0.7, 1.1))
        
        # Only generate for dinner service (most common for reservations)
        if random.random() < 0.85:  # 85% are dinner reservations
            for _ in range(min(daily_reservations, count - reservations_generated)):
                reservation_id = f"RES-{generate_short_id(length=6)}"
                while reservation_id in used_ids:
                    reservation_id = f"RES-{generate_short_id(length=6)}"
                used_ids.add(reservation_id)
                
                reservation = generate_reservation(reservation_id, customers, current_date)
                reservations.append(reservation)
                reservations_generated += 1
        
        current_date += timedelta(days=1)
    
    return reservations


def main(
    customers: List[Dict[str, Any]], 
    output_dir: str = "output"
) -> List[Dict[str, Any]]:
    """
    Main function to generate and save reservation data.
    
    Args:
        customers: List of customers
        output_dir: Directory to save output files
        
    Returns:
        List of generated reservations
    """
    print("\n📅 Generating reservation data...")
    
    reservations = generate_reservations(customers)
    
    # Save to files
    write_json(reservations, "reservations.json", output_dir)
    write_csv(reservations, "reservations.csv", output_dir)
    
    # Print summary stats
    print(f"  📊 Generated {len(reservations)} reservations")
    
    # Status breakdown
    status_counts = {}
    for res in reservations:
        status = res["status"]
        status_counts[status] = status_counts.get(status, 0) + 1
    
    print("  📊 Reservation status:")
    for status, count in sorted(status_counts.items()):
        pct = (count / len(reservations)) * 100
        print(f"     {status}: {count} ({pct:.1f}%)")
    
    # Party size stats
    avg_party = sum(r["party_size"] for r in reservations) / len(reservations)
    print(f"  📊 Average party size: {avg_party:.1f}")
    
    return reservations


if __name__ == "__main__":
    print("This module requires customers data.")
    print("Run generate_all.py instead.")
