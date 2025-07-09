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
