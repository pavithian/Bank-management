from datetime import datetime

class Deposit:
    def __init__(self, db):
        self.db = db

    def deposit_amount(self):
        acc_num = input("🏦 Enter account number: ")
        amount = float(input("💰 Enter deposit amount: "))
        self.db.cursor.execute("UPDATE accounts SET balance = balance + ? WHERE acc_num = ?", (amount, acc_num))
        self.db.cursor.execute("INSERT INTO transactions (acc_num, type, amount, time) VALUES (?, 'Deposit', ?, ?)",
                               (acc_num, amount, datetime.now()))
        self.db.commit()
        print("✅ Deposit successful!")
