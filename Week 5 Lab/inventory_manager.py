# Global Constants

import json

MAX_CAPACITY = 500
TAX_RATE = 0.1  # 10% tax rate
INVENTORY_FILE = r"inventory.json"


def load_inventory():
    inventory = []
    try:
        with open(INVENTORY_FILE, "r") as f:
            inventory = json.load(f)
        status = True
    except FileNotFoundError:
        status = False
    return inventory, status

def save_inventory(inventory):
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory, f, indent=4)

def search_product(inventory, product_id):
    for product in inventory:
        if product["product_id"] == product_id:
            return product
    return None

def add_product(inventory, product_id, name, price, stock):
    # Check if product ID already exists
    if search_product(inventory, product_id):
        return False
    
    new_product = {
        "product_id": product_id,
        "name": name,
        "price": float(price),
        "stock": int(stock)
    }
    inventory.append(new_product)
    return True

def update_stock(inventory, product_id, new_stock):
    product = search_product(inventory, product_id)
    if product:
        product["stock"] = int(new_stock)
        return True
    return False

# Part of UI
def display_all(inventory):
    print("Current Inventory")
    print("-" * 48)
    for product in inventory:
        print(f"ID: {product['product_id']} | Name: {product['name']} | Price: ${product['price']:.2f} | Stock: {product['stock']}")
    print("-" * 48)


def get_valid_input():
    """Get a valid product name and quantity from the user."""

    product_name = input("Enter Product Name: ")

    if product_name.lower() == "quit":
        return "quit", 0

    while True:
        quantity = input("Enter quantity: ")

        if quantity.isdigit() and int(quantity) > 0:
            return product_name, int(quantity)

        print("Error: Please enter a valid quantity.")


def process_delivery(current_total, new_value):
    new_total = current_total + new_value

    print("Current inventory:", current_total)
    print("New stock added:", new_value)
    print("Total Inventory:", new_total)

    return new_total


def calculate_tax(amount):
    return amount * TAX_RATE


def generate_report(total_units, failed_entries):
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_entries)


def main():
    """
    Main function to run inventory manager.
    """
    # local variables
    inventory = []
    exit_program = False
    
    # Display header and load inventory
    print("=" * 40)
    print("INVENTORY MANAGEMENT SYSTEM")
    print("=" * 40)
    
    inventory, status = load_inventory()
    
    if status:
        print("inventory.json found.")
        print("Inventory loaded successfully.")
    else:
        print("inventory.json not found. Starting fresh.")

    while not exit_program:
        print("----------- MENU -----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("----------------------------")
        
        option = input("Enter option: ")

        if option == "1":
            display_all(inventory)

        elif option == "2":
            print("Add New Product")
            product_id = input("Product ID: ")
            name = input("Product Name: ")
            price = input("Price: ")
            stock = input("Stock Quantity: ")
            
            if add_product(inventory, product_id, name, price, stock):
                print("Product added successfully!")
            else:
                print("Error: Product ID already exists.")

        elif option == "3":
            print("Update Stock")
            product_id = input("Enter Product ID: ")
            product = search_product(inventory, product_id)
            
            if product:
                print("Product Found!")
                print(f"Name: {product['name']}")
                print(f"Current Stock: {product['stock']}")
                new_stock = input("New Stock Quantity: ")
                update_stock(inventory, product_id, new_stock)
                print("Stock updated successfully!")
            else:
                print("Product not found.")

        elif option == "4":
            print("Search Product")
            product_id = input("Enter Product ID: ")
            product = search_product(inventory, product_id)
            
            if product:
                print("Product Found")
                print("-" * 48)
                print(f"ID: {product['product_id']}")
                print(f"Name: {product['name']}")
                print(f"Price: ${product['price']:.2f}")
                print(f"Stock: {product['stock']}")
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

# __name__ (Program Entry Point)
if __name__ == "__main__":
    main()
    