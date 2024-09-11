#!/usr/bin/env python
import typer
from rich.console import Console
from typing_extensions import Annotated
from pathlib import Path

from kudaflib.logic.process import metadata_process
from kudaflib.logic.utils import (
    check_filepaths_validity,
)


console = Console()


app = typer.Typer(
    pretty_exceptions_enable=True,
    pretty_exceptions_short=False,
    pretty_exceptions_show_locals=False,
)


@app.callback()
def callback():
    """
    Kudaf Metadata Tools
    """
    ...


@app.command(name='metadata')
def gen_metadata(
    config_yaml_path: Annotated[Path, typer.Option(
        help="Absolute path to the YAML configuration file"
    )] = Path.cwd() / 'config.yaml',
    output_metadata_dir: Annotated[Path, typer.Option(
        help="Absolute path to directory where the Metadata files are to be written to" 
    )] = Path.cwd(),
):
    """
    Generate Variables/UnitTypes Metadata  

    JSON metadata files ('variables.json' and maybe 'unit_types.json') will be written to the \n
    (optionally) given output directory. \n

    If any of the optional directories is not specified, the current directory is used as default.

    """
    try:
        check_filepaths_validity([config_yaml_path, output_metadata_dir])

        variables = metadata_process.generate(
            config_yaml_path, output_metadata_dir,
        )
    except Exception as e:
        console.rule("[bold red]:poop: An Exception occurred :confused:", style="red")
        console.print(e)
        console.rule(style="red")
        raise typer.Exit()

    console.rule("[bold green]:zap: Success! :partying_face:")
    console.print(f"[bold blue]Generated Metadata (Variables and UnitTypes) available at :point_right: [italic]{output_metadata_dir}[/italic][/bold blue]")
    console.rule()

    return variables
