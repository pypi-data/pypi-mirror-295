"""
All connector implementations must implement both sync and async versions of the connector.
The easiest way is to create the async version and use "unasync" to generate the sync version.
"""

import filecmp
import tempfile
from pathlib import Path

import unasync

__all__ = ("make_sync", "walk", "Rule")


def walk(path: Path):
    """Recursively walk a directory and yield all files."""
    for p in Path(path).iterdir():
        if p.is_dir():
            yield from walk(p)
            continue
        yield p.resolve()


class Rule(unasync.Rule):
    """Custom unasync rule for easier handling of token replacements"""


def make_sync(
    async_dir: Path,
    rules: list[Rule] | None = None,
    additional_replacements: dict[str, str] | None = None,
    *,
    check: bool = False,
    quiet: bool = False,
) -> bool:
    """
    Generate sync versions of async files.
    :param async_dir: Path to the directory containing the async files.
    :param rules: List of unasync rules.
    :param additional_replacements: Additional tokens to replace.
    :param check: Check if the generated files are different from the existing ones.
    Pass in your usual arguments for rules or leave blank.
    :param quiet: Suppress console output.
    :return: whether operation was successful
    """
    if not rules:
        rules = [unasync.Rule("/async_/", "/sync_/")]
    else:
        assert all(
            isinstance(rule, Rule) for rule in rules
        ), "Rules must be of custom Rule from connector.make_sync."

    if not additional_replacements:
        additional_replacements = {
            # httpx
            "AsyncClient": "Client",
            # pathlib
            "AsyncOAuth2Client": "OAuth2Client",
            # integrations
            "async_integration": "sync_integration",
            # imports
            "async_": "sync_",
        }
    for rule in rules:
        rule.token_replacements.update(additional_replacements)

    if check:
        success = True
        for x in walk(async_dir):
            if x.suffix != ".py":
                continue
            async_file = str(x.absolute())
            with tempfile.TemporaryDirectory() as tmp_dir_str:
                temp_dir = Path(tmp_dir_str)
                new_rules = []
                for rule in rules:
                    new_rule = Rule(
                        fromdir=str(Path(async_file).parent.absolute()), todir=str(temp_dir)
                    )
                    new_rule.token_replacements = rule.token_replacements
                    new_rules.append(new_rule)
                unasync.unasync_files([async_file], rules=new_rules)

                for rule in rules:
                    sync_file = Path(async_file.replace(rule.fromdir, rule.todir))
                    if sync_file.exists():
                        break
                else:
                    success = False
                    if not quiet:
                        print(
                            f"Sync file for {Path(async_file).relative_to(async_dir.parent)} does "
                            f"not exist"
                        )
                    continue
                if not filecmp.cmp(temp_dir / x.name, sync_file):
                    success = False
                    if not quiet:
                        print(
                            f"Sync file for {Path(async_file).relative_to(async_dir.parent)} is "
                            f"different"
                        )

        return success

    unasync.unasync_files(
        [str(x.absolute()) for x in walk(async_dir) if x.suffix == ".py"], rules=rules
    )
    return True
