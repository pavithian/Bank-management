from auth import Authenticator

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
        except:
            print("❌ Account already exists.")
