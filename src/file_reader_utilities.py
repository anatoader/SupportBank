from transaction import Transaction
from datetime import datetime, timedelta
import pandas as pd
import os
from logging_utilities import init_logger
import json
from bs4 import BeautifulSoup

logger = init_logger("SupportBank")


def read_transactions_from_file(filename: str) -> list[Transaction]:
    if not os.path.isfile(filename):
        logger.error(f"File {filename} does not exist")
        return []

    _, file_extension = os.path.splitext(filename)

    if file_extension == ".csv":
        return _read_transactions_from_csv(filename)

    if file_extension == ".json":
        return _read_transactions_from_json(filename)

    if file_extension == ".xml":
        return _read_transactions_from_xml(filename)

    return []


def _validate_transaction(date: str, amount: float, narrative: str, from_name: str, to_name: str) -> Transaction | None:
    try:
        return Transaction(date, amount, narrative, from_name, to_name)
    except ValueError as e:
        logger.error(f"[ERROR READING TRANSACTION] {date, from_name, to_name, narrative, amount}: {e}")

    return None


def _filter_transactions(transactions: list[Transaction]) -> list[Transaction]:
    return [transaction for transaction in transactions if transaction is not None]


def _read_transactions_from_csv(csv_filepath: str) -> list[Transaction]:
    transactions_data = pd.read_csv(csv_filepath)

    transactions = [
        _validate_transaction(row["Date"], row["Amount"], row["Narrative"], row["From"], row["To"])
        for _, row in transactions_data.iterrows()
    ]

    return _filter_transactions(transactions)


def _read_transactions_from_json(json_filepath: str) -> list[Transaction]:
    try:
        with open(json_filepath, 'r') as file:
            data = json.load(file)
    except IOError as e:
        data = {}
        logger.error(f"[ERROR READING TRANSACTIONS] {json_filepath}: {e}]")

    transactions = [
        _validate_transaction(entry["Date"], entry["Amount"], entry["Narrative"], entry["FromAccount"],
                              entry["ToAccount"])
        for entry in data
    ]

    return _filter_transactions(transactions)


def _convert_xml_date_to_datetime(xml_date: str) -> str:
    date = datetime(1899, 12, 30) + timedelta(days=int(xml_date))
    return date.strftime(format="%Y-%m-%dT%H:%M:%S")


def _read_transactions_from_xml(xml_filepath: str) -> list[Transaction]:
    try:
        with open(xml_filepath, 'r', encoding='utf-8') as f:
            data = f.read()
    except IOError as e:
        logger.error(f"[ERROR READING TRANSACTIONS] {xml_filepath}: {e}]")
        return []

    soup = BeautifulSoup(data, "xml")
    transactions_xml = soup.find_all('SupportTransaction')

    transactions = [
        _validate_transaction(
            date=_convert_xml_date_to_datetime(transaction_xml["Date"]),
            amount=transaction_xml.Value.text,
            narrative=transaction_xml.Description.text,
            from_name=transaction_xml.Parties.From.text,
            to_name=transaction_xml.Parties.To.text
        )
        for transaction_xml in transactions_xml
    ]

    return _filter_transactions(transactions)
