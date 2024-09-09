# This file is part of fm-weck: executing fm-tools in containerized environments.
# https://gitlab.com/sosy-lab/software/fm-weck
#
# SPDX-FileCopyrightText: 2024 Dirk Beyer <https://www.sosy-lab.org>
#
# SPDX-License-Identifier: Apache-2.0

import argparse
import logging
import os
from argparse import Namespace
from dataclasses import dataclass
from functools import cache
from pathlib import Path
from typing import Any, Callable, Optional, Tuple, Union

from fm_tools.benchexec_helper import DataModel

from fm_weck import Config
from fm_weck.config import _SEARCH_ORDER
from fm_weck.resources import iter_fm_data, iter_properties

from . import __version__
from .engine import Engine, NoImageError
from .serve import run_guided, run_manual, setup_fm_tool

logger = logging.getLogger(__name__)


@dataclass
class ToolQualifier:
    tool: Union[str, Path]
    version: Optional[str]

    def __init__(self, qualifier: str):
        """
        The string is of the form <tool>[:<version>]. Tool might be a path.
        """

        self.tool = qualifier.split(":")[0]

        self.version = None
        try:
            self.version = qualifier.split(":")[1]
        except IndexError:
            # No version given
            return


def add_tool_arg(parser, nargs="?"):
    parser.add_argument(
        "TOOL",
        help="The tool to obtain the container from. Can be the form <tool>:<version>. "
        "The TOOL is either the name of a bundled tool (c.f. fm-weck --list) or "
        "the path to a fm-tools yaml file.",
        type=ToolQualifier,
        nargs=nargs,
    )


def add_shared_args_for_run_modes(parser):
    parser.add_argument(
        "--skip-download",
        action="store_true",
        help="Do not download the fm-tool, even if it is not available in the cache.",
    )

    add_tool_arg(parser, nargs=None)


def parse(raw_args: list[str]) -> Tuple[Callable[[], None], Namespace]:
    parser = argparse.ArgumentParser(description="fm-weck")

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
    )
    parser.add_argument(
        "--config",
        action="store",
        type=Path,
        help="Path to the configuration file.",
        default=None,
    )

    parser.add_argument(
        "--loglevel",
        choices=["debug", "info", "warning", "error", "critical"],
        action="store",
        default=None,
        help="Set the log level.",
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List all fm-tools that can be called by name.",
        required=False,
        default=False,
    )

    subparsers = parser.add_subparsers()

    run = subparsers.add_parser("run", aliases=["r"], help="Run a verifier inside a container.")

    # guided mode
    run.add_argument(
        "-p",
        "--property",
        "--spec",
        action="store",
        help=(
            "Property to that is forwarded to the fm-tool."
            " Either a path to a property file or a property name from SV-COMP or Test-Comp."
            " Use fm-weck serve --list to see all properties that can be called by name."
        ),
        required=False,
        default=None,
    )

    run.add_argument(
        "-d",
        "--data-model",
        action="store",
        choices=list(DataModel),
        help="The data model that shall be used.",
        required=False,
        type=lambda dm: DataModel[dm],
        default=DataModel.LP64,
    )

    run.add_argument(
        "-w",
        "--witness",
        action="store",
        help="A witness that shall be passed to the tool.",
        required=False,
        default=None,
    )

    add_shared_args_for_run_modes(run)

    run.add_argument("files", metavar="FILES", nargs="+", help="Files to pass to the tool")
    run.add_argument(
        "argument_list",
        metavar="args",
        nargs="*",
        help="Additional arguments for the fm-tool." " To add them, separate them with '--' from the files.",
    )
    run.set_defaults(main=main_run)

    expert = subparsers.add_parser(
        "expert",
        aliases=["e", "m"],
        help="Manually run a verifier inside a container."
        "Arguments are passed verbatim to the tool, so expert-ise about it's command line is required.",
    )

    add_shared_args_for_run_modes(expert)

    expert.add_argument("argument_list", metavar="args", nargs="*", help="Arguments for the fm-tool")
    expert.set_defaults(main=main_manual)

    shell = subparsers.add_parser("shell", help="Start an interactive shell inside the container.")

    shell.add_argument("--entry", action="store", help="The entry point of the shell.", default="/bin/bash")

    add_tool_arg(shell)
    shell.set_defaults(main=main_shell)

    install = subparsers.add_parser("install", aliases=["i"], help="Download and unpack a TOOL for later use.")
    add_tool_arg(install, nargs="+")
    install.set_defaults(main=main_install)

    def help_callback():
        parser.print_help()

    result, left_over = parser.parse_known_args(raw_args)

    if not left_over:
        # Parsing went fine
        return help_callback, result

    # Find the first offending argument and insert "--" before it
    # We do this to allow the user to pass arguments to the fm-tool without
    # having to specify the pseudo argument "--"
    idx = raw_args.index(left_over[0])
    raw_args.insert(idx, "--")

    return help_callback, parser.parse_args(raw_args)


@cache
def fm_tools_choice_map():
    ignore = {
        "schema.yml",
    }

    actors = {actor_def.stem: actor_def for actor_def in iter_fm_data() if (actor_def.name not in ignore)}

    return actors


@cache
def property_choice_map():
    return {spec_path.stem: spec_path for spec_path in iter_properties() if spec_path.suffix != ".license"}


def list_known_tools():
    return fm_tools_choice_map().keys()


def list_known_properties():
    return property_choice_map().keys()


def resolve_tool(tool: ToolQualifier) -> Path:
    tool_name = tool.tool
    if (as_path := Path(tool_name)).exists() and as_path.is_file():
        return as_path

    return fm_tools_choice_map()[tool_name]


def resolve_property(prop_name: str) -> Path:
    if (as_path := Path(prop_name)).exists() and as_path.is_file():
        return as_path

    return property_choice_map()[prop_name]


def set_log_level(loglevel: Optional[str], config: dict[str, Any]):
    level = "WARNING"
    level = loglevel.upper() if loglevel else config.get("logging", {}).get("level", level)
    logging.basicConfig(level=level)
    logging.getLogger("httpcore").setLevel("WARNING")


def main_run(args: argparse.Namespace):
    if not args.TOOL:
        logger.error("No fm-tool given. Aborting...")
        return 1
    try:
        fm_data = resolve_tool(args.TOOL)
    except KeyError:
        logger.error("Unknown tool %s", args.TOOL)
        return 1

    try:
        property_path = resolve_property(args.property) if args.property else None
    except KeyError:
        logger.error("Unknown property %s", args.property)
        return 1

    run_guided(
        fm_tool=fm_data,
        version=args.TOOL.version,
        configuration=Config(),
        prop=property_path,
        program_files=args.files,
        additional_args=args.argument_list,
        data_model=args.data_model,
        skip_download=args.skip_download,
    )


def main_manual(args: argparse.Namespace):
    if not args.TOOL:
        logger.error("No fm-tool given. Aborting...")
        return 1
    try:
        fm_data = resolve_tool(args.TOOL)
    except KeyError:
        logger.error("Unknown tool %s", args.TOOL)
        return 1

    run_manual(
        fm_tool=fm_data,
        version=args.TOOL.version,
        configuration=Config(),
        command=args.argument_list,
        skip_download=args.skip_download,
    )


def main_install(args: argparse.Namespace):
    for tool in args.TOOL:
        try:
            fm_data = resolve_tool(tool)
        except KeyError:
            logger.error("Unknown tool %s. Skipping installation...", tool)
            continue

        setup_fm_tool(
            fm_tool=fm_data,
            version=tool.version,
            configuration=Config(),
        )


def main_shell(args: argparse.Namespace):
    if not args.TOOL:
        engine = Engine.from_config(Config())
    else:
        try:
            fm_data = resolve_tool(args.TOOL)
        except KeyError:
            logger.error("Unknown tool %s", args.fm_data)
            return 1
        engine = Engine.from_config(fm_data, args.TOOL.version, Config())
    engine.interactive = True
    engine.run(args.entry)


def log_no_image_error(tool, config):
    order = []
    for path in _SEARCH_ORDER:
        if path.is_relative_to(Path.cwd()):
            order.append(str(path.relative_to(Path.cwd())))
        else:
            order.append(str(path))

    text = ""
    if tool:
        text = f"{os.linesep}No image specified in the fm-tool yml file for {tool.tool}."
    else:
        text = f"{os.linesep}No image specified."
    if config is None:
        text += f"""
There is currently no configuration file found in the search path.
The search order was 
{os.linesep.join(order)}
Please specify an image in the fm-tool yml file or add a configuration.

To add a configuration you can do the following (on POSIX Terminals):

printf '[defaults]\\nimage = "<your_image>"' > .weck

Replace <your_image> with the image you want to use.
        """
        logger.error(text)
        return

    text = """
No image specified in the fm-tool yml file for %s nor in the configuration file %s.
Please specify an image in the fm-tool yml file or in the configuration file.
To specify an image add

[defaults]
image = "your_image"

to your .weck file.
    """

    logger.error(text, tool, config)


def cli(raw_args: list[str]):
    help_callback, args = parse(raw_args)
    configuration = Config().load(args.config)
    set_log_level(args.loglevel, configuration)

    if args.list:
        print("List of fm-tools callable by name:")
        for tool in sorted(list_known_tools()):
            print(f"  - {tool}")
        print("\nList of properties callable by name:")
        for prop in sorted(list_known_properties()):
            print(f"  - {prop}")
        return

    if not hasattr(args, "TOOL"):
        return help_callback()

    try:
        args.main(args)
    except NoImageError:
        log_no_image_error(args.TOOL, Config()._config_source)
        return 1
