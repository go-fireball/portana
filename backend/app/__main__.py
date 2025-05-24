import argparse

from app.importers.schwab_lot_importer import import_schwab_lot_details
from app.services.account_service import create_account
from app.services.user_service import create_user


def main():
    parser = argparse.ArgumentParser(description="Import financial data or create user/account.")
    subparsers = parser.add_subparsers(dest="command")

    # Create user
    user_parser = subparsers.add_parser("create-user")
    user_parser.add_argument("--email", required=True)
    user_parser.add_argument("--name", required=True)

    # Create account
    account_parser = subparsers.add_parser("create-account")
    account_parser.add_argument("--email", required=True)
    account_parser.add_argument("--brokerage", required=True, choices=["schwab", "fidelity", "vanguard"])
    account_parser.add_argument("--account_number", required=True)
    account_parser.add_argument("--nickname", default="")

    # Import file
    import_parser = subparsers.add_parser("import")
    import_parser.add_argument("--broker", required=True, choices=["schwab", "fidelity", "vanguard"])
    import_parser.add_argument("--format", required=True)
    import_parser.add_argument("--email", required=True)
    import_parser.add_argument("--account", required=True)
    import_parser.add_argument("--file", required=True)

    args = parser.parse_args()

    if args.command == "create-user":
        create_user(args.email, args.name)

    elif args.command == "create-account":
        create_account(args.email, args.brokerage, args.account_number, args.nickname)

    elif args.command == "import":
        if args.broker.lower() == "schwab" and args.format.lower() == "lot_details":
            transactions = import_schwab_lot_details(args.file, args.email, args.account)
            for txn in transactions:
                print(txn)
        else:
            print("Unsupported broker or format combination.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
