import datetime

# Data storage
customers = {}
customer_last_id = 0

# Load full customer data from bank_data.txt
def load_customer_data():
    global customer_last_id
    try:
        with open("bank_data.txt", "r") as f:
            for line in f:
                parts = line.strip().split("|")
                if len(parts) == 6:
                    acc, cid, name, pwd, bal, txn = parts
                    customers[acc] = {
                        "customer_id": cid,
                        "name": name,
                        "password": pwd,
                        "balance": float(bal),
                        "transaction_history": txn.split(";") if txn else []
                    }
                    id_num = int(cid[2:])
                    if id_num > customer_last_id:
                        customer_last_id = id_num
    except FileNotFoundError:
        pass

# Save all customer data to bank_data.txt
def save_customer_data():
    with open("bank_data.txt", "w") as f:
        for acc, data in customers.items():
            txn_str = ";".join(data["transaction_history"])
            line = f"{acc}|{data['customer_id']}|{data['name']}|{data['password']}|{data['balance']}|{txn_str}\n"
            f.write(line)

# Save only ID, name, password to logins.txt
def save_customer_personal_data():
    with open("logins.txt", "w") as f:
        for data in customers.values():
            f.write(f"{data['customer_id']}|{data['name']}|{data['password']}\n")

# Save both files
def save_all_data():
    save_customer_data()
    save_customer_personal_data()

def auto_generate_customer_id():
    global customer_last_id
    customer_last_id += 1
    return f"cu{str(customer_last_id).zfill(3)}"

def get_current_time():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_customer_account():
    account_number = input("Enter the account number: ")
    if account_number in customers:
        print("This account already exists.")
        return
    customer_id = auto_generate_customer_id()
    name = input("Enter the customer name: ")
    password = input("Enter the customer password: ")
    try:
        balance = float(input("Enter the current balance: "))
        if balance < 0:
            raise ValueError("Balance cannot be negative.")
    except ValueError as e:
        print(f"Invalid balance: {e}")
        return
    customers[account_number] = {
        "customer_id": customer_id,
        "name": name,
        "password": password,
        "balance": balance,
        "transaction_history": [f"Account created on {get_current_time()}."]
    }
    save_all_data()
    print(f"Customer ID: {customer_id}")
    print("Account created successfully.")

def update_account():
    account_number = input("Enter the account number to update: ")
    if account_number not in customers:
        print("Invalid account number.")
        return
    print("1. Update Name")
    print("2. Update Password")
    choice = input("Enter your choice: ")
    if choice == "1":
        new_name = input("Enter new name: ")
        customers[account_number]["name"] = new_name
        print("Name updated successfully.")
    elif choice == "2":
        new_password = input("Enter new password: ")
        customers[account_number]["password"] = new_password
        print("Password updated successfully.")
    else:
        print("Invalid choice.")
        return
    save_all_data()

def delete_account():
    account_number = input("Enter the account number to delete: ")
    if account_number not in customers:
        print("Invalid account number.")
        return
    del customers[account_number]
    save_all_data()
    print("Account deleted successfully.")

def deposit():
    account_number = input("Enter the account number: ")
    if account_number not in customers:
        print("Invalid account number.")
        return
    try:
        amount = float(input("Enter the deposit amount: "))
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
    except ValueError as e:
        print(f"Invalid amount: {e}")
        return
    customers[account_number]["balance"] += amount
    transaction_time = get_current_time()
    customers[account_number]["transaction_history"].append(f"Deposited: {amount} on {transaction_time}")
    print(f"Deposit successful. New balance: {customers[account_number]['balance']}")
    save_all_data()

def withdraw():
    account_number = input("Enter the account number: ")
    if account_number not in customers:
        print("Invalid account number.")
        return
    try:
        amount = float(input("Enter the withdrawal amount: "))
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        if amount > customers[account_number]["balance"]:
            raise ValueError("Insufficient funds.")
    except ValueError as e:
        print(f"Invalid amount: {e}")
        return
    customers[account_number]["balance"] -= amount
    transaction_time = get_current_time()
    customers[account_number]["transaction_history"].append(f"Withdrew: {amount} on {transaction_time}")
    print(f"Withdrawal successful. New balance: {customers[account_number]['balance']}")
    save_all_data()

def check_balance():
    account_number = input("Enter the account number: ")
    if account_number not in customers:
        print("Invalid account number.")
        return
    print(f"Balance: {customers[account_number]['balance']}")

def transaction_history():
    account_number = input("Enter the account number: ")
    if account_number not in customers:
        print("Invalid account number.")
        return
    print("Transaction History:")
    for transaction in customers[account_number]["transaction_history"]:
        print(transaction)

# Main Menu
def main_menu():
    while True:
        print("\n1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Update Account")
        print("7. Delete Account")
        print("8. Exit - Admin will Exit, Customer will Return to Main Menu")

        choice = input("Enter your choice: ")

        if choice == "1":
            create_customer_account()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            check_balance()
        elif choice == "5":
            transaction_history()
        elif choice == "6":
            update_account()
        elif choice == "7":
            delete_account()
        elif choice == "8":
            user_role = input("Are you an Admin or Customer? (admin/customer): ")
            if user_role == "admin":
                print("Exiting admin system. Program will now terminate.")
                exit()  # Admin exits the program completely
            elif user_role == "Customer":
                print("Exiting customer menu... Returning to Main Menu.")
                break  # Customer exits back to the main menu
            else:
                print("Invalid input. Please enter 'admin' or 'Customer'.")
        else:
            print("Invalid choice. Please try again.")

# Entry point
if __name__ == "__main__":
    load_customer_data()
    main_menu()  # Start the main menu directly
