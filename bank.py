import os
import json

class BankingSystem:
    def __init__(self):
        self.customer_last_id = 0
        self.customers = {}
        self.load_customer_data()

    def load_customer_data(self):
        if os.path.exists("customers_data.json"):
            try:
                with open("customers_data.json", "r") as file:
                    data = json.load(file)
                    self.customers = data.get("customers", {})
                    self.customer_last_id = data.get("last_id", 0)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading customer data: {e}")
    
    def save_customer_data(self):
        
        data = {
            "customers": self.customers,
            "last_id": self.customer_last_id
        }
        try:
            with open("customers_data.json", "w") as file:
                json.dump(data, file, indent=4)
        except IOError as e:
            print(f"Error saving customer data: {e}")

    def auto_generate_customer_id(self):
        
        self.customer_last_id += 1
        return f"cu{str(self.customer_last_id).zfill(3)}"

    def create_customer_account(self):
       
        account_number = input("Enter the account number: ")
        if account_number in self.customers:
            print("This account already exists.")
            return
        customer_id = self.auto_generate_customer_id()
        name = input("Enter the customer name: ")
        password = input("Enter the customer password: ")
        try:
            balance = float(input("Enter the current balance: "))
            if balance < 0:
                raise ValueError("Balance cannot be negative.")
        except ValueError as e:
            print(f"Invalid balance: {e}")
            return
        self.customers[account_number] = {
            "customer_id": customer_id,
            "name": name,
            "password": password,
            "balance": balance,
            "transaction_history": ["Account created."]
        }
        self.save_customer_data()
        print(f"Customer ID: {customer_id}")
        print("Account created successfully.")

    def deposit(self):
        
        account_number = input("Enter the account number: ")
        if account_number not in self.customers:
            print("Invalid account number.")
            return
        try:
            amount = float(input("Enter the deposit amount: "))
            if amount <= 0:
                raise ValueError("Deposit amount must be positive.")
        except ValueError as e:
            print(f"Invalid amount: {e}")
            return
        self.customers[account_number]["balance"] += amount
        self.customers[account_number]["transaction_history"].append(f"Deposited: {amount}")
        self.save_customer_data()
        print(f"Deposit successful. New balance: {self.customers[account_number]['balance']}")

    def withdraw(self):
       
        account_number = input("Enter the account number: ")
        if account_number not in self.customers:
            print("Invalid account number.")
            return
        try:
            amount = float(input("Enter the withdrawal amount: "))
            if amount <= 0:
                raise ValueError("Withdrawal amount must be positive.")
            if amount > self.customers[account_number]["balance"]:
                raise ValueError("Insufficient funds.")
        except ValueError as e:
            print(f"Invalid amount: {e}")
            return
        self.customers[account_number]["balance"] -= amount
        self.customers[account_number]["transaction_history"].append(f"Withdrew: {amount}")
        self.save_customer_data()
        print(f"Withdrawal successful. New balance: {self.customers[account_number]['balance']}")

    def check_balance(self):
       
        account_number = input("Enter the account number: ")
        if account_number not in self.customers:
            print("Invalid account number.")
            return
        print(f"Balance: {self.customers[account_number]['balance']}")

    def transaction_history(self):
        
        account_number = input("Enter the account number: ")
        if account_number not in self.customers:
            print("Invalid account number.")
            return
        print("Transaction History:")
        for transaction in self.customers[account_number]["transaction_history"]:
            print(transaction)

    def main(self):
        
       
        while True:
            print("\n1. Create Account")
            print("2. Deposit Money")
            print("3. Withdraw Money")
            print("4. Check Balance")
            print("5. Transaction History")
            print("6. Exit")
            choice = input("Enter your choice: ")
            if choice == "1":
                self.create_customer_account()
            elif choice == "2":
                self.deposit()
            elif choice == "3":
                self.withdraw()
            elif choice == "4":
                self.check_balance()
            elif choice == "5":
                self.transaction_history()
            elif choice == "6":
                print("Exiting system.")
                break
            else:
                print("Invalid choice. Please try again.")
def admin_login():
    print("--- Admin Login ---")
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")

    if username == "admin" and password == "admin123":
        print("Login successful.\n")
        main_menu()
    else:
        print("Invalid credentials. Access denied.")

Admin_login()
if __name__ == "__main__":
    system = BankingSystem()
    system.main()
   
