import pandas as pd

from transaction import Transaction
from logging_utilities import init_logger
import os
from bs4 import BeautifulSoup
import json

logger = init_logger("SupportBank")


def export_transactions_to_file(transactions: list[Transaction], filename: str) -> None:
    _, file_extension = os.path.splitext(filename)

    print(file_extension)

    if file_extension == ".xml":
        _export_transactions_to_xml(transactions, filename)

    elif file_extension == ".json":
        _export_transactions_to_json(transactions, filename)

    elif file_extension == ".csv":
        _export_transactions_to_csv(transactions, filename)

    else:
        error_message = f"File extension {file_extension} not supported"
        print(error_message)
        logger.error(error_message)


def _export_transactions_to_xml(transactions: list[Transaction], filename: str) -> None:
    soup = BeautifulSoup(features="xml")

    root = soup.new_tag('TransactionList')
    soup.append(root)

    for transaction in transactions:
        root.append(transaction.to_xml(soup))

    with open(filename, "w", encoding="utf-8") as file:
        file.write(soup.prettify())

def _export_transactions_to_json(transactions: list[Transaction], filename: str) -> None:
    transactions_json = [transaction.to_json() for transaction in transactions]

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(transactions_json, file, indent=4)

def _export_transactions_to_csv(transactions: list[Transaction], filename: str) -> None:
    transactions_series = [teansaction.to_series() for teansaction in transactions]
    df = pd.DataFrame(transactions_series, columns = ["Date", "FromAccount", "ToAccount", "Narrative", "Amount"])
    df.to_csv(filename, index=False)
