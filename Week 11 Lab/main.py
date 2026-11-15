import os
import json
import csv

from inventory import Inventory
from product_factory import ProductFactory
from supplier import Supplier

INVENTORY_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "inventory.json"
)

# Fallback for old inventory.json files that have no "supplier" block.
UNKNOWN_SUPPLIER = Supplier("SUP-000", "Unknown Supplier", "unknown@example.com")

# Shared cache so products with the same supplier_id share ONE Supplier object.
known_suppliers: dict[str, Supplier] = {}


def resolve_supplier(raw: dict | None) -> Supplier:
    if not raw:
        return UNKNOWN_SUPPLIER
    sid = raw["supplier_id"]
    if sid not in known_suppliers:
        known_suppliers[sid] = Supplier(sid, raw["name"], raw["contact_email"])
    return known_suppliers[sid]


def prompt_supplier() -> Supplier:
    supplier_id = input("Supplier ID: ").strip()
    existing = known_suppliers.get(supplier_id)
    if existing is not None:
        print(f"Using existing supplier: {existing.get_name()}")
        return existing
    name = input("Supplier Name: ").strip()
    email = input("Supplier Contact Email: ").strip()
    supplier = Supplier(supplier_id, name, email)
    known_suppliers[supplier_id] = supplier
    return supplier


def get_positive_float(prompt: str) -> float:
    """Keep asking until the user enters a number greater than zero."""
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")


def get_non_negative_int(prompt: str) -> int:
    """Keep asking until the user enters a whole number >= 0."""
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a whole number (0 or more).")
                continue
            return value
        except ValueError:
            print("Please enter a whole number, e.g. 10")


def get_non_negative_float(prompt: str) -> float:
    """Keep asking until the user enters a number >= 0."""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a number (0 or more).")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 2.5")


def load_inventory() -> Inventory:
    inventory = Inventory()

    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)

        for item in data:
            supplier = resolve_supplier(item.get("supplier"))

            try:
                product = ProductFactory.create(
                    item["type"],
                    item["product_id"], item["name"], item["price"],
                    item["stock"], supplier,
                    weight=item.get("weight"),
                    download_size=item.get("download_size"),
                    billing_period=item.get("billing_period"),
                )
            except ValueError as error:
                print(f"⚠️  Skipping product: {error}")
                continue

            inventory.add_product(product)

        print("inventory.json found.")
        print("Inventory loaded successfully.")

    except FileNotFoundError:
        print("inventory.json not found. Starting fresh.")
    except json.JSONDecodeError:
        print("inventory.json is empty or corrupted. Starting fresh.")

    return inventory


def load_products(path: str, inventory: Inventory,
                  supplier: Supplier) -> None:
    """Load products from a CSV file via the factory.

    A missing file is reported, not raised. Individual bad rows are
    reported and skipped so loading carries on.
    """
    loaded = 0
    try:
        file = open(path, newline="")
    except FileNotFoundError:
        print(f"Products file not found: {path}")
    else:
        with file:
            reader = csv.reader(file)
            next(reader, None)          # skip header row
            for row_number, row in enumerate(reader, start=2):
                if not row or all(not cell.strip() for cell in row):
                    continue            # skip blank lines
                try:
                    product = ProductFactory.create(
                        row[0].strip(),        # product_type
                        row[1].strip(),        # product_id
                        row[2].strip(),        # name
                        row[3].strip(),        # price
                        row[4].strip(),        # stock_quantity
                        supplier,
                    )
                    if inventory.add_product(product):
                        loaded += 1
                    else:
                        print(f"⚠️  Row {row_number}: duplicate product "
                              f"ID {row[1].strip()} — skipped.")
                except (ValueError, IndexError) as error:
                    print(f"⚠️  Row {row_number}: {error} — skipped.")
        print(f"{loaded} products loaded.")
    finally:
        print("Load attempt finished.")


def save_inventory(inventory: Inventory) -> None:
    data = [product.to_dict() for product in inventory.get_products()]
    with open(INVENTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)


def main() -> None:
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)

    inventory = load_inventory()
    exit_program = False

    while not exit_program:
        print("\n----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Load Products from CSV")
        print("7. Exit")
        print("----------------------------")

        option = input("Enter option: ")

        if option == "1":
            inventory.display_all()

        elif option == "2":
            print("Add New Product")
            product_id = input("Product ID: ").strip()
            name = input("Product Name: ").strip()
            price = get_positive_float("Price: ")
            stock = get_non_negative_int("Stock Quantity: ")

            product_type = (
                input("Product type (physical/digital/subscription): ")
                .strip().lower()
            )
            if product_type not in ("physical", "digital", "subscription"):
                print("Error: Invalid product type.")
                continue

            supplier = prompt_supplier()

            type_specific: dict = {}
            if product_type == "physical":
                type_specific["weight"] = get_non_negative_float(
                    "Weight (kg): "
                )
            elif product_type == "digital":
                type_specific["download_size"] = get_non_negative_float(
                    "Download size (MB): "
                )
            else:
                while True:
                    period = (
                        input("Billing period (monthly/yearly): ")
                        .strip().lower()
                    )
                    if period in ("monthly", "yearly"):
                        type_specific["billing_period"] = period
                        break
                    print("Please enter 'monthly' or 'yearly'.")

            try:
                product = ProductFactory.create(
                    product_type, product_id, name, price, stock, supplier,
                    **type_specific,
                )
            except ValueError as error:
                print(f"Error: {error}")
                continue

            if inventory.add_product(product):
                print("Product added successfully!")
            else:
                print("Error: Product ID already exists.")

        elif option == "3":
            print("Update Stock")
            product_id = input("Enter Product ID: ").strip()
            product = inventory.search_product(product_id)

            if product is None:
                print("Product not found.")
                continue

            print("Product Found!")
            print(f"Name: {product.get_name()}")
            print(f"Current Stock: {product.get_stock()}")
            try:
                product.update_stock(int(input("New Stock Quantity: ")))
                print("Stock updated successfully!")
            except ValueError as error:
                print(f"Error: {error}")

        elif option == "4":
            print("Search Product")
            product_id = input("Enter Product ID: ")
            product = inventory.search_product(product_id)

            if product:
                print("Product Found")
                print("-" * 48)
                product.display_information()
                print(f"  Fulfilment: {product.get_fulfilment_info()}")
                if hasattr(product, "calculate_shipping_cost"):
                    print(f"  Shipping cost: "
                          f"${product.calculate_shipping_cost():.2f}")
                print("-" * 48)
            else:
                print("Product not found.")

        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json.")

        elif option == "6":
            path = input("CSV path (default: products.csv): ").strip()
            if not path:
                path = os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    "products.csv",
                )
            load_products(path, inventory, UNKNOWN_SUPPLIER)

        elif option == "7":
            print("Saving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            exit_program = True

        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()