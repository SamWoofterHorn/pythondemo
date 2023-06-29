# Standard lib
import os

# Third-party packages
import click


@click.group()
def cli():
    pass


@cli.command()
@click.argument("mode",
                type=click.Choice(["development", "production", "test"]))
def server(mode):
    from pythondemo import create_app

    if 'FLASK_ENV' not in os.environ:
        os.environ['FLASK_ENV'] = mode

    app = create_app()
    app.run(host="0.0.0.0", port=5002)


if __name__ == "__main__":
    cli()
