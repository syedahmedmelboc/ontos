"""
Master script to generate all restaurant sample data.

This script orchestrates the generation of all entities in the correct
dependency order:
1. Customers (no dependencies)
2. Menu Categories and Items (no dependencies)
3. Orders and Order Items (depends on customers, menu items)
4. Reservations (depends on customers)
5. Suppliers and Inventory (no dependencies)
6. Staff (no dependencies)
7. Reviews (depends on customers, orders)

All data is generated with referential integrity and realistic distributions.
"""

import time
import os
import sys
from datetime import datetime
from typing import Dict, Any, List

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import FAKER_SEED, EntityCounts
from utils import write_summary, print_summary, validate_referential_integrity

# Import generators
from customers import generate_customers, update_customer_stats
from menu_items import generate_menu
from orders import generate_orders
from reservations import generate_reservations
from inventory import generate_inventory
from staff import generate_staff
from reviews import generate_reviews


def main(output_dir: str = "output") -> Dict[str, Any]:
    """
    Generate all restaurant sample data.
    
    Args:
        output_dir: Directory to save output files
        
    Returns:
        Summary dictionary with generation statistics
    """
    start_time = time.time()
    
    print("\n" + "=" * 60)
    print("🍽️  RESTAURANT SAMPLE DATA GENERATOR")
    print("=" * 60)
    print(f"Output directory: {output_dir}")
    print(f"Faker seed: {FAKER_SEED}")
    print("=" * 60)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    summary = {
        "seed": FAKER_SEED,
        "generated_at": datetime.now().isoformat(),
        "entities": {},
        "files": [],
        "validation": None,
        "generation_time_seconds": 0,
    }
    
    # ============================================
    # 1. Generate Customers (no dependencies)
    # ============================================
    print("\n👥 [1/7] Generating customers...")
    customers = generate_customers()
    summary["entities"]["customers"] = len(customers)
    summary["files"].extend(["customers.json", "customers.csv"])
    
    # ============================================
    # 2. Generate Menu (no dependencies)
    # ============================================
    print("\n🍽️  [2/7] Generating menu categories and items...")
    categories, menu_items = generate_menu()
    summary["entities"]["menu_categories"] = len(categories)
    summary["entities"]["menu_items"] = len(menu_items)
    summary["files"].extend(["menu_categories.json", "menu_categories.csv", 
                             "menu_items.json", "menu_items.csv"])
    
    # ============================================
    # 3. Generate Orders (depends on customers, menu_items)
    # ============================================
    print("\n🧾 [3/7] Generating orders and order items...")
    orders, order_items = generate_orders(customers, menu_items)
    summary["entities"]["orders"] = len(orders)
    summary["entities"]["order_items"] = len(order_items)
    summary["files"].extend(["orders.json", "orders.csv", 
                             "order_items.json", "order_items.csv"])
    
    # ============================================
    # 4. Generate Reservations (depends on customers)
    # ============================================
    print("\n📅 [4/7] Generating reservations...")
    reservations = generate_reservations(customers)
    summary["entities"]["reservations"] = len(reservations)
    summary["files"].extend(["reservations.json", "reservations.csv"])
    
    # ============================================
    # 5. Generate Inventory and Suppliers (no dependencies)
    # ============================================
    print("\n📦 [5/7] Generating inventory and suppliers...")
    suppliers, inventory_items = generate_inventory()
    summary["entities"]["suppliers"] = len(suppliers)
    summary["entities"]["inventory_items"] = len(inventory_items)
    summary["files"].extend(["suppliers.json", "suppliers.csv",
                             "inventory.json", "inventory.csv"])
    
    # ============================================
    # 6. Generate Staff (no dependencies)
    # ============================================
    print("\n👨‍🍳 [6/7] Generating staff...")
    staff = generate_staff()
    summary["entities"]["staff"] = len(staff)
    summary["files"].extend(["staff.json", "staff.csv"])
    
    # ============================================
    # 7. Generate Reviews (depends on customers, orders)
    # ============================================
    print("\n⭐ [7/7] Generating reviews...")
    reviews = generate_reviews(customers, orders)
    summary["entities"]["reviews"] = len(reviews)
    summary["files"].extend(["reviews.json", "reviews.csv"])
    
    # ============================================
    # Post-generation: Update customer stats
    # ============================================
    print("\n🔄 Updating customer statistics from orders...")
    customers = update_customer_stats(customers, orders)
    
    # Re-save customers with updated stats
    from utils import write_json, write_csv
    write_json(customers, "customers.json", output_dir)
    write_csv(customers, "customers.csv", output_dir)
    
    # ============================================
    # Validation
    # ============================================
    print("\n✅ Validating referential integrity...")
    validation = validate_referential_integrity(orders, customers, menu_items)
    summary["validation"] = validation
    
    if validation["valid"]:
        print(f"  ✓ All {validation['total_checks']} references validated successfully")
    else:
        print(f"  ⚠️  Found {len(validation['issues'])} issues:")
        for issue in validation["issues"][:5]:  # Show first 5
            print(f"    - {issue}")
        if len(validation["issues"]) > 5:
            print(f"    ... and {len(validation['issues']) - 5} more")
    
    # ============================================
    # Finalize
    # ============================================
    end_time = time.time()
    summary["generation_time_seconds"] = round(end_time - start_time, 2)
    
    # Write summary
    write_summary(summary, output_dir)
    
    # Print summary
    print_summary(summary)
    
    # Print additional stats
    print("\n📊 ADDITIONAL STATISTICS:")
    print("-" * 40)
    
    # Revenue stats
    completed_orders = [o for o in orders if o["status"] == "completed"]
    total_revenue = sum(o["total"] for o in completed_orders)
    print(f"Total Revenue (completed orders): ${total_revenue:,.2f}")
    print(f"Average Order Value: ${total_revenue / len(completed_orders):.2f}")
    
    # Customer stats
    customers_with_orders = sum(1 for c in customers if c["total_orders"] > 0)
    print(f"Customers with orders: {customers_with_orders} ({customers_with_orders/len(customers)*100:.1f}%)")
    
    # Inventory stats
    total_inventory_value = sum(i["total_value"] for i in inventory_items)
    print(f"Total Inventory Value: ${total_inventory_value:,.2f}")
    
    # Staff stats
    annual_payroll = sum(s["hourly_rate"] * s["weekly_hours"] * 52 for s in staff)
    print(f"Annual Payroll: ${annual_payroll:,.2f}")
    
    # Review stats
    avg_rating = sum(r["rating"] for r in reviews) / len(reviews)
    print(f"Average Review Rating: {avg_rating:.2f}/5")
    
    print("\n✨ Generation complete!")
    print(f"📁 All files saved to: {os.path.abspath(output_dir)}")
    
    return summary


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate restaurant sample data for Ontos tutorial"
    )
    parser.add_argument(
        "-o", "--output",
        default="output",
        help="Output directory for generated files (default: output)"
    )
    
    args = parser.parse_args()
    
    main(output_dir=args.output)
