from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from bank import BankService


app = FastAPI(title="E-Wallet REST API")
bank = BankService()

class AccountCreateRequest(BaseModel):
    name: str
    passcode: str
    transaction_pin: str

class DepositRequest(BaseModel):
    transaction_pin: str
    amount: float

class TransferRequest(BaseModel):
    transaction_pin: str
    target_account_number: str
    amount: float

class ChangePinRequest(BaseModel):
    current_pin: str
    new_pin: str

class HistoryRequest(BaseModel):
    transaction_pin: str

class DeleteAccountRequest(BaseModel):
    passcode: str
    transaction_pin: str


@app.post("/accounts", status_code=status.HTTP_201_CREATED)
def create_account(payload: AccountCreateRequest):
    new_account = bank.create_account(
        name=payload.name,
        passcode=payload.passcode,
        transaction_pin=payload.transaction_pin
    )
    return {
        "message": "Account created successfully",
        "account_number": new_account.account_number,
        "name": new_account.name
    }

@app.get("/accounts/{account_number}", status_code=status.HTTP_200_OK)
def get_account_details(account_number: str):
    account = bank.get_account_by_number(account_number)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account number not found"
        )
    
    return {
        "account_number": account.account_number,
        "name": account.name,
        "balance": account.balance
    }

@app.post("/accounts/{account_number}/deposit", status_code=status.HTTP_200_OK)
def deposit_funds(account_number: str, payload: DepositRequest):
    account = bank.get_account_by_number(account_number)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account number not found"
        )

    if payload.transaction_pin != account.transaction_pin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid transaction PIN"
        )

    if account.deposit(payload.amount):
        bank.save_to_json()
        return {
            "message": f"Successfully deposited N{payload.amount:.2f}",
            "account_number": account.account_number,
            "new_balance": account.balance
        }

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Deposit failed. Amount must be greater than 0"
    )

@app.post("/accounts/{account_number}/transfer", status_code=status.HTTP_200_OK)
def transfer_funds(account_number: str, payload: TransferRequest):
    sender_account = bank.get_account_by_number(account_number)
    if not sender_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sender account number not found"
        )

    target_account = bank.get_account_by_number(payload.target_account_number)
    if not target_account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Receiver account number not found"
        )

    if sender_account.account_number == target_account.account_number:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot transfer money to yourself"
        )

    if payload.transaction_pin != sender_account.transaction_pin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid transaction PIN"
        )

    if sender_account.transfer(target_account, payload.amount):
        bank.save_to_json()
        return {
            "message": f"Successfully transferred N{payload.amount:.2f} to {target_account.name}",
            "sender_account": sender_account.account_number,
            "receiver_account": target_account.account_number,
            "new_balance": sender_account.balance
        }

    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Transfer failed. Insufficient funds or invalid amount"
    )

@app.put("/accounts/{account_number}/pin", status_code=status.HTTP_200_OK)
def change_pin(account_number: str, payload: ChangePinRequest):
    account = bank.get_account_by_number(account_number)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account number not found"
        )

    if payload.current_pin != account.transaction_pin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid current PIN"
        )

    account.transaction_pin = payload.new_pin
    bank.save_to_json()
    return {"message": "Transaction PIN successfully updated"}



@app.post("/accounts/{account_number}/history", status_code=status.HTTP_200_OK)
def get_transaction_history(account_number: str, payload: HistoryRequest):
    account = bank.get_account_by_number(account_number)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account number not found"
        )

    if payload.transaction_pin != account.transaction_pin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid transaction PIN"
        )

    return {
        "account_number": account.account_number,
        "history": account.history
    }

@app.delete("/accounts/{account_number}", status_code=status.HTTP_200_OK)
def delete_account(account_number: str, payload: DeleteAccountRequest):
    account = bank.get_account_by_number(account_number)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Account number not found"
        )

    if payload.passcode != account.passcode:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid passcode"
        )

    if payload.transaction_pin != account.transaction_pin:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid transaction PIN"
        )

    if bank.delete_account(account_number):
        return {
            "message": f"This account has been permanently deleted"
        }

    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to delete account"
    )