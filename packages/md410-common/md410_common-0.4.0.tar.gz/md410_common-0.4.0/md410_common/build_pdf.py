""" Build a PDF document from the supplied path to a markdown file and Docker container

"""
__author__ = "K van Wyk"
__version__ = "0.0.1"
import os.path
from pathlib import Path

import rich_click as click
import docker
from rich import print

CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def build_pdf(source: Path, image: str, pull: bool = False, debug: bool = False):
    """Read SOURCE file and write an equivalently named PDF file to SOURCE's dir by invoking docker IMAGE"""
    source = source.absolute()
    client = docker.from_env()
    volumes = {source.parent: {"bind": "/io", "mode": "rw"}}
    if pull:
        if debug:
            print(f"[yellow]Pulling {image}[/]")
        client.images.pull(image)
        if debug:
            print(f"[green]Done pulling {image}[/]")

    client.containers.run(
        image,
        name="md410_pdf_creator",
        command=f"/io/{source.name}",
        volumes=volumes,
        auto_remove=True,
        stdout=True,
        stderr=True,
        tty=False,
    ).decode("utf-8")
    fn = f"{os.path.splitext(source.name)[0]}.pdf"
    if debug:
        print(f'Built PDF of "{fn}"')
    return fn


@click.command(context_settings=CONTEXT_SETTINGS)
@click.argument(
    "source",
)
@click.argument(
    "image",
)
@click.option("--pull", is_flag=True, help="Whether to also pull a fresh image")
@click.option("--debug/--no-debug", default=True, help="Whether to output debug")
def main(source, image, pull, debug):
    build_pdf(Path(source), image, pull, debug)


if __name__ == "__main__":
    main()
