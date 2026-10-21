class Account:
    def __init__(self, name, account_number, passcode, transaction_pin, balance = 0.0, history = None):
        self.name = name
        self.account_number = account_number
        self.passcode = passcode
        self.transaction_pin = transaction_pin
        self.balance = float(balance)
        self.history = history if history is not None else []

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.history.append(f"Deposited: N{amount:.2f}")
            return True
        else:
            return False

    def withdraw(self, amount):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self.history.append(f"Withdrew: N{amount: .2f}")
            return True
        else:
            return False
        
    def transfer(self, target_account, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            target_account.balance += amount
            self.history.append(f"Transferred: N{amount:.2F} to {target_account.name} {target_account.account_number}")
            target_account.history.append(f"Received N{amount:.2f} from {self.name} {self.account_number}")
            return True
        else:
            return False

    def to_dict(self):
        return {
            "account_number": self.account_number,
            "name": self.name,
            "passcode": self.passcode,
            "transaction_pin": self.transaction_pin,
            "balance": self.balance,
            "history": self.history,
        }
        
