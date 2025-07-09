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
