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
