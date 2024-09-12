import click as _click
import getoptify as _getoptify


def seqpad(seq):
    while len(seq) % 3 != 0:
        seq += "N"
    return seq


@_getoptify.command(
    shortopts="hV",
    longopts=["help", "version"],
    allow_argv=True,
    gnu=True,
)
@_click.command(add_help_option=False)
@_click.help_option("-h", "--help")
@_click.version_option(None, "-V", "--version")
@_click.argument("seq", required=False)
def main(seq):
    """pad seq to a length that is a multiple of three"""
    if seq is not None:
        _click.echo(seqpad(seq))


if __name__ == "__main__":
    main()
