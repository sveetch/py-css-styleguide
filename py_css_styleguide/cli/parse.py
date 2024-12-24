import logging
from pathlib import Path

import click

from ..model import Manifest
from ..exceptions import ParserErrors, SerializerError


@click.command()
@click.argument(
    "source",
    nargs=1,
    type=click.Path(exists=True, path_type=Path),
)
@click.option(
    "--destination",
    type=click.Path(
        file_okay=True, dir_okay=False, resolve_path=False, path_type=Path,
    ),
    help=(
        "File path destination where to write serialized JSON manifest. If not given"
        "serialized JSON will be outputed to standard output."
    ),
)
@click.pass_context
def parse_command(context, source, destination):
    """
    Parse a CSS manifest to validate it and possibly dump it to JSON.

    'SOURCE' argument have to be an existing filepath to a CSS manifest.

    \f

    **Usage** ::

        styleguide parse SOURCE --destination DESTINATION

    Optional ``--destination`` is a file path destination where to write serialized
    JSON manifest. If not given serialized JSON will be outputed to standard output.
    """
    logger = logging.getLogger("py-css-styleguide")

    logger.debug("Parsing: {}".format(source.resolve()))

    manifest = Manifest()

    try:
        manifest.load(source.read_text())
    except ParserErrors as e:
        logger.critical(e)
        for line in e.error_payload:
            logger.error(line)

        raise click.Abort()
    except SerializerError as e:
        logger.critical(e)

        raise click.Abort()

    if destination:
        destination.write_text(manifest.to_json())
    else:
        click.echo(manifest.to_json())
