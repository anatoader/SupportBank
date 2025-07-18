from transaction import Transaction
from datetime import datetime
import pandas as pd
import os
from logging_utilities import init_logger
import json

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

    return []

def _validate_transaction(date: datetime, amount: float, narrative: str, from_name: str, to_name: str) -> Transaction | None:
    try:
        return Transaction(date, amount, narrative, from_name, to_name)
    except ValueError as e:
        logger.error(f"[ERROR READING TRANSACTION] {date,from_name,to_name,narrative,amount}: {e}")

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
        _validate_transaction(entry["Date"], entry["Amount"], entry["Narrative"], entry["FromAccount"], entry["ToAccount"])
        for entry in data
    ]

    return _filter_transactions(transactions)
