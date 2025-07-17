class Account:
    def __init__(self, name: str):
        self.name = name
        self.balance = 0
        self.transactions = []

    def add_transaction(self, transaction: dict[str, str | float]) -> None:
        if transaction["from"] == self.name:
            self.balance += transaction["amount"]
        elif transaction["to"] == self.name:
            self.balance -= transaction["amount"]
        else:
            raise Exception(f'Transaction source {transaction["from"]} or destination {transaction["to"]} do not match the account.')

        self.transactions.append(transaction)

    def __str__(self) -> str:
        return f"Name: {self.name}, balance: {self.balance}"
