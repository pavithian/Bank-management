import sqlite3
from datetime import datetime

DB_NAME = "bank.db"

# ---------- Database ----------
class DBManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_NAME)
        self.cursor = self.conn.cursor()
        self.init_db()

    def init_db(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS accounts (
            acc_num TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            balance REAL DEFAULT 0
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS users (
            acc_num TEXT PRIMARY KEY,
            pin TEXT NOT NULL
        )""")
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            acc_num TEXT,
            type TEXT,
            amount REAL,
            time TEXT
        )""")
        self.conn.commit()

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.close()


# ---------- Authentication ----------
class Authenticator:
    def __init__(self, cursor):
        self.cursor = cursor

    def login(self, acc_num, pin_input):
        self.cursor.execute("SELECT pin FROM users WHERE acc_num = ?", (acc_num,))
        result = self.cursor.fetchone()
        return result and result[0] == pin_input

    def register_pin(self, acc_num, pin):
        self.cursor.execute("INSERT INTO users (acc_num, pin) VALUES (?, ?)", (acc_num, pin))


# ---------- Features ----------
class CreateAccount:
    def __init__(self, db):
        self.db = db
        self.auth = Authenticator(db.cursor)

    def open_account(self):
        acc_num = input("📄 Enter new account number: ")
        name = input("👤 Enter account holder name: ")
        pin = input("🔑 Set 4-digit PIN: ")
        try:
            self.db.cursor.execute("INSERT INTO accounts (acc_num, name) VALUES (?, ?)", (acc_num, name))
            self.auth.register_pin(acc_num, pin)
            self.db.commit()
            print("✅ Account created successfully!")
        except sqlite3.IntegrityError:
            print("❌ Account number already exists.")


class Deposit:
    def __init__(self, db):
        self.db = db

    def deposit_amount(self):
        acc_num = input("🏦 Enter account number: ")
        amount = float(input("💰 Enter amount to deposit: "))
        self.db.cursor.execute("UPDATE accounts SET balance = balance + ? WHERE acc_num = ?", (amount, acc_num))
        self.db.cursor.execute("INSERT INTO transactions (acc_num, type, amount, time) VALUES (?, 'Deposit', ?, ?)",
                               (acc_num, amount, datetime.now()))
        self.db.commit()
        print("✅ Deposit successful!")


class Withdraw:
    def __init__(self, db):
        self.db = db

    def withdraw_amount(self):
        acc_num = input("🏦 Enter account number: ")
        amount = float(input("💸 Enter amount to withdraw: "))
        self.db.cursor.execute("SELECT balance FROM accounts WHERE acc_num = ?", (acc_num,))
        result = self.db.cursor.fetchone()
        if result and result[0] >= amount:
            self.db.cursor.execute("UPDATE accounts SET balance = balance - ? WHERE acc_num = ?", (amount, acc_num))
            self.db.cursor.execute("INSERT INTO transactions (acc_num, type, amount, time) VALUES (?, 'Withdraw', ?, ?)",
                                   (acc_num, amount, datetime.now()))
            self.db.commit()
            print("✅ Withdrawal successful!")
        else:
            print("❌ Insufficient balance or invalid account.")


class History:
    def __init__(self, db):
        self.db = db

    def show_transaction_history(self):
        acc_num = input("📜 Enter account number: ")
        self.db.cursor.execute("SELECT type, amount, time FROM transactions WHERE acc_num = ?", (acc_num,))
        rows = self.db.cursor.fetchall()
        print("📄 Transaction History:")
        for r in rows:
            print(f" - {r[0]} ₹{r[1]} on {r[2]}")


class Statement:
    def __init__(self, db):
        self.db = db

    def show_mini_statement(self):
        acc_num = input("📑 Enter account number: ")
        self.db.cursor.execute("""SELECT type, amount, time FROM transactions 
                                  WHERE acc_num = ? ORDER BY time DESC LIMIT 5""", (acc_num,))
        rows = self.db.cursor.fetchall()
        print("🧾 Mini Statement:")
        for r in rows:
            print(f" - {r[0]} ₹{r[1]} on {r[2]}")


class CloseAccount:
    def __init__(self, db):
        self.db = db

    def delete_account(self):
        acc_num = input("❌ Enter account number to close: ")
        self.db.cursor.execute("DELETE FROM users WHERE acc_num = ?", (acc_num,))
        self.db.cursor.execute("DELETE FROM transactions WHERE acc_num = ?", (acc_num,))
        self.db.cursor.execute("DELETE FROM accounts WHERE acc_num = ?", (acc_num,))
        self.db.commit()
        print("✅ Account closed successfully!")


class BalanceEnquiry:
    def __init__(self, db):
        self.db = db

    def check_balance(self):
        acc_num = input("💳 Enter account number: ")
        self.db.cursor.execute("SELECT name, balance FROM accounts WHERE acc_num = ?", (acc_num,))
        result = self.db.cursor.fetchone()
        if result:
            name, balance = result
            print(f"👤 Account Holder: {name}")
            print(f"💰 Current Balance: ₹{balance:.2f}")
        else:
            print("❌ Account not found.")


# ---------- Controller ----------
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


# ---------- Entry ----------
def main():
    db = DBManager()
    app = BankSystem(db)
    if app.login():
        app.show_menu()
    db.close()

if __name__ == "__main__":
    main()
