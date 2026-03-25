"""
Load restaurant sample data into Databricks Unity Catalog.

This script:
1. Creates the target schema (catalog.schema) if it doesn't exist
2. Creates Delta tables with proper schema
3. Loads data from JSON files into the tables
4. Sets up table properties and comments

Usage:
    python load_to_databricks.py --catalog main --schema restaurant --output-dir output

Prerequisites:
    - Databricks SDK installed (databricks-sdk)
    - Databricks CLI configured with profile
    - Unity Catalog enabled in workspace
"""

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

try:
    from databricks.sdk import WorkspaceClient
    from databricks.sdk.errors import NotFound
except ImportError:
    print("Error: databricks-sdk not installed.")
    print("Install with: pip install databricks-sdk")
    sys.exit(1)


# Table schemas with Databricks SQL types
TABLE_SCHEMAS = {
    "customers": {
        "columns": [
            ("customer_id", "STRING NOT NULL", "Unique customer identifier (CUST-XXXXXX)"),
            ("first_name", "STRING NOT NULL", "Customer first name"),
            ("last_name", "STRING NOT NULL", "Customer last name"),
            ("email", "STRING NOT NULL", "Customer email address (PII)"),
            ("phone", "STRING", "Customer phone number (PII)"),
            ("loyalty_tier", "STRING NOT NULL", "Loyalty tier: Bronze, Silver, Gold, Platinum"),
            ("registration_date", "DATE NOT NULL", "Date customer registered"),
            ("total_orders", "INT NOT NULL DEFAULT 0", "Total number of orders"),
            ("total_spent", "DECIMAL(10,2) NOT NULL DEFAULT 0.00", "Total lifetime spend"),
            ("last_order_date", "TIMESTAMP", "Timestamp of most recent order"),
            ("preferred_order_type", "STRING", "Preferred order type: dine_in, takeout, delivery"),
        ],
        "primary_key": "customer_id",
        "partition_by": None,
        "comment": "Customer master data with loyalty information and order history metrics.",
    },
    "menu_categories": {
        "columns": [
            ("category_id", "STRING NOT NULL", "Unique category identifier"),
            ("name", "STRING NOT NULL", "Category display name"),
            ("description", "STRING", "Category description"),
            ("sort_order", "INT NOT NULL", "Display order for menu"),
            ("is_active", "BOOLEAN NOT NULL DEFAULT true", "Whether category is active"),
        ],
        "primary_key": "category_id",
        "partition_by": None,
        "comment": "Menu categories for organizing menu items.",
    },
    "menu_items": {
        "columns": [
            ("item_id", "STRING NOT NULL", "Unique item identifier"),
            ("category_id", "STRING NOT NULL", "Foreign key to menu_categories"),
            ("name", "STRING NOT NULL", "Item display name"),
            ("description", "STRING", "Item description"),
            ("price", "DECIMAL(8,2) NOT NULL", "Current selling price"),
            ("cost", "DECIMAL(8,2)", "Cost to prepare"),
            ("preparation_time_minutes", "INT", "Average preparation time"),
            ("is_vegetarian", "BOOLEAN NOT NULL DEFAULT false", "Vegetarian friendly"),
            ("is_vegan", "BOOLEAN NOT NULL DEFAULT false", "Vegan friendly"),
            ("is_gluten_free", "BOOLEAN NOT NULL DEFAULT false", "Gluten free"),
            ("contains_allergens", "ARRAY<STRING>", "List of allergens"),
            ("calories", "INT", "Calorie count"),
            ("is_available", "BOOLEAN NOT NULL DEFAULT true", "Currently available"),
            ("is_featured", "BOOLEAN NOT NULL DEFAULT false", "Featured on menu"),
        ],
        "primary_key": "item_id",
        "partition_by": None,
        "comment": "Menu items with pricing, dietary information, and availability.",
    },
    "orders": {
        "columns": [
            ("order_id", "STRING NOT NULL", "Unique order identifier"),
            ("customer_id", "STRING", "Foreign key to customers (null for guest orders)"),
            ("order_type", "STRING NOT NULL", "Order type: dine_in, takeout, delivery"),
            ("status", "STRING NOT NULL", "Order status: pending, confirmed, preparing, ready, completed, cancelled"),
            ("table_number", "INT", "Table number for dine-in orders"),
            ("subtotal", "DECIMAL(10,2) NOT NULL", "Order subtotal before tax"),
            ("tax", "DECIMAL(10,2) NOT NULL", "Tax amount"),
            ("total", "DECIMAL(10,2) NOT NULL", "Total order amount"),
            ("payment_method", "STRING NOT NULL", "Payment method: credit_card, debit_card, cash, mobile_payment"),
            ("delivery_address", "STRING", "Delivery address for delivery orders"),
            ("special_instructions", "STRING", "Special instructions for the order"),
            ("created_at", "TIMESTAMP NOT NULL", "Order creation timestamp"),
            ("updated_at", "TIMESTAMP", "Last update timestamp"),
            ("completed_at", "TIMESTAMP", "Order completion timestamp"),
        ],
        "primary_key": "order_id",
        "partition_by": None,  # Could partition by date for large volumes
        "comment": "Order headers with transaction details and status tracking.",
    },
    "order_items": {
        "columns": [
            ("order_item_id", "STRING NOT NULL", "Unique order item identifier"),
            ("order_id", "STRING NOT NULL", "Foreign key to orders"),
            ("item_id", "STRING NOT NULL", "Foreign key to menu_items"),
            ("item_name", "STRING NOT NULL", "Item name at time of order"),
            ("quantity", "INT NOT NULL", "Quantity ordered"),
            ("unit_price", "DECIMAL(8,2) NOT NULL", "Price per unit"),
            ("line_total", "DECIMAL(10,2) NOT NULL", "Total for this line item"),
            ("special_requests", "STRING", "Special requests for this item"),
        ],
        "primary_key": "order_item_id",
        "partition_by": None,
        "comment": "Order line items linking orders to menu items.",
    },
    "reservations": {
        "columns": [
            ("reservation_id", "STRING NOT NULL", "Unique reservation identifier"),
            ("customer_id", "STRING", "Foreign key to customers (null for guest reservations)"),
            ("party_size", "INT NOT NULL", "Number of guests"),
            ("reservation_datetime", "TIMESTAMP NOT NULL", "Reservation date and time"),
            ("table_number", "INT", "Assigned table number"),
            ("status", "STRING NOT NULL", "Reservation status: pending, confirmed, completed, cancelled, no_show"),
            ("special_requests", "STRING", "Special requests (dietary, celebration, etc.)"),
            ("contact_phone", "STRING", "Contact phone number"),
            ("created_at", "TIMESTAMP NOT NULL", "Reservation creation timestamp"),
        ],
        "primary_key": "reservation_id",
        "partition_by": None,
        "comment": "Table reservations with party size and status tracking.",
    },
    "suppliers": {
        "columns": [
            ("supplier_id", "STRING NOT NULL", "Unique supplier identifier"),
            ("name", "STRING NOT NULL", "Supplier name"),
            ("contact_name", "STRING", "Primary contact name"),
            ("email", "STRING", "Contact email"),
            ("phone", "STRING", "Contact phone"),
            ("address", "STRING", "Supplier address"),
            ("category", "STRING NOT NULL", "Supply category: produce, meat, dairy, dry_goods, beverages"),
            ("payment_terms", "STRING", "Payment terms"),
            ("is_active", "BOOLEAN NOT NULL DEFAULT true", "Whether supplier is active"),
        ],
        "primary_key": "supplier_id",
        "partition_by": None,
        "comment": "Supplier master data for inventory management.",
    },
    "inventory": {
        "columns": [
            ("inventory_id", "STRING NOT NULL", "Unique inventory item identifier"),
            ("item_name", "STRING NOT NULL", "Inventory item name"),
            ("category", "STRING NOT NULL", "Category: produce, meat, dairy, dry_goods, beverages"),
            ("supplier_id", "STRING NOT NULL", "Foreign key to suppliers"),
            ("unit", "STRING NOT NULL", "Unit of measure: kg, lb, liter, gallon, unit"),
            ("current_quantity", "DECIMAL(10,2) NOT NULL", "Current quantity in stock"),
            ("reorder_level", "DECIMAL(10,2) NOT NULL", "Quantity at which to reorder"),
            ("unit_cost", "DECIMAL(8,2) NOT NULL", "Cost per unit"),
            ("total_value", "DECIMAL(10,2) NOT NULL", "Total value of current stock"),
            ("last_restocked", "DATE", "Date of last restock"),
            ("expiry_date", "DATE", "Expiration date if applicable"),
        ],
        "primary_key": "inventory_id",
        "partition_by": None,
        "comment": "Inventory levels with supplier information and reorder tracking.",
    },
    "staff": {
        "columns": [
            ("staff_id", "STRING NOT NULL", "Unique staff identifier"),
            ("first_name", "STRING NOT NULL", "Staff first name (PII)"),
            ("last_name", "STRING NOT NULL", "Staff last name (PII)"),
            ("email", "STRING NOT NULL", "Work email (PII)"),
            ("phone", "STRING", "Phone number (PII)"),
            ("role", "STRING NOT NULL", "Job role: head_chef, sous_chef, line_cook, server, host, bartender, manager"),
            ("department", "STRING NOT NULL", "Department: kitchen, front_of_house, management"),
            ("hire_date", "DATE NOT NULL", "Hire date"),
            ("hourly_rate", "DECIMAL(6,2) NOT NULL", "Hourly pay rate"),
            ("weekly_hours", "INT NOT NULL", "Scheduled weekly hours"),
            ("is_active", "BOOLEAN NOT NULL DEFAULT true", "Currently employed"),
        ],
        "primary_key": "staff_id",
        "partition_by": None,
        "comment": "Staff records with HR information. Contains PII - restrict access.",
    },
    "reviews": {
        "columns": [
            ("review_id", "STRING NOT NULL", "Unique review identifier"),
            ("order_id", "STRING NOT NULL", "Foreign key to orders"),
            ("customer_id", "STRING", "Foreign key to customers (null for anonymous)"),
            ("rating", "INT NOT NULL", "Rating from 1-5 stars"),
            ("review_text", "STRING", "Review text content"),
            ("aspects", "ARRAY<STRING>", "Aspects reviewed: food_quality, service, ambiance, value"),
            ("is_verified", "BOOLEAN NOT NULL", "Verified purchase review"),
            ("helpful_count", "INT NOT NULL DEFAULT 0", "Number of helpful votes"),
            ("response_text", "STRING", "Management response"),
            ("response_date", "TIMESTAMP", "Date of management response"),
            ("created_at", "TIMESTAMP NOT NULL", "Review creation timestamp"),
            ("source", "STRING NOT NULL", "Review source: website, mobile_app, google, yelp, internal"),
        ],
        "primary_key": "review_id",
        "partition_by": None,
        "comment": "Customer reviews linked to orders with ratings and feedback.",
    },
}


class DatabricksLoader:
    """Load sample data into Databricks Unity Catalog."""

    def __init__(
        self,
        catalog: str,
        schema: str,
        output_dir: str = "output",
        profile: Optional[str] = None,
    ):
        """
        Initialize the loader.

        Args:
            catalog: Unity Catalog catalog name
            schema: Schema name within catalog
            output_dir: Directory containing generated JSON files
            profile: Databricks CLI profile (uses default if None)
        """
        self.catalog = catalog
        self.schema = schema
        self.output_dir = output_dir
        self.full_schema = f"{catalog}.{schema}"

        # Initialize workspace client
        kwargs = {}
        if profile:
            kwargs["profile"] = profile
        self.client = WorkspaceClient(**kwargs)

        print(f"✓ Connected to Databricks workspace")
        print(f"  Target: {self.full_schema}")

    def ensure_catalog_exists(self) -> bool:
        """Ensure the catalog exists, create if not."""
        try:
            self.client.catalogs.get(self.catalog)
            print(f"✓ Catalog '{self.catalog}' exists")
            return True
        except NotFound:
            print(f"⚠ Catalog '{self.catalog}' not found")
            print(f"  Creating catalog '{self.catalog}'...")
            try:
                self.client.catalogs.create(
                    name=self.catalog,
                    comment="Restaurant business sample data catalog",
                )
                print(f"✓ Created catalog '{self.catalog}'")
                return True
            except Exception as e:
                print(f"✗ Failed to create catalog: {e}")
                return False

    def ensure_schema_exists(self) -> bool:
        """Ensure the schema exists, create if not."""
        try:
            self.client.schemas.get(self.full_schema)
            print(f"✓ Schema '{self.full_schema}' exists")
            return True
        except NotFound:
            print(f"⚠ Schema '{self.full_schema}' not found")
            print(f"  Creating schema '{self.full_schema}'...")
            try:
                self.client.schemas.create(
                    name=self.schema,
                    catalog_name=self.catalog,
                    comment="Restaurant business domain sample data",
                )
                print(f"✓ Created schema '{self.full_schema}'")
                return True
            except Exception as e:
                print(f"✗ Failed to create schema: {e}")
                return False

    def create_table(self, table_name: str) -> bool:
        """
        Create a Delta table with proper schema.

        Args:
            table_name: Name of the table to create

        Returns:
            True if successful, False otherwise
        """
        if table_name not in TABLE_SCHEMAS:
            print(f"⚠ No schema defined for table '{table_name}'")
            return False

        schema_def = TABLE_SCHEMAS[table_name]
        full_table_name = f"{self.full_schema}.{table_name}"

        # Build column definitions
        column_defs = []
        for col_name, col_type, col_comment in schema_def["columns"]:
            column_defs.append(f"{col_name} {col_type} COMMENT '{col_comment}'")

        columns_sql = ",\n    ".join(column_defs)

        # Build CREATE TABLE statement
        create_sql = f"""
CREATE TABLE IF NOT EXISTS {full_table_name} (
    {columns_sql}
)
USING DELTA
COMMENT '{schema_def["comment"]}'
"""

        # Add primary key constraint
        if schema_def.get("primary_key"):
            create_sql += f"""
TBLPROPERTIES (
    'primary_key' = '{schema_def["primary_key"]}'
)
"""

        try:
            # Execute CREATE TABLE via SQL statement
            self.client.statement_execution.execute_statement(
                statement=create_sql,
                warehouse_id=self._get_warehouse_id(),
                catalog=self.catalog,
                schema=self.schema,
            )
            print(f"✓ Created table '{full_table_name}'")
            return True
        except Exception as e:
            print(f"✗ Failed to create table '{table_name}': {e}")
            return False

    def _get_warehouse_id(self) -> str:
        """Get the first available SQL warehouse ID."""
        warehouses = list(self.client.warehouses.list())
        if not warehouses:
            raise RuntimeError("No SQL warehouses found in workspace")

        # Prefer running warehouses
        for wh in warehouses:
            if wh.state == "RUNNING":
                return wh.id

        # Fall back to first warehouse
        return warehouses[0].id

    def load_data(self, table_name: str) -> bool:
        """
        Load data from JSON file into table.

        Args:
            table_name: Name of the table to load

        Returns:
            True if successful, False otherwise
        """
        json_file = os.path.join(self.output_dir, f"{table_name}.json")

        if not os.path.exists(json_file):
            print(f"⚠ JSON file not found: {json_file}")
            return False

        # Read JSON data
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        if not data:
            print(f"⚠ No data in {json_file}")
            return False

        full_table_name = f"{self.full_schema}.{table_name}"
        print(f"  Loading {len(data)} records into {full_table_name}...")

        # Use INSERT statements (for small datasets)
        # For larger datasets, consider using DBFS upload + COPY INTO
        try:
            # Convert records to VALUES clauses
            schema_def = TABLE_SCHEMAS[table_name]
            column_names = [col[0] for col in schema_def["columns"]]

            # Build batch insert
            # Note: For production, use bulk loading via DBFS/Volume
            inserted = 0
            batch_size = 100

            for i in range(0, len(data), batch_size):
                batch = data[i : i + batch_size]

                for record in batch:
                    values = self._format_values(record, schema_def["columns"])
                    columns_sql = ", ".join(column_names)
                    values_sql = ", ".join(values)

                    insert_sql = f"INSERT INTO {full_table_name} ({columns_sql}) VALUES ({values_sql})"

                    try:
                        self.client.statement_execution.execute_statement(
                            statement=insert_sql,
                            warehouse_id=self._get_warehouse_id(),
                            catalog=self.catalog,
                            schema=self.schema,
                        )
                        inserted += 1
                    except Exception as e:
                        # Log but continue for individual record failures
                        print(f"    ⚠ Failed to insert record: {e}")

            print(f"  ✓ Loaded {inserted}/{len(data)} records into {full_table_name}")
            return inserted > 0

        except Exception as e:
            print(f"  ✗ Failed to load data into '{table_name}': {e}")
            return False

    def _format_values(self, record: Dict[str, Any], columns: List[tuple]) -> List[str]:
        """Format record values for SQL INSERT."""
        values = []
        for col_name, col_type, _ in columns:
            value = record.get(col_name)

            if value is None:
                values.append("NULL")
            elif col_type.startswith("STRING") or col_type == "DATE":
                # Escape single quotes
                if isinstance(value, str):
                    escaped = value.replace("'", "''")
                    values.append(f"'{escaped}'")
                else:
                    values.append(f"'{value}'")
            elif col_type.startswith("ARRAY"):
                # Handle array types
                if isinstance(value, list):
                    arr_str = json.dumps(value)
                    values.append(f"ARRAY({arr_str[1:-1]})")  # Remove brackets
                else:
                    values.append("NULL")
            elif col_type == "BOOLEAN":
                values.append("TRUE" if value else "FALSE")
            elif col_type.startswith("TIMESTAMP"):
                values.append(f"'{value}'")
            else:
                values.append(str(value))

        return values

    def load_all_tables(
        self, tables: Optional[List[str]] = None, recreate: bool = False
    ) -> Dict[str, bool]:
        """
        Load all tables with data.

        Args:
            tables: List of tables to load (all if None)
            recreate: Whether to drop and recreate tables

        Returns:
            Dictionary mapping table names to success status
        """
        if tables is None:
            tables = list(TABLE_SCHEMAS.keys())

        results = {}

        print("\n" + "=" * 60)
        print("Loading Restaurant Sample Data into Databricks")
        print("=" * 60)

        # Ensure catalog and schema exist
        if not self.ensure_catalog_exists():
            return {t: False for t in tables}

        if not self.ensure_schema_exists():
            return {t: False for t in tables}

        # Process each table
        for table_name in tables:
            print(f"\n📊 Processing table: {table_name}")
            print("-" * 40)

            # Drop table if recreate requested
            if recreate:
                try:
                    self.client.tables.delete(f"{self.full_schema}.{table_name}")
                    print(f"  ✓ Dropped existing table")
                except NotFound:
                    pass
                except Exception as e:
                    print(f"  ⚠ Could not drop table: {e}")

            # Create table
            if not self.create_table(table_name):
                results[table_name] = False
                continue

            # Load data
            results[table_name] = self.load_data(table_name)

        # Summary
        print("\n" + "=" * 60)
        print("Load Summary")
        print("=" * 60)

        success_count = sum(1 for v in results.values() if v)
        fail_count = len(results) - success_count

        for table, success in results.items():
            status = "✓" if success else "✗"
            print(f"  {status} {table}")

        print(f"\nTotal: {success_count} succeeded, {fail_count} failed")
        print(f"Schema: {self.full_schema}")

        return results


def main():
    parser = argparse.ArgumentParser(
        description="Load restaurant sample data into Databricks Unity Catalog"
    )
    parser.add_argument(
        "--catalog",
        default="main",
        help="Unity Catalog catalog name (default: main)",
    )
    parser.add_argument(
        "--schema",
        default="restaurant",
        help="Schema name within catalog (default: restaurant)",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory containing generated JSON files (default: output)",
    )
    parser.add_argument(
        "--profile",
        help="Databricks CLI profile name",
    )
    parser.add_argument(
        "--tables",
        nargs="+",
        help="Specific tables to load (default: all)",
    )
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Drop and recreate tables",
    )

    args = parser.parse_args()

    # Initialize loader
    loader = DatabricksLoader(
        catalog=args.catalog,
        schema=args.schema,
        output_dir=args.output_dir,
        profile=args.profile,
    )

    # Load tables
    results = loader.load_all_tables(tables=args.tables, recreate=args.recreate)

    # Exit with error if any failed
    if not all(results.values()):
        sys.exit(1)


if __name__ == "__main__":
    main()
