# Global Constant
MAX_CAPACITY = 500
TAX_RATE = 0.1  # 10% tax rate


def get_valid_input(failed_entries):
    while True:
        user_input = input("Enter stock quantity or 'quit': ")

        if user_input == "quit":
            print("Exiting the program.")
            return "quit", failed_entries

        if user_input.startswith("-") and user_input[1:].isdigit():
            print("Error: Negative stock is not allowed.")
            failed_entries += 1
            print("Number of Failed/Rejected Entries for negative stock:", failed_entries)
            continue

        if not user_input.isdigit():
            print("Error: Invalid input.")
            failed_entries += 1
            print("Number of Failed/Rejected Entries for invalid input:", failed_entries)
            continue
        

        return user_input, failed_entries


def process_delivery(current_total, new_value):
    new_total = current_total + new_value

    print("Current inventory:", current_total)
    print("New stock added:", new_value)
    print("Total Inventory:", new_total)

    if new_total > MAX_CAPACITY:
        print("ALERT: Overstock! Inventory exceeds 500 units.")

    return new_total


def calculate_tax(amount):
    print("Calculating tax for total inventory:", amount)
    return amount * TAX_RATE


def generate_report(total_units, failed_entries):
    print("Total Units Processed:", total_units)
    print("Number of Failed/Rejected Entries:", failed_entries)


def main():
    inventory = 0
    tax_amount = 0
    failed_entries = 0
    exit_program = False

    while not exit_program:

        # Get both the user input AND updated failed_entries
        user_input_stock, failed_entries = get_valid_input(failed_entries)

        if user_input_stock == "quit":
            generate_report(inventory, failed_entries)
            exit_program = True

        else:
            inventory = process_delivery(inventory, int(user_input_stock))
            tax_amount = calculate_tax(inventory)


# Program Entry Point
if __name__ == "__main__":
    main()

