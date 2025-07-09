from db_manager import DBManager
from auth import Authenticator
from create_account import CreateAccount
from deposit import Deposit
from withdraw import Withdraw
from history import History
from statement import Statement
from close_account import CloseAccount
from balance_enquiry import BalanceEnquiry

class BankSystem:
    def __init__(self, db):
        self.db = db
        self.current_user = None
        self.auth = Authenticator(db.cursor)
        self.creator = CreateAccount(db)
        self.depositor = Deposit(db)
        self.withdrawer = Withdraw(db)
        self.historian = History(db)
        self.statement = Statement(db)
        self.closer = CloseAccount(db)
        self.balance_checker = BalanceEnquiry(db)

    def login(self):
        print("\n🔐 Login Required")
        acc_num = input("🔢 Enter account number: ")
        pin = input("🔑 Enter 4-digit PIN: ")
        if self.auth.login(acc_num, pin):
            self.current_user = acc_num
            print(f"✅ Welcome, {acc_num}!")
            return True
        else:
            print("❌ Login failed.")
            choice = input("➕ Would you like to create a new account? (y/n): ")
            if choice.lower() == "y":
                self.creator.open_account()
                print("🔁 Please restart the program to log in.")
            else:
                print("👋 Exiting. Try again later.")
            return False

    def show_menu(self):
        while True:
            print("\n🏦 Main Menu")
            print("1. Create Account")
            print("2. Deposit")
            print("3. Withdraw")
            print("4. Transaction History")
            print("5. Mini Statement")
            print("6. Close Account")
            print("7. Exit")
            print("8. Re-authenticate")
            print("9. Balance Enquiry")

            choice = input("Select (1–9): ")
            if choice == "1":
                self.creator.open_account()
            elif choice == "2":
                self.depositor.deposit_amount()
            elif choice == "3":
                self.withdrawer.withdraw_amount()
            elif choice == "4":
                self.historian.show_transaction_history()
            elif choice == "5":
                self.statement.show_mini_statement()
            elif choice == "6":
                self.closer.delete_account()
            elif choice == "7":
                print(f"👋 Session ended for {self.current_user}.")
                break
            elif choice == "8":
                self.login()
            elif choice == "9":
                self.balance_checker.check_balance()
            else:
                print("❗ Invalid choice.")

def main():
    db = DBManager()
    app = BankSystem(db)
    if app.login():
        app.show_menu()

if __name__ == "__main__":
    main()
