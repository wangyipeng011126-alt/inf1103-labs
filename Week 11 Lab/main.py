import os
import json

from inventory import Inventory
from physicalproduct import PhysicalProduct
from digitalproduct import DigitalProduct
from subscription_product import SubscriptionProduct
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


def load_inventory() -> Inventory:
    inventory = Inventory()

    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)

        for item in data:
            supplier = resolve_supplier(item.get("supplier"))
            product_type = item.get("type")

            if product_type == "physical":
                product = PhysicalProduct(
                    item["product_id"], item["name"], item["price"],
                    item["stock"], item["weight"], supplier,
                )
            elif product_type == "digital":
                product = DigitalProduct(
                    item["product_id"], item["name"], item["price"],
                    item["stock"], item["download_size"], supplier,
                )
            elif product_type == "subscription":
                product = SubscriptionProduct(
                    item["product_id"], item["name"], item["price"],
                    item["stock"], item["billing_period"], supplier,
                )
            else:
                print(f"⚠️  Skipping unknown product type: {product_type!r}")
                continue

            inventory.add_product(product)

        print("inventory.json found.")
        print("Inventory loaded successfully.")

    except FileNotFoundError:
        print("inventory.json not found. Starting fresh.")
    except json.JSONDecodeError:
        print("inventory.json is empty or corrupted. Starting fresh.")

    return inventory


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
        print("6. Exit")
        print("----------------------------")

        option = input("Enter option: ")

        if option == "1":
            inventory.display_all()

        elif option == "2":
            print("Add New Product")
            product_id = input("Product ID: ")
            name = input("Product Name: ")

            try:
                price = float(input("Price: "))
                stock = int(input("Stock Quantity: "))

                if price < 0 or stock < 0:
                    print("Error: Price and stock cannot be negative.")
                    continue

                product_type = (
                    input("Product type (physical/digital/subscription): ")
                    .strip().lower()
                )

                if product_type not in ("physical", "digital", "subscription"):
                    print("Error: Invalid product type.")
                    continue

                supplier = prompt_supplier()

                if product_type == "physical":
                    weight = float(input("Weight (kg): "))
                    if weight < 0:
                        print("Error: Weight cannot be negative.")
                        continue
                    product = PhysicalProduct(
                        product_id, name, price, stock, weight, supplier
                    )
                elif product_type == "digital":
                    download_size = float(input("Download size (MB): "))
                    if download_size < 0:
                        print("Error: Download size cannot be negative.")
                        continue
                    product = DigitalProduct(
                        product_id, name, price, stock, download_size, supplier
                    )
                else:  # subscription
                    billing_period = (
                        input("Billing period (monthly/yearly): ").strip().lower()
                    )
                    if billing_period not in ("monthly", "yearly"):
                        print("Error: Billing period must be 'monthly' or 'yearly'.")
                        continue
                    product = SubscriptionProduct(
                        product_id, name, price, stock, billing_period, supplier
                    )

                if inventory.add_product(product):
                    print("Product added successfully!")
                else:
                    print("Error: Product ID already exists.")

            except ValueError:
                print("Error: Please enter valid numeric values.")

        elif option == "3":
            print("Update Stock")
            product_id = input("Enter Product ID: ")
            product = inventory.search_product(product_id)

            if product:
                print("Product Found!")
                print(f"Name: {product.get_name()}")
                print(f"Current Stock: {product.get_stock()}")
                try:
                    new_stock = int(input("New Stock Quantity: "))
                    if new_stock < 0:
                        print("Error: Stock cannot be negative.")
                    else:
                        product.update_stock(new_stock)
                        print("Stock updated successfully!")
                except ValueError:
                    print("Error: Please enter a valid stock quantity.")
            else:
                print("Product not found.")

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
                    print(f"  Shipping cost: ${product.calculate_shipping_cost():.2f}")
                print("-" * 48)
            else:
                print("Product not found.")

        elif option == "5":
            print("Saving inventory...")
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json.")

        elif option == "6":
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