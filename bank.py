import datetime
# Data storage
customers = {}
customer_last_id = 0

# Functions for banking system
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
                        "transaction_history": [txn]
                    }
                    id_num = int(cid[2:])
                    if id_num > customer_last_id:
                        customer_last_id = id_num
    except FileNotFoundError:
        pass
def auto_generate_customer_id():
    global customer_last_id
    customer_last_id += 1
    return f"cu{str(customer_last_id).zfill(3)}"

def get_current_time():
    # Return current date and time in a readable format
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def create_customer_account():
    account_number = input("Enter the account number: ")
    if account_number in customers:
        print("This account already exists.")
        return
    customer_id = auto_generate_customer_id()
    name = input("Enter the customer name: ")
    password = input("Enter the customer password: ")  # Password is visible
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
        new_password = input("Enter new password: ")  # Password is visible
        customers[account_number]["password"] = new_password
        print("Password updated successfully.")
    else:
        print("Invalid choice.")

def delete_account():
    account_number = input("Enter the account number to delete: ")
    if account_number not in customers:
        print("Invalid account number.")
        return
    del customers[account_number]
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

# Admin login function
def admin_login():
    print("--- Admin Login ---")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    if username == "admin" and password == "admin123":
        print("Login successful.\n")
        main_menu()  # Show the banking menu
    else:
        print("Invalid credentials. Access denied.")

# Main menu for banking operations
def main_menu():
    while True:
        print("\n1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Transaction History")
        print("6. Update Account")
        print("7. Delete Account")
        print("8. Exit")
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
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Please try again.")

# Entry point
if __name__ == "__main__":
    load_customer_data()
    admin_login()
