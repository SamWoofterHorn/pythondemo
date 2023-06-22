# Third-party packages
import click


@click.group()
def cli():
    pass


@cli.command()
def server():
    from pythondemo import create_app

    app = create_app()
    app.run(host="127.0.0.1", port=5002)


if __name__ == "__main__":
    cli()
