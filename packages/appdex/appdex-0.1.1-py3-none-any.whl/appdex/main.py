import logging

import typer
import questionary

import appdex.install as install
from appdex.log import TyperLoggerHandler, parse_log_level

app = typer.Typer()
app.add_typer(install.app, name="install")
app_list = [f for f in dir(install) if
            not f.startswith("__") and not f in install.excluded_attributes["symbols"] and not f in
                                                                                               install.excluded_attributes[
                                                                                                   "imports"]]


@app.command()
def ls():
    typer.echo("Available apps:")
    for app_name in app_list:
        typer.echo(f"- {app_name}")


@app.callback(invoke_without_command=True)
def main(ctx: typer.Context, verbose: bool = typer.Option(False, "--verbose", "-v"),
         log_level: str = typer.Option("INFO", "--log-level", "-l")):
    if log_level:
        log_level = log_level.upper()
        if log_level not in ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]:
            logging.error(f"Invalid log level: {log_level} is not one of DEBUG, INFO, WARNING, ERROR, CRITICAL")
            raise typer.Exit(code=1)
        logging.getLogger().setLevel(parse_log_level(log_level))
        logging.debug(f"Log level set to {log_level}")

    if verbose:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Verbose mode enabled")
        logging.debug(f"Log level set to DEBUG")

    if ctx.invoked_subcommand is not None:
        return

    input_choices = questionary.checkbox(
        'Select apps',
        choices=["all"] + app_list,
    ).ask()

    if input_choices is None:
        raise typer.Exit()

    if "all" in input_choices:
        input_choices = app_list

    for step in input_choices:
        func = getattr(install, step)
        if func is None:
            logging.error(f"Invalid option: {step}")
            raise typer.Exit(code=1)
        typer.run(func)

    logging.info("Done")
    raise typer.Exit()


if __name__ == "__main__":
    typer_handler = TyperLoggerHandler()
    logging.basicConfig(level=logging.INFO, handlers=(typer_handler,))
    app()
