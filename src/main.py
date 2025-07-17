import re
from bank import Bank

def main():
    bank = Bank()
    bank.parse_transactions_from_csv("data/Transactions2014.csv")

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