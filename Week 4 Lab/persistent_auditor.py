# Global Constants
MAX_CAPACITY = 500
TAX_RATE = 0.1  # 10% tax rate
INVENTORY_FILE = "inventory.txt"


def load_inventory():
    """Read the saved inventory from the file."""
    try:
        with open(INVENTORY_FILE, "r") as f:
            inventory = []

            for line in f:
                line = line.strip()

                if line:
                    parts = line.split(",")

                    item_id = int(parts[0].strip())
                    product_name = parts[1].strip()
                    quantity = int(parts[2].strip())

                    inventory.append(
                        (item_id, product_name, quantity)
                    )

            return inventory

    except FileNotFoundError:
        print("No previous records found! Starting with an empty inventory.")
        return []


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
    inventory = 0
    transaction_history = []
    failed_entries = 0
    exit_program = False

    # Load previously saved inventory
    transaction_history = load_inventory()



    print("\nCurrent Inventory:")
    print("")
    for item in transaction_history:
        item_id, product_name, quantity = item

        print(
            f"{item_id}, {product_name}, {quantity}"
        )

    while not exit_program:
        product_name, quantity = get_valid_input()

        if product_name == "quit":

            # Calculate tax
            tax_amount = calculate_tax(inventory)

            print("\nTotal Inventory:", inventory)
            print("Tax Amount:", tax_amount)

            generate_report(inventory, failed_entries)

            exit_program = True

        else:
            # Check maximum capacity
            if inventory > MAX_CAPACITY:
                print(
                    "ALERT: Overstock! Inventory exceeds 500 units."
                )


# Program Entry Point
if __name__ == "__main__":
    main()