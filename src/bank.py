from account import Account
from transaction import Transaction
import itertools
from file_writer_utilities import export_transactions_to_file

class Bank:
    def __init__(self) -> None:
        self.accounts = {}

    def get_or_create_account(self, name: str) -> Account:
        if name not in self.accounts:
            self.accounts[name] = Account(name)
        return self.accounts[name]

    def process_transactions(self, transactions: list[Transaction]) -> None:
        for transaction in transactions:
            from_account = self.get_or_create_account(transaction.from_name)
            from_account.add_transaction(transaction)

            to_account = self.get_or_create_account(transaction.to_name)
            to_account.add_transaction(transaction)

    def get_all_transactions(self) -> list[Transaction]:
        return list(itertools.chain(*[account.transactions for _, account in self.accounts.items()]))

    def export_transactions(self, filename: str) -> None:
        transactions = self.get_all_transactions()
        export_transactions_to_file(transactions, filename)

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
                print(transaction)
