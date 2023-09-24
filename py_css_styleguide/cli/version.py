import click

from py_css_styleguide import __version__


@click.command()
@click.pass_context
def version_command(context):
    """
    Show version and exit.

    \f

    **Usage** ::

        styleguide version
    """
    click.echo("py-css-styleguide version {}".format(__version__))
