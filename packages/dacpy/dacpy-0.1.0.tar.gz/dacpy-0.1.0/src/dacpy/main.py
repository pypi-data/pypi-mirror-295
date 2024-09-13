from typing import Annotated

import typer
from typer import Typer
from rich import print
from dacpy.__version__ import __version__

app = Typer(name="dacpy")


@app.command(name="sync")
def sync_playlists(playlist: Annotated[str, typer.Option("--name", "-n")]):
    # check if module spotipy is installed
    try:
        from dacpy.sync import main
    except ImportError:
        print("[red]Please install dacpy with the `spotipy` extra: `uv tool install dacpy[spotipy]`")
    else:
        main(playlist)


@app.command()
def version():
    print(__version__)


if __name__ == "__main__":
    app()
