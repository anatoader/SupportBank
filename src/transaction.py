from datetime import datetime
import re
from bs4 import BeautifulSoup, Tag
import pandas as pd


class Transaction:
    def __init__(self, date: str, amount: float, narrative: str, from_name: str, to_name: str) -> None:
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
        valid_formats = ["%d/%m/%Y", "%Y-%m-%dT%H:%M:%S"]
        for date_format in valid_formats:
            try:
                self._date = datetime.strptime(date, date_format)
                return
            except ValueError:
                continue

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

    def to_xml(self, soup: BeautifulSoup) -> Tag:
        transaction_tag = soup.new_tag('SupportTransaction', Date=self.date.isoformat())

        description_tag = soup.new_tag('Description', string=self.narrative)
        transaction_tag.append(description_tag)

        value_tag = soup.new_tag('Value', string=str(self.amount))
        transaction_tag.append(value_tag)

        parties_tag = soup.new_tag('Parties')
        parties_tag.append(soup.new_tag('From', string=self.from_name))
        parties_tag.append(soup.new_tag('To', string=self.to_name))
        transaction_tag.append(parties_tag)

        return transaction_tag

    def to_json(self) -> dict[str, str | float]:
        return   {
            "Date": self.date.isoformat(),
            "FromAccount": self.from_name,
            "ToAccount": self.to_name,
            "Narrative": self.narrative,
            "Amount": self.amount
          }

    def to_series(self) -> pd.Series:
        return pd.Series(self.to_json())

    def __str__(self) -> str:
        return (f'Date: {self.date}, '
                f'From: {self.from_name}, '
                f'To: {self.to_name}, '
                f'Narrative: {self.narrative}, '
                f'Amount: {self.amount}')
