import os as _os

import click as _click
import getoptify as _getoptify

_CONTEXT_SETTINGS = dict(help_option_names=["-h", "--help"])


def file_list(*paths):
    return list(file_generator(*paths))


def file_generator(*paths):
    for raw_path in paths:
        path = raw_path
        path = _os.path.expanduser(path)
        path = _os.path.expandvars(path)
        if _os.path.isfile(path):
            yield path
            continue
        for root, dnames, fnames in _os.walk(path):
            for fname in fnames:
                file = _os.path.join(root, fname)
                yield file


@_getoptify.command(shortopts="hV")
@_click.command(context_settings=_CONTEXT_SETTINGS)
@_click.version_option(None, "-V", "--version")
@_click.argument("path", nargs=-1)
def main(path):
    """List files under given paths."""
    for f in file_list(*path):
        _click.echo(f)


if __name__ == "__main__":
    main()
