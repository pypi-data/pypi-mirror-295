import argparse
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description="(Lumos) Connectors CLI")
    subparsers = parser.add_subparsers(dest="command")

    scaffold_parser = subparsers.add_parser("scaffold", help="Create a new connector")
    scaffold_parser.add_argument("name", help="Name of the new connector")
    scaffold_parser.add_argument(
        "directory", type=Path, help="Directory to create the connector in"
    )

    hacking_parser = subparsers.add_parser(
        "hacking", help="Run commands for developing the `connector` library"
    )
    hacking_subparsers = hacking_parser.add_subparsers(dest="hacking_command")
    hacking_subparsers.add_parser("unasync", help="Unasync async code")

    args = parser.parse_args()

    if args.command == "scaffold":
        from connector.scaffold.create import scaffold

        scaffold(args)
    elif args.command == "hacking":
        if args.hacking_command == "unasync":
            from connector.make_sync import make_sync

            make_sync(Path(__file__).parent / "async_")
            make_sync(Path(__file__).parent / "scaffold" / "templates" / "connector" / "async_")


if __name__ == "__main__":
    main()
