"""Main entrypoint for the application."""

import typer
from dotenv import load_dotenv
from promptarchitect.tracing import LogProcessor
import logging

from promptarchitect.analysis import cli as analysis_cli
from promptarchitect.validation import cli as validation_cli

app = typer.Typer(rich_markup_mode=True)

app.add_typer(analysis_cli.app, name="analyze")
app.add_typer(validation_cli.app, name="test")

if __name__ == "__main__":
    load_dotenv()
    log_processor = LogProcessor()
    root_logger = logging.getLogger()

    root_logger.addHandler(log_processor)
    root_logger.setLevel(logging.INFO)

    app()
