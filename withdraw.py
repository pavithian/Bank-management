from datetime import datetime

class Withdraw:
    def __init__(self, db):
        self.db = db

    def withdraw_amount(self):
        acc_num = input("🏦 Enter account number: ")
        amount = float(input("💸 Enter withdrawal amount: "))
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
