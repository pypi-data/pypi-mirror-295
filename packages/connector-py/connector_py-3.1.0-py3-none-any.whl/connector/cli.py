import inspect
import json
import subprocess
from argparse import ArgumentParser, Namespace
from pathlib import Path
from typing import cast

from connector.capability import CapabilityName
from connector.generated import CapabilityName as OpenApiCapabilityName
from connector.helpers import collect_methods, get_pydantic_model
from connector.integration import Integration
from connector.oai.integration import Integration as OpenApiIntegration

__all__ = ("collect_commands", "run_command")


# Hacking commands
# ----------------


def _prep_hacking_command(args: Namespace):
    data = vars(args)
    data.pop("command")
    data.pop("func")
    return data


def unasync(
    sync_commands: object, directory: str = "", check: bool = False, quiet: bool = False
) -> None:
    from connector.make_sync import make_sync

    if not directory:
        _dir = Path(inspect.getfile(sync_commands.__class__)).parent.parent / "async_"
    else:
        _dir = Path(directory)

    success = make_sync(Path(_dir), check=check, quiet=quiet)
    if check:
        if not quiet:
            print("Unasync check complete")
        exit(bool(not success))
    else:
        if not quiet:
            print("Unasync complete")


def http_command_server(async_commands: object, port: int = 8000):
    from connector.http_server import collect_routes, runserver

    router = collect_routes(async_commands)
    try:
        runserver(router, port)
    except KeyboardInterrupt:
        pass


def http_integration_server(integration: Integration | OpenApiIntegration, port: int = 8000):
    from connector.http_server import collect_integration_routes, runserver

    router = collect_integration_routes(integration)
    try:
        runserver(router, port)
    except KeyboardInterrupt:
        pass


def build_executable(path: str) -> None:
    try:
        subprocess.run(["pyinstaller", "--version"], check=True)
    except FileNotFoundError:
        print("PyInstaller not found in PATH. Please pip install pyinstaller")
        return

    command = [
        "pyinstaller",
        path,
        "--noconsole",
        "--onefile",
        "--clean",
        "--paths=projects/libs/python",
    ]
    if __file__ not in "site-packages":
        command.append("--paths=projects/libs/python")
    subprocess.run(command)


def run_test():
    subprocess.run(["pytest", "tests/"], check=True)


def create_command_hacking_parser(
    sync_commands: object, async_commands: object, parser: ArgumentParser
) -> None:
    subparsers = parser.add_subparsers(dest="command")

    unasync_parser = subparsers.add_parser("unasync")
    unasync_parser.add_argument(
        "--directory",
        "-d",
        type=str,
        help="The directory to unasync. Defaults to the async_ directory in the connector.",
    )
    unasync_parser.add_argument(
        "--check",
        "-c",
        action="store_true",
        help="Check if the async functions can be converted to sync.",
    )
    unasync_parser.add_argument(
        "--quiet", "-q", action="store_true", help="Do not print anything to the console."
    )
    unasync_parser.set_defaults(
        func=lambda args: unasync(sync_commands, **_prep_hacking_command(args))
    )

    http_server_parser = subparsers.add_parser("http-server")
    http_server_parser.add_argument(
        "--port", "-p", type=int, default=8000, help="The port to run the server on."
    )
    http_server_parser.set_defaults(
        func=lambda args: http_command_server(async_commands, **_prep_hacking_command(args))
    )

    build_executable_parser = subparsers.add_parser(
        "build-executable",
        help=(
            "Create a single file executable with PyInstaller. Provide the path to your library's"
            " main.py file."
        ),
    )
    build_executable_parser.add_argument("path", type=str, help="The path to the main.py file.")
    build_executable_parser.set_defaults(
        func=lambda args: build_executable(**_prep_hacking_command(args))
    )

    test_parser = subparsers.add_parser("test")
    test_parser.set_defaults(func=lambda args: run_test())

    return None


def create_integration_hacking_parser(
    integration: Integration | OpenApiIntegration, parser: ArgumentParser
) -> None:
    subparsers = parser.add_subparsers(dest="command")

    http_server_parser = subparsers.add_parser("http-server")
    http_server_parser.add_argument(
        "--port", "-p", type=int, default=8000, help="The port to run the server on."
    )
    http_server_parser.set_defaults(
        func=lambda args: http_integration_server(integration, **_prep_hacking_command(args))
    )

    build_executable_parser = subparsers.add_parser(
        "build-executable",
        help=(
            "Create a single file executable with PyInstaller. Provide the path to your library's"
            " main.py file."
        ),
    )
    build_executable_parser.add_argument("path", type=str, help="The path to the main.py file.")
    build_executable_parser.set_defaults(
        func=lambda args: build_executable(**_prep_hacking_command(args))
    )

    test_parser = subparsers.add_parser("test")
    test_parser.set_defaults(func=lambda args: run_test())

    return None


# Actual Commands
# ---------------


def _print_pydantic(model):
    # Pydantic v2
    if hasattr(model, "model_dump_json"):
        print(model.model_dump_json())
    # Pydantic v1
    elif hasattr(model, "json"):
        print(model.json())
    elif type(model) in (dict, list):
        print(json.dumps(model))
    else:
        print(model)


def _print_decorator(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        if isinstance(result, list):
            for item in result:
                _print_pydantic(item)
        else:
            _print_pydantic(result)
        return result

    return wrapper


def command_executor(sync_commands: object, args: Namespace):
    """Executes a command from the CLI."""
    method = getattr(sync_commands, cast(str, args.command).replace("-", "_"))
    try:
        model_cls = get_pydantic_model(method.__annotations__)
    except ValueError:
        model_cls = None

    if model_cls:
        try:
            model = model_cls.model_validate_json(args.json)
        except AttributeError:
            model = model_cls.parse_raw(args.json)
        output = method(model)
    else:
        output = method()
    _print_pydantic(output)


def capability_executor(integration: Integration | OpenApiIntegration, args: Namespace):
    """Executes a command from the CLI."""
    if isinstance(integration, OpenApiIntegration):
        output = integration.dispatch(OpenApiCapabilityName(args.command), args.json)
    else:
        output = integration.dispatch(CapabilityName(args.command), args.json)
    print(output)


def collect_commands(
    sync_commands: object, async_commands: object, no_print: bool = False
) -> ArgumentParser:
    """
    Collect all methods from an object and create a CLI command for each.
    The object must be instantiated.
    """
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    commands = collect_methods(sync_commands)
    for method in commands:
        subparser = subparsers.add_parser(
            method.__name__.replace("_", "-"), description=method.__doc__
        )

        try:
            get_pydantic_model(method.__annotations__)
        except ValueError:
            pass
        else:
            subparser.add_argument("--json", type=str, help="JSON input", required=True)

        subparser.set_defaults(func=lambda args: command_executor(sync_commands, args))

    hacking_subparser = subparsers.add_parser("hacking")
    create_command_hacking_parser(sync_commands, async_commands, hacking_subparser)

    return parser


def collect_capabilities(
    integration: Integration | OpenApiIntegration, no_print: bool = False
) -> ArgumentParser:
    """
    Collect all methods from an Integration class and create a CLI
    command for each.
    """
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest="command")

    subparser = subparsers.add_parser("info", description=integration.info.__doc__)
    subparser.set_defaults(func=lambda args: command_executor(integration, args))

    for capability_name, capability in integration.capabilities.items():
        subparser = subparsers.add_parser(capability_name.value, description=capability.__doc__)

        try:
            get_pydantic_model(capability.__annotations__)
        except ValueError:
            pass
        else:
            subparser.add_argument("--json", type=str, help="JSON input", required=True)

        subparser.set_defaults(func=lambda args: capability_executor(integration, args))

    hacking_subparser = subparsers.add_parser("hacking")
    create_integration_hacking_parser(integration, hacking_subparser)

    return parser


def run_command(sync_commands: object, async_commands: object, no_print: bool = False) -> None:
    """Run a command from the CLI."""
    parser = collect_commands(sync_commands, async_commands, no_print)
    args = parser.parse_args()
    args.func(args)


def run_integration(
    integration: Integration | OpenApiIntegration,
    no_print: bool = False,
) -> None:
    """Run a command from the CLI, integratin version."""
    parser = collect_capabilities(integration, no_print)
    args = parser.parse_args()
    args.func(args)
