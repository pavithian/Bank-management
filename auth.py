class Authenticator:
    def __init__(self, cursor):
        self.cursor = cursor

    def login(self, acc_num, pin_input):
        self.cursor.execute("SELECT pin FROM users WHERE acc_num = ?", (acc_num,))
        result = self.cursor.fetchone()
        return result and result[0] == pin_input

    def register_pin(self, acc_num, pin):
        self.cursor.execute("INSERT INTO users (acc_num, pin) VALUES (?, ?)", (acc_num, pin))
