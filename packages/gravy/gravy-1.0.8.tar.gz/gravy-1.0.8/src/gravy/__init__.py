import typing as _typing

import click as _click
import getoptify as _getoptify

__all__ = ["calculate", "main", "score"]

_VALUES = {
    "A": 1.8,
    "C": 2.5,
    "D": -3.5,
    "E": -3.5,
    "F": 2.8,
    "G": -0.4,
    "H": -3.2,
    "I": 4.5,
    "K": -3.9,
    "L": 3.8,
    "M": 1.9,
    "N": -3.5,
    "P": -1.6,
    "Q": -3.5,
    "R": -4.5,
    "S": -0.8,
    "T": -0.7,
    "V": 4.2,
    "W": -0.9,
    "X": None,
    "Y": -1.3,
    "-": None,
}


def score(seq: _typing.Iterable):
    """Calculate the GRAVY score."""
    answers = [_VALUES[str(k)] for k in seq]
    answers = [v for v in answers if v is not None]
    if len(answers):
        return sum(answers) / len(answers)
    else:
        return float("nan")


calculate = score  # for legacy


@_getoptify.command(
    shortopts="hV",
    longopts=["help", "version", "format="],
    allow_argv=True,
    gnu=True,
)
@_click.command(add_help_option=False)
@_click.option(
    "--format", "f", help="format of the output", default=".5f", show_default=True
)
@_click.help_option("-h", "--help")
@_click.version_option(None, "-V", "--version")
@_click.argument("seq")
def main(seq, f):
    """calculate the GRAVY score of seq"""
    ans = score(seq)
    out = format(ans, f)
    _click.echo(out)


if __name__ == "__main__":
    main()
