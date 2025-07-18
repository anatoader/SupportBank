from transaction import Transaction


class Account:
    def __init__(self, name: str):
        self.name = name
        self.balance = 0
        self.transactions = []

    def add_transaction(self, transaction: Transaction) -> None:
        if transaction.from_name == self.name:
            self.balance += transaction.amount
        elif transaction.to_name == self.name:
            self.balance -= transaction.amount
        else:
            raise Exception(f'Transaction source {transaction["from"]} or destination {transaction["to"]} do not match the account.')

        self.transactions.append(transaction)

    def __str__(self) -> str:
        return f"Name: {self.name}, balance: {self.balance}"
