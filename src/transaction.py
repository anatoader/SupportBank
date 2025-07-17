class Transaction:
    def __init__(self, date: str, amount: float, narrative: str, from_name: str, to_name: str) -> None:
        self.date = date
        self.amount = amount
        self.narrative = narrative
        self.from_name = from_name
        self.to_name = to_name

    def __str__(self) -> str:
        return (f'Date: {self.date}, '
                f'From: {self.from_name}, '
                f'To: {self.to_name}, '
                f'Narrative: {self.narrative}, '
                f'Amount: {self.amount}')
