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
