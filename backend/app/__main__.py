import argparse
import sys

from app.importers.fidelity_positions_importer import import_fidelity_positions
from app.importers.fidelity_transactions_importer import import_fidelity_transactions
from app.importers.schwab_lot_importer import import_schwab_lot_details
from app.importers.schwab_transactions_importer import import_schwab_transactions
from app.importers.vanguard_transactions_importer import import_vanguard_transactions
from app.services.account_service import create_account
from app.services.position_service import recalculate_positions
from app.services.price_service import fetch_and_store_prices
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

    # Recalculate positions
    recalc_parser = subparsers.add_parser("recalculate-positions")
    recalc_parser.add_argument("--email", required=True)
    recalc_parser.add_argument("--initial_load", action="store_true")

    # Fetch latest prices
    fetch_prices_parser = subparsers.add_parser("fetch-prices",
                                                help="Fetch current prices for all distinct symbols in positions.")

    args = parser.parse_args()

    if args.command == "create-user":
        create_user(args.email, args.name)

    elif args.command == "create-account":
        create_account(args.email, args.brokerage, args.account_number, args.nickname)

    elif args.command == "import":
        if args.broker.lower() == "vanguard":
            if args.format.lower() == "transactions":
                transactions = import_vanguard_transactions(args.file, args.email, args.account)
                print(len(transactions), "transactions imported.")
        if args.broker.lower() == "fidelity":
            if args.format.lower() == "positions":
                transactions = import_fidelity_positions(args.file, args.email, args.account)
                print(len(transactions), "transactions imported.")
            elif args.format.lower() == "transactions":
                transactions = import_fidelity_transactions(args.file, args.email, args.account)
                print(len(transactions), "transactions imported.")
        elif args.broker.lower() == "schwab":
            if args.format.lower() == "lot_details":
                transactions = import_schwab_lot_details(args.file, args.email, args.account)
                print(len(transactions), "transactions imported.")
                sys.exit(0)  # Exit with success code
            elif args.format.lower() == "transactions":
                transactions = import_schwab_transactions(args.file, args.email, args.account)
                print(len(transactions), "transactions imported from transactions file.")
                sys.exit(0)
            else:
                print("Unsupported format for Schwab. Use 'lot_details' or 'transactions'.")
        else:
            print("Unsupported broker or format combination.")

    elif args.command == "recalculate-positions":
        recalculate_positions(args.email, args.initial_load)
    elif args.command == "fetch-prices":
        fetch_and_store_prices()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
