import json
import os
import random
from account import Account

class BankService:
    def __init__(self, filename = "data.json"):
        self.filename = filename
        self.accounts = {}
        self.load_from_json()

    def load_from_json(self):
        if not os.path.exists(self.filename):
            self.accounts = {}
            return
        try:
            with open(self.filename, "r") as f:
                data = json.load(f)
                for acc_num, acc_data in data.items():
                    self.accounts[acc_num] = Account(
                        name=acc_data["name"],
                        account_number=acc_data["account_number"],
                        passcode=acc_data["passcode"],
                        transaction_pin=acc_data["transaction_pin"],
                        balance=acc_data["balance"],
                        history=acc_data.get("history", [])
                    )
        except (json.JSONDecodeError, FileNotFoundError):
            self.accounts = {}

    def generate_account_number(self):
        return "30" + str(random.randint(10000000, 99999999))

    def create_account(self, name, passcode, transaction_pin):
        account_number = self.generate_account_number()
        new_account = Account(name, account_number, passcode, transaction_pin)
        self.accounts[account_number] = new_account
        self.save_to_json
        return new_account

    def login(self, passcode):
        for account in self.accounts.values():
            if account.passcode == passcode:
                return account
        return None

    def save_to_json(self):
        data = {acc_num: acc.to_dict() for acc_num, acc in self.accounts.items()}
        with open(self.filename, "w") as f:
            json.dump(data, f, indent=4)

    def get_account_by_number(self, account_number):
        return self.accounts.get(account_number)

    def delete_account(self, account_number: str) -> bool:
        if account_number in self.accounts:
            del self.accounts[account_number]
            self.save_to_json()
            return True 
        else:    
            return False

        
