import os
import json
from product import Product
from inventory import Inventory


INVENTORY_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "inventory.json"
)


def load_inventory():
    inventory = Inventory()

    try:
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)

        for item in data:
            product = Product(
                item["product_id"],
                item["name"],
                item["price"],
                item["stock"]
            )
            inventory.add_product(product)

        print("inventory.json found.")
        print("Inventory loaded successfully.")

    except FileNotFoundError:
        print("inventory.json not found. Starting fresh.")

    return inventory


def save_inventory(inventory):
    # Convert Product objects into dictionaries for JSON
    data = [
        product.to_dict()
        for product in inventory.get_products()
    ]

    with open(INVENTORY_FILE, "w") as file:
        json.dump(data, file, indent=4)


def main():
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

                product = Product(product_id, name, price, stock)

                if inventory.add_product(product):
                    print("Product added successfully!")
                else:
                    print("Error: Product ID already exists.")

            except ValueError:
                print("Error: Please enter a valid price and stock quantity.")

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
