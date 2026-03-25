"""
Staff data generator for restaurant sample data.

Generates realistic staff records including:
- Various restaurant roles
- Hire dates and tenure
- Compensation data
- Contact information
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from faker import Faker

from config import FAKER_SEED, EntityCounts, STAFF_ROLES
from utils import generate_short_id, write_json, write_csv

# Initialize Faker with fixed seed
fake = Faker()
Faker.seed(FAKER_SEED)
random.seed(FAKER_SEED)


def generate_staff_member(
    staff_id: str,
    role: str,
    role_config: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Generate a single staff member record.
    
    Args:
        staff_id: Unique identifier
        role: Job role/title
        role_config: Configuration with hourly_rate range
        
    Returns:
        Dictionary containing staff data
    """
    first_name = fake.first_name()
    last_name = fake.last_name()
    
    # Generate hire date (weighted towards more recent hires)
    hire_date = fake.date_between(start_date="-10y", end_date="-1m")
    
    # Calculate tenure
    tenure_days = (datetime.now().date() - hire_date).days
    tenure_years = round(tenure_days / 365, 1)
    
    # Hourly rate based on role and tenure
    rate_min, rate_max = role_config["hourly_rate"]
    tenure_bonus = min(tenure_years * 0.5, 3.0)  # Up to $3/hr for tenure
    base_rate = random.uniform(rate_min, rate_max)
    hourly_rate = round(base_rate + tenure_bonus, 2)
    
    # Work schedule
    employment_type = "full_time" if random.random() < 0.70 else "part_time"
    
    # Generate weekly hours based on employment type
    if employment_type == "full_time":
        weekly_hours = random.randint(35, 45)
    else:
        weekly_hours = random.randint(15, 30)
    
    return {
        "staff_id": staff_id,
        "first_name": first_name,
        "last_name": last_name,
        "email": f"{first_name.lower()}.{last_name.lower()}@restaurant.com",
        "phone": fake.phone_number(),
        "role": role,
        "department": get_department_for_role(role),
        "hourly_rate": hourly_rate,
        "employment_type": employment_type,
        "weekly_hours": weekly_hours,
        "hire_date": hire_date.isoformat(),
        "tenure_years": tenure_years,
        "is_active": True,
        "emergency_contact": fake.name(),
        "emergency_phone": fake.phone_number(),
        "address": fake.address().replace("\n", ", "),
        "date_of_birth": fake.date_of_birth(minimum_age=18, maximum_age=65).isoformat(),
    }


def get_department_for_role(role: str) -> str:
    """Map role to department."""
    if "Chef" in role or "Cook" in role:
        return "Kitchen"
    elif "Server" in role or "Host" in role:
        return "Front of House"
    elif "Bartender" in role:
        return "Bar"
    elif "Manager" in role:
        return "Management"
    else:
        return "Operations"


def generate_staff(count: int = None) -> List[Dict[str, Any]]:
    """
    Generate staff records based on role configuration.
    
    Args:
        count: Override count (uses STAFF_ROLES config if None)
        
    Returns:
        List of staff dictionaries
    """
    if count is None:
        count = EntityCounts.staff
    
    staff = []
    used_ids = set()
    
    # Generate staff for each role based on count
    for role, role_config in STAFF_ROLES.items():
        role_count = role_config["count"]
        
        for _ in range(role_count):
            staff_id = f"EMP-{generate_short_id(length=5)}"
            while staff_id in used_ids:
                staff_id = f"EMP-{generate_short_id(length=5)}"
            used_ids.add(staff_id)
            
            staff_member = generate_staff_member(staff_id, role, role_config)
            staff.append(staff_member)
    
    return staff


def main(output_dir: str = "output") -> List[Dict[str, Any]]:
    """
    Main function to generate and save staff data.
    
    Args:
        output_dir: Directory to save output files
        
    Returns:
        List of generated staff records
    """
    print("\n👨‍🍳 Generating staff data...")
    
    staff = generate_staff()
    
    # Save to files
    write_json(staff, "staff.json", output_dir)
    write_csv(staff, "staff.csv", output_dir)
    
    # Print summary stats
    print(f"  📊 Generated {len(staff)} staff members")
    
    # Role breakdown
    role_counts = {}
    for member in staff:
        role = member["role"]
        role_counts[role] = role_counts.get(role, 0) + 1
    
    print("  📊 Staff by role:")
    for role, count in sorted(role_counts.items()):
        print(f"     {role}: {count}")
    
    # Department breakdown
    dept_counts = {}
    for member in staff:
        dept = member["department"]
        dept_counts[dept] = dept_counts.get(dept, 0) + 1
    
    print("  📊 Staff by department:")
    for dept, count in sorted(dept_counts.items()):
        print(f"     {dept}: {count}")
    
    # Average tenure
    avg_tenure = sum(m["tenure_years"] for m in staff) / len(staff)
    print(f"  📊 Average tenure: {avg_tenure:.1f} years")
    
    # Payroll stats
    total_hourly = sum(m["hourly_rate"] * m["weekly_hours"] for m in staff)
    weekly_payroll = total_hourly
    annual_payroll = weekly_payroll * 52
    print(f"  📊 Weekly payroll: ${weekly_payroll:,.2f}")
    print(f"  📊 Annual payroll: ${annual_payroll:,.2f}")
    
    return staff


if __name__ == "__main__":
    main()
