inventory = 0
failed_entries = 0

while True:
    stock = input("Enter stock quantity or 'quit': ")

    if stock.lower() == "quit":
        break

    # Check for negative number
    if stock.startswith("-") and stock[1:].isdigit():
        print("Error: Negative stock is not allowed.")
        failed_entries += 1
        continue

    # Check if input is a valid number
    if not stock.isdigit():
        print("Error: Invalid input.")
        failed_entries += 1
        continue

    stock = int(stock)

    inventory += stock
    print("Current inventory:", inventory)

    if inventory > 500:
        print("ALERT: Overstock! Inventory exceeds 500 units.")
        print ("test")
        break

print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)