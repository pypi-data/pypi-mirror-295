import rich
import typer
from vanty.config import config

app = typer.Typer(name="admin", help="Admin commands", no_args_is_help=True)


@app.command(help="Echo configuration settings. ")
def show_config():
    user_config = config.display()
    # echo the user config
    typer.echo(rich.print(user_config))
