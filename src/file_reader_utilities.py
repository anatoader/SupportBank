from transaction import Transaction
import pandas as pd
import os

def read_transactions_from_file(filename: str) -> list[Transaction]:
    _, file_extension = os.path.splitext(filename)
    if file_extension == ".csv":
        return _read_transactions_from_csv(filename)

    return []

def _read_transactions_from_csv(csv_filepath: str) -> list[Transaction]:
    transactions_data = pd.read_csv(csv_filepath)

    return [
        Transaction(row["Date"], row["Amount"], row["Narrative"], row["From"], row["To"])
        for _, row in transactions_data.iterrows()
    ]
