import json
from datetime import datetime, timedelta

class SmartWallet:
    def __init__(self, total_balance):
        self.total_balance = total_balance
        self.locked_balance = 0
        self.lock_expiry_time = None
        self.spending_goal = None
        self.total_spent = 0
        self.history = []
        self.lock_password = None

    def set_password(self, password):
        self.lock_password = password
        print("🔐 Lock password has been set.")
        self._log_action("set_password", 0, "Password created")

    def lock_amount(self, amount, lock_minutes):
        if self.lock_password is None:
            print("⚠️ Please set a password first using option 7.")
            return

        entered = input("Enter password to lock: ")
        if entered != self.lock_password:
            print("❌ Incorrect password. Cannot lock funds.")
            return

        if amount <= self.get_available_balance():
            self.locked_balance += amount
            self.lock_expiry_time = datetime.now() + timedelta(minutes=lock_minutes)
            print(f"₹{amount} locked until {self.lock_expiry_time.strftime('%Y-%m-%d %H:%M:%S')}")
            self._log_action("lock", amount, f"Locked for {lock_minutes} mins")
        else:
            print("❌ Insufficient balance to lock.")

    def unlock_prompt(self):
        if self.lock_password is None:
            print("⚠️ Password not set.")
            return

        entered = input("Enter password to unlock: ")
        if entered != self.lock_password:
            print("❌ Incorrect password.")
            return

        now = datetime.now()
        if self.lock_expiry_time and now >= self.lock_expiry_time:
            confirm = input("⏳ Lock expired. Unlock funds? (yes/no): ")
            if confirm.lower() == "yes":
                print(f"₹{self.locked_balance} unlocked.")
                self._log_action("unlock", self.locked_balance, "Unlocked after expiry")
                self.locked_balance = 0
                self.lock_expiry_time = None
        else:
            reason = input("🔓 Attempting early unlock. Provide reason: ")
            confirm = input("Proceed to unlock early? (yes/no): ")
            if confirm.lower() == "yes":
                print(f"⚠️ Early unlock: ₹{self.locked_balance} released.")
                self._log_action("early_unlock", self.locked_balance, reason)
                self.locked_balance = 0
                self.lock_expiry_time = None

    def set_spending_goal(self, goal_amount):
        self.spending_goal = goal_amount
        self.total_spent = 0
        print(f"🎯 Spending goal of ₹{goal_amount} set.")
        self._log_action("set_goal", goal_amount)

    def spend(self, amount):
        if amount <= self.get_available_balance():
            self.total_balance -= amount
            self.total_spent += amount
            print(f"💸 Spent ₹{amount}. Remaining: ₹{self.get_available_balance()}")
            self._log_action("spend", amount)

            if self.spending_goal and self.total_spent > self.spending_goal:
                print("⚠️ Alert: Spending goal exceeded!")
        else:
            print("❌ Insufficient available balance.")

    def get_available_balance(self):
        return self.total_balance - self.locked_balance

    def show_summary(self):
        print("\n🔒 Wallet Summary")
        print(f"Total Balance     : ₹{self.total_balance}")
        print(f"Locked Balance    : ₹{self.locked_balance}")
        print(f"Available Balance : ₹{self.get_available_balance()}")
        if self.lock_expiry_time:
            print(f"Lock Expires On   : {self.lock_expiry_time.strftime('%Y-%m-%d %H:%M:%S')}")
        if self.spending_goal:
            print(f"Spending Goal     : ₹{self.spending_goal}")
            print(f"Total Spent       : ₹{self.total_spent}")
        print()

    def _log_action(self, action, amount, note=None):
        record = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "action": action,
            "amount": amount,
            "note": note
        }
        self.history.append(record)
        self._save_history_to_file()

    def _save_history_to_file(self):
        with open("wallet_history.json", "w") as f:
            json.dump(self.history, f, indent=4)
