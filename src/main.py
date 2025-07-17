import re
from bank import Bank
from file_reader_utilities import read_transactions_from_file

def main():
    bank = Bank()

    transactions = read_transactions_from_file("data/Transactions2014.csv")
    bank.process_transactions(transactions)

    while True:
        print('-------------------')
        print("Available commands:")
        print("  - [List All] Outputs the names of all available accounts.")
        print("  - [List[<Account_name>]] Lists all transactions for the account associated with <Account_name>.")
        print("  - [Exit] Gracefully exits the program.")
        user_input = input("Please enter a command: ").strip()

        if user_input == "List All":
            bank.list_all_accounts()
        elif re.match(r"^List\[[a-zA-Z ]+]$", user_input):
            account_name = user_input[5:-1]
            bank.list_account_transactions(account_name)
        elif user_input == "Exit":
            print("Exiting...")
            break
        else:
            print("Invalid input. Please try again.")

if __name__ == "__main__":
    main()