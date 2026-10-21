import stdiomask
from bank import BankService


def dashboard_session(account, bank):
    while True:
        print("---------------------------------------------------------------\n"
                      "What do you want to do today?\n"
              "---------------------------------------------------------------\n"
              "1. Deposit \n"
              "2. Transfer \n"
              "3. Check Balance \n"
              "4. Change Transaction Pin \n"
              "5. Check Transaction History \n"
              "6. Delete Account \n"
              "7. Log Out")
        action = input("Pick one between (1-7); ").strip()
        if action == "1":
            pin = stdiomask.getpass(prompt="Enter your pin: ", mask="*").strip()
            if pin == account.transaction_pin:
                try:
                    amount = float(input("Enter the amount you want to deposit: "))
                    if account.deposit(amount):
                        bank.save_to_json()
                        print(f"Deposit Successful!\nYour current account balance is N{account.balance:.2f}")
                    else:
                        print("Deposit failed. Amount must be greater than 0.")
                except ValueError:
                    print("Invalid Amount Entered.")
            else:
                print("Invalid Pin")
        elif action == "2":
            target_acc_num = input("Enter Receiver's Account Number: ").strip()
            target_account = bank.get_account_by_number(target_acc_num)
            if target_account is None:
                print('Receiver account not found')
            elif target_account.account_number == account.account_number:
                print("You can not transfer money to yourself")
            else:
                pin = stdiomask.getpass(prompt="Enter your pin: ", mask="*").strip()
                if pin == account.transaction_pin:
                    try:
                        amount = float(input(f"Enter the amount you want to transfer to {target_account.name}: "))
                        if account.transfer(target_account, amount):
                            bank.save_to_json()
                            print(f"You have succesfully transferred N{amount:.2f} to {target_account.name}!")
                            print(f"You account balance is N{account.balance:.2f}")
                        else:
                            print("Insufficient funds! Fund Your Account and Try again")
                    except ValueError:
                        print("Invalid Amount Entered")
                else:
                    print("Invalid pin")
        elif action == "3":
            pin = stdiomask.getpass(prompt="Enter your pin: ", mask="*").strip()
            if pin == account.transaction_pin:
                print(f"Your current account balance is N{account.balance}")
            else:
                print("Invalid Pin")
        elif action == "4":
            pin = stdiomask.getpass(prompt="Enter your current pin: ", mask="*").strip()
            if  pin == account.transaction_pin:
                while True:
                    new_pin = stdiomask.getpass(prompt="Enter a new 4 digit pin: ", mask="*").strip()
                    confirm_new_pin = stdiomask.getpass(prompt="Enter a new 4 digit pin: ", mask="*").strip()
                    if new_pin == confirm_new_pin:
                        break
                    else:
                        print("Pins do not match. Try again!")
                account.transaction_pin = new_pin
                bank.save_to_json()
                print("You have succesfully changed your pin")
            else:
                print("Invalid Pin")
        elif action == "5":
            pin = stdiomask.getpass(prompt="Enter your current pin: ", mask="*").strip()
            if  pin == account.transaction_pin:
                print("\n--- TRANSACTION HISTORY ---")
                if not account.history:
                    print("No transactions yet.")
                else:
                    for item in account.history:
                        print(f"- {item}")
                print("---------------------------\n")
            else:
                print("Invalid Pin")
        elif action == "6":
            confirm = input("Are you sure you want to delete your account? (yes/no): ").strip().lower()
            if confirm == "yes":
                pin = stdiomask.getpass(prompt="Enter your transaction pin to confirm deletion: ", mask="*").strip()
                if pin == account.transaction_pin:
                    if bank.delete_account(account.account_number):
                        print("Your account has been permanently deleted. Logging out...")
                        break
                    else:
                        print("Failed to delete account.")
                else:
                    print("Invalid Pin. Account deletion canceled.")
            else:
                print("Account deletion canceled.")

        elif action == "7":
            print("Logging Out........")
            break
        else:
            print("Pick A Valid Option from 1 - 7")


def main():
    
    bank = BankService()

    while True:
        print("---------------------------------------------------------------\n"
            "             WELCOME TO MY E-WALLET SERVICE\n"
            "---------------------------------------------------------------\n"
            "1. Sign UP (Create a New Account)\n"
            "2. Login\n"
            "3. Exit\n"
            "---------------------------------------------------------------")
        choice = input("Pick what you want to do from the list: ").strip()
        if choice == "1":
            name = input("Enter your full name: ")
            while True:
                passcode = stdiomask.getpass(prompt="Enter your passcode: ", mask="*").strip()
                confirm_passcode = stdiomask.getpass(prompt = "Confirm your passcode: ", mask="*").strip()
                if passcode == confirm_passcode:
                    break
                else:
                    print("Password do no match!")
            while True:
                pin = stdiomask.getpass(prompt="Enter your pin: ", mask="*").strip()
                confirm_pin = stdiomask.getpass(prompt="Confirm your pin: ", mask="*").strip()
                if pin == confirm_pin:
                    break
                else:
                    print("Pin do not match")
            account = bank.create_account(name=name, passcode=passcode, transaction_pin=pin)
            print(f"You have succesfully created a new account. Below are your account details:\n"
                f"{name}\n"
                f"{account.account_number}")
        elif choice == "2":
            passcode = stdiomask.getpass(prompt="Enter your passcode: ", mask="*").strip()
            account = bank.login(passcode=passcode)
            if account is not None:
                print("Login Successful!\n"
                    f"Welcome {account.name}\n" 
                    f"Account Number = {account.account_number}")
                dashboard_session(account, bank)
            else:
                print("Invalid Passcode")
        elif choice == "3":
            print("Thank you for using this E-Wallet service.\n Goodbye!")
            break
        else:
            print("Invalid Selection, Pick either 1, 2 or 3")




if __name__ == "__main__":
    main()