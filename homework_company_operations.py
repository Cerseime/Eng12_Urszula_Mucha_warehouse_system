#    --- PREDEFINED UNCHANGABLE ---

#Possible commands of operation
commands = [
    "Balance",
    "Sale",
    "Purchase",
    "Account",
    "List",
    "Warehouse",
    "Review",
    "End"
]

#    --- TRACKING ---

#company account money value
current_account_balance = 542  # made-up number to start with something

#tracking the operations done by the user
operations = []

#warehouse items with their price and quantity - made up to start with something
warehouse = {
    "Lemon": {"Quantity": 115, "Price": 0.5},
    "Cauliflower": {"Quantity": 80, "Price": 1},
    "Basket": {"Quantity": 31, "Price": 8.3}
}

#        --- FUNCTIONS ---

#GETTING THE USER CHOICE
#To save the user time and minimize letter mistakes I decided for a number input
def select_from_list(options, name):
    print(f"\nSelect {name}")
    for i, option in enumerate(options, start=1):
        print(f"{i}) {option}")

    while True:
        user_entry = input("Option: ")

        try:
            choice = int(user_entry) - 1

        except ValueError:
            print(f"Please write a number of the chosen {name} .")
            continue

        if 0 <= choice < len(options):
            print(f"You've chosen {name}:", options[choice])
            return options[choice]
        else:
            print("Please select a valid number")

#MAKING THE BALANCE OPERATION
def balance_command(current_account_balance, operations):
    print("Change the account balance. Write a negative number to remove money, positive to add.")

    try:
        action_with_money = float(input("Amount: "))
    except ValueError:
        print("Please enter a number")
        return current_account_balance

    current_account_balance += action_with_money
    operations.append(
        f"Balance changed by {action_with_money}, new balance: {current_account_balance}"
    )

    print("\n--- Result ---")
    print("Current balance:", current_account_balance)
    return current_account_balance

#MAKING THE SALE OPERATION
def sale_command(warehouse, current_account_balance, operations):
    print("You can only sell products that are available in the warehouse:")


    while True:
        item_chosen = select_from_list(list(warehouse.keys()), "item")
        item_sold = int(input("How many of the " + item_chosen + " item are you selling? "))
        if item_sold > warehouse[item_chosen]["Quantity"]:
            print(f"Not enough {item_chosen}s in the warehouse!")
            continue

        warehouse[item_chosen]["Quantity"] -= item_sold

        current_account_balance += warehouse[item_chosen]["Price"] * item_sold
        operations.append(
            f"{item_sold} of {item_chosen} items sold, new account balance: {current_account_balance}. There are {warehouse[item_chosen]["Quantity"]} of {item_chosen} left in the warehouse."
        )

        print("\n--- Result ---")
        print(operations[-1])
        return current_account_balance

# MAKING THE PURCHASE OPERATION
def purchase_command(warehouse, current_account_balance, operations):
    print(f"There's {current_account_balance} money available in your account.")
    while True:
        item_new_name = input("What's the name of the new item? ")
        item_new_cost = float(input("How much did a single count cost? "))
        item_new_quantity = int(input("How many of the new item are you buying? "))
        item_new_price = float(input("What's your price of the new item (How much will you sell it for)? "))

        item_new_name_capitalized = item_new_name.capitalize() #to minimize duplicates made by entering the same item with different sized letters
        total_cost = item_new_cost * item_new_quantity

        if item_new_quantity <= 0 or item_new_cost <= 0:
            print("Invalid values - number has to be positive!")
            continue

        if total_cost > current_account_balance:
            print(f"There's not enough money for this purchase!")
            continue

        current_account_balance -= total_cost

        print("\n--- Result ---")
        if item_new_name_capitalized in warehouse:
            warehouse[item_new_name_capitalized]["Quantity"] += item_new_quantity # just add to existing stock
            warehouse[item_new_name_capitalized]["Price"] = item_new_price #update the old price
            operations.append(
                f"Quantity of {item_new_name_capitalized} updated. There is now {warehouse[item_new_name_capitalized]["Quantity"]} items, and they will be sold for {item_new_price}.\nNew account balance: {current_account_balance}."
            )
        else:
            warehouse[item_new_name_capitalized] = {
                    "Quantity": item_new_quantity,
                    "Price": item_new_price
            }
            operations.append(
                f"{item_new_quantity} of {item_new_name_capitalized} items purchased, new account balance: {current_account_balance}.")

        print(operations[-1])
        return current_account_balance

# GETTING THE LOW STOCK
def get_low_stock_items(warehouse, threshold=50):
    return [
        item
        for item, info in warehouse.items()
        if info["Quantity"] < threshold
    ]


# MAKING THE LIST OPERATION
def list_command(warehouse, operations):
    print(f"\nCurrent warehouse state:")


    print("{:<15} {:<15} {:<15}".format("Item", "Quantity", "Price"))
    for item, info in warehouse.items():
        quantity = info["Quantity"]
        price = info["Price"]
        print("{:<15} {:<15} {:<15.2f}".format(item, quantity, price))

    low_stock_items = get_low_stock_items(warehouse)

    if low_stock_items:
        items_running_low = ", ".join(low_stock_items)
        print(f"\nItems low on stock: {items_running_low}.")
        operations.append(
            f"\nWarehouse status checked. Items low on stock: {items_running_low}.")
    else:
        operations.append(
            f"\nWarehouse status checked.")

# MAKING THE WAREHOUSE OPERATION
def warehouse_command(warehouse, operations):
    print("Choose a product you want to check:")

    item_chosen = select_from_list(list(warehouse.keys()), "item")
    info = warehouse[item_chosen]
    quantity = info["Quantity"]
    price = info["Price"]
    print()
    print("{:<15} {:<15} {:<15}".format("Item", "Quantity", "Price"))
    print("{:<15} {:<15} {:<15.2f}".format(item_chosen, quantity, price))

    low_stock_items = get_low_stock_items(warehouse)

    if item_chosen in low_stock_items:
        print(f"\n{item_chosen} is low on stock.")
        operations.append(
            f"\n{item_chosen} status checked. Item low on stock.")
    else:
        operations.append(
            f"\n{item_chosen} status checked.")

# MAKING THE REVIEW OPERATION

def review_command(operations):
    if not operations:
        print("No operations yet.")
        return
    while True:
        start_input = int(input("Enter the start operation number (leave blank for the first):"))
        end_input = int(input("Enter the end operation number (leave blank for the last):"))

        try:
            start = start_input - 1 if start_input else 0
            end = end_input if end_input else len(operations)
        except ValueError:
            print("Enter valid numbers")
            continue

        if start < 0 or end > len(operations) or start >= end:
            print("invalid range.")
            continue

        print("\nOperations done:")
        for chosen_operation in operations[start:end]:
            print(chosen_operation)

        return #exiting the review after writing a correct number



# --- ACTUAL PROGRAM ---

#While loop to ask the user about the operation until they choose "End"
#While command != "End":
#Ask user what operation they want - I chose to handle the human mistakes by providing a list choice
while True:
    command_chosen = select_from_list(commands, "command")

    if command_chosen == "Balance":
        #ask for number to add/ extract from the account
        #do the math on the numbers
        #print the new account result
        current_account_balance = balance_command(current_account_balance, operations)

    elif command_chosen == "Sale":
        #ask the user what product did they buy, how many and how much did it cost
        #update numbers in the warehouse and bank balance
        #print some statement?
        current_account_balance = sale_command(warehouse, current_account_balance, operations)

    elif command_chosen == "Purchase":
        #ask the user what product did they buy, how many and how much did it cost
        #update numbers in the warehouse
        #print a statement if the bank balance become empty or minus
        current_account_balance = purchase_command(warehouse, current_account_balance, operations)

    elif command_chosen == "Account":
        #print how much money is on the account.
        print(f"\nCurrent account balance: {current_account_balance}")
        operations.append(
            f"Account balance checked. Current account balance: {current_account_balance}.")

    elif command_chosen == "List":
        #display current warehouse state - prices and quantities
        list_command(warehouse, operations)

    elif command_chosen == "Warehouse":
        #ask user about the item they want to check
        #print the status of warehouse for this item - how many of this product is left
        warehouse_command(warehouse, operations)

    elif command_chosen == "Review":  #review the operations which happened until now
        review_command(operations)
        #ask user to provide range from and to, or nothing, to display all operations.
        #Show some error when a range is out of ass
    elif command_chosen == "End":
        print("Operations completed")
        break