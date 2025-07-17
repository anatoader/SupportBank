import pandas as pd
from account import Account

class Bank:
    def __init__(self) -> None:
        self.accounts = {}

    def get_or_create_account(self, name: str) -> Account:
        if name not in self.accounts:
            self.accounts[name] = Account(name)
        return self.accounts[name]

    def parse_transactions_from_csv(self, filename: str) -> None:
        transactions_data = pd.read_csv(filename)

        for _, row in transactions_data.iterrows():
            transaction = {
                "date": row["Date"],
                "amount": row["Amount"],
                "narrative": row["Narrative"],
                "from": row["From"],
                "to": row["To"]
            }

            from_account = self.get_or_create_account(row["From"])
            from_account.add_transaction(transaction)

            to_account = self.get_or_create_account(row["To"])
            to_account.add_transaction(transaction)

    def list_all_accounts(self) -> None:
        print("Available accounts:")
        for _, account in self.accounts.items():
            print(account)

    def list_account_transactions(self, name: str) -> None:
        if name not in self.accounts:
            print(f'Account {name} not found.')
        else:
            account = self.accounts[name]
            print(account)
            print("Transactions:")
            for transaction in account.transactions:
                print(f'Date: {transaction["date"]},'
                      f'From: {transaction["from"]},'
                      f'To: {transaction["to"]},'
                      f'Narrative: {transaction["narrative"]},'
                      f'Amount: {transaction["amount"]}')