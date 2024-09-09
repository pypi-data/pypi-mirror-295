#!/usr/bin/env python

import argparse
import json
import shutil
import click
import livereload
import logging
import tempfile

from importlib import metadata
from pathlib import Path
from rich.logging import RichHandler
from urllib.parse import urlparse

from .config import Config
from .constants import (
    EXPECTED_CONFIG_LOCATION,
    DEFAULT_OUTPUT_DIR,
    REVEALJS_RESOURCE,
    HIGHLIGHTJS_RESOURCE,
    VERSION,
    REVEALJS_VERSION,
    HIGHLIGHTJS_THEMES_VERSION,
)
from .markupgenerator import MarkupGenerator


logger = logging.getLogger()
logger.setLevel("DEBUG")
logger.addHandler(RichHandler(show_path=False))


################################################################################

context_settings = {"help_option_names": ["-h", "--help"], "max_content_width": 120}

files_argument_data = {
    "metavar": "FILENAME|PATH",
    # "help": "Path to the Markdown file, or the directory containing Markdown files.",
}

config_file_argument_data = {
    "metavar": "FILENAME",
    "default": EXPECTED_CONFIG_LOCATION,
    "help": "Provide a specific MkSlides-Reveal config file.",
}


@click.group(context_settings=context_settings)
@click.version_option(
    VERSION,
    "-V",
    "--version",
    message=f"mkslides-reveal, version {VERSION}\nreveal.js, version {REVEALJS_VERSION}\nhighlight.js themes, version {HIGHLIGHTJS_THEMES_VERSION}"
    "",
)
def cli():
    "MkSlides-Reveal - Slides with Markdown using the power of Reveal.js."
    pass


def read_config(config_location: str) -> Config:
    config_path = Path(config_location).resolve()
    config = Config()

    if config_path.exists():
        logger.info(f'Config file found at "{config_path.absolute()}"')
        config.merge_config_from_file(config_path)

    return config


def parse_ip_port(
    ip_port_str: str,
) -> tuple[str, int]:
    urlparse_result = urlparse(f"//{ip_port_str}")
    ip = urlparse_result.hostname
    port = urlparse_result.port

    return ip, port


@cli.command()
@click.argument("files", **files_argument_data)
@click.option("-f", "--config-file", **config_file_argument_data)
@click.option(
    "-d",
    "--site-dir",
    help="The directory to output the result of the slides build.",
    metavar="PATH",
    default=DEFAULT_OUTPUT_DIR,
)
def build(files, config_file, site_dir):
    """
    Build the MkDocs documentation.

    FILENAME|PATH is the path to the Markdown file, or the directory containing Markdown files.
    """

    logger.info("Command: build")

    # Reading configuration

    config = read_config(config_file)

    # Configuring paths

    input_path = Path(files).resolve(strict=True)
    md_root_path = input_path if input_path.is_dir() else input_path.parent
    output_directory = Path(site_dir).resolve(strict=False)
    markup_generator = MarkupGenerator(config, output_directory)

    # Process markdown files

    markup_generator.create_output_directory()
    markup_generator.process_markdown(input_path)


@cli.command()
@click.argument("files", **files_argument_data)
@click.option(
    "-a",
    "--dev-addr",
    help="IP address and port to serve slides locally.",
    metavar="<IP:PORT>",
)
@click.option(
    "-o",
    "--open",
    "open_in_browser",
    help="Open the website in a Web browser after the initial build finishes.",
    is_flag=True,
)
@click.option(
    "--watch-index-theme",
    help="Include the index theme in list of files to watch for live reloading.",
    is_flag=True,
)
@click.option(
    "--watch-index-template",
    help="Include the index template in list of files to watch for live reloading.",
    is_flag=True,
)
@click.option(
    "--watch-slides-theme",
    help="Include the slides theme in list of files to watch for live reloading.",
    is_flag=True,
)
@click.option(
    "--watch-slides-template",
    help="Include the slides template in list of files to watch for live reloading.",
    is_flag=True,
)
@click.option("-f", "--config-file", **config_file_argument_data)
def serve(
    files,
    dev_addr,
    open_in_browser,
    watch_index_theme,
    watch_index_template,
    watch_slides_theme,
    watch_slides_template,
    config_file,
):
    """
    Run the builtin development server.

    FILENAME|PATH is the path to the Markdown file, or the directory containing Markdown files.
    """

    logger.info("Command: serve")

    # Reading configuration

    config = read_config(config_file)

    # Configuring paths

    input_path = Path(files).resolve(strict=True)
    md_root_path = input_path if input_path.is_dir() else input_path.parent
    site_dir = tempfile.mkdtemp(prefix="mkslides_")
    output_directory = Path(site_dir).resolve(strict=False)
    markup_generator = MarkupGenerator(config, output_directory)

    # Process markdown files

    markup_generator.create_output_directory()
    markup_generator.process_markdown(input_path)

    # Livereload

    def reload():
        logger.info("Reloading ...")
        markup_generator.create_output_directory()
        markup_generator.process_markdown(input_path)

    try:
        server = livereload.Server()
        server._setup_logging = (
            lambda: None
        )  # https://github.com/lepture/python-livereload/issues/232

        watched_paths = [
            files,
            config_file,  # TODO reload config
        ]

        if watch_index_theme:
            watched_paths.append(config.get("index", "theme"))
        if watch_index_template:
            watched_paths.append(config.get("index", "template"))
        if watch_slides_theme:
            watched_paths.append(config.get("slides", "theme"))
        if watch_slides_template:
            watched_paths.append(config.get("slides", "template"))

        for path in watched_paths:
            if path:
                path = Path(path).resolve(strict=True)
                logger.info(f'Watching: "{path.absolute()}"')
                server.watch(filepath=path.absolute().as_posix(), func=reload, delay=1)

        ip, port = parse_ip_port(dev_addr)

        server.serve(
            host=ip,
            port=port,
            root=output_directory,
            open_url_delay=0 if open else None,
        )

    finally:
        if output_directory.exists():
            shutil.rmtree(output_directory)
            logger.info(f'Removed "{output_directory}"')


if __name__ == "__main__":
    cli()
