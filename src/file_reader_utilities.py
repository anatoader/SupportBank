from transaction import Transaction
from datetime import datetime
import pandas as pd
import os
from logging_utilities import init_logger

logger = init_logger("SupportBank")

def read_transactions_from_file(filename: str) -> list[Transaction]:
    _, file_extension = os.path.splitext(filename)
    if file_extension == ".csv":
        return _read_transactions_from_csv(filename)

    return []

def _validate_transaction(date: datetime, amount: float, narrative: str, from_name: str, to_name: str) -> Transaction | None:
    try:
        return Transaction(date, amount, narrative, from_name, to_name)
    except ValueError as e:
        logger.error(f"[ERROR READING TRANSACTION] {date,from_name,to_name,narrative,amount}: {e}")

    return None

def _read_transactions_from_csv(csv_filepath: str) -> list[Transaction]:
    transactions_data = pd.read_csv(csv_filepath)

    transactions = [
        _validate_transaction(row["Date"], row["Amount"], row["Narrative"], row["From"], row["To"])
        for _, row in transactions_data.iterrows()
    ]

    return [transaction for transaction in transactions if transaction is not None]
