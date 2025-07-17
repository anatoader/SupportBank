from datetime import datetime
import re

class Transaction:
    def __init__(self, date: datetime, amount: float, narrative: str, from_name: str, to_name: str) -> None:
        self.date = date
        self.amount = amount
        self.narrative = narrative
        self.from_name = from_name
        self.to_name = to_name

    @property
    def date(self) -> datetime:
        return self._date

    @date.setter
    def date(self, date: str) -> None:
        if not date: raise ValueError(f"Date cannot be empty")
        try:
            self._date = datetime.strptime(date, "%d/%m/%Y")
        except ValueError:
            raise ValueError(f"Invalid date: {date}")

    @property
    def amount(self) -> float:
        return self._amount

    @amount.setter
    def amount(self, amount: float) -> None:
        if not amount: raise ValueError(f"Amount cannot be empty")
        try:
            self._amount = float(amount)
        except ValueError:
            raise ValueError(f"Invalid amount: {amount}")

    @property
    def from_name(self) -> str:
        return self._from_name

    @from_name.setter
    def from_name(self, from_name: str) -> None:
        self._from_name = Transaction._validate_name(from_name)

    @property
    def to_name(self) -> str:
        return self._to_name

    @to_name.setter
    def to_name(self, to_name: str) -> None:
        self._to_name = Transaction._validate_name(to_name)

    @staticmethod
    def _validate_name(name: str) -> str:
        if not name: raise ValueError(f"Name cannot be empty")
        if not re.match(r"^[a-zA-Z ]+$", name):
            raise ValueError(f"Invalid name: {name}")
        return name

    def __str__(self) -> str:
        return (f'Date: {self.date}, '
                f'From: {self.from_name}, '
                f'To: {self.to_name}, '
                f'Narrative: {self.narrative}, '
                f'Amount: {self.amount}')
