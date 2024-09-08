"""Console script for rstms_nbctl."""

import json
import sys
from pathlib import Path

import click
import click.core

from .exception_handler import ExceptionHandler
from .netboot import Netboot
from .shell import _shell_completion
from .version import __timestamp__, __version__

header = f"{__name__.split('.')[0]} v{__version__} {__timestamp__}"


def _ehandler(ctx, option, debug):
    ctx.obj = dict(ehandler=ExceptionHandler(debug))
    ctx.obj["debug"] = debug


@click.group("nbctl", context_settings={"auto_envvar_prefix": "NBCTL"})
@click.version_option(message=header)
@click.option("-d", "--debug", is_eager=True, is_flag=True, callback=_ehandler, help="debug mode")
@click.option(
    "--shell-completion",
    is_flag=False,
    flag_value="[auto]",
    callback=_shell_completion,
    help="configure shell completion",
)
@click.option("-u", "--url", default="https://netboot.rstms.net/api", envvar="NBCTL_URL")
@click.option("-C", "--ca", default="/etc/ssl/keymaster.pem", envvar="NBCTL_CA")
@click.option("-c", "--cert", default="/etc/ssl/netboot.pem", envvar="NBCTL_CERT")
@click.option("-k", "--key", default="/etc/ssl/netboot.key", envvar="NBCTL_KEY")
@click.pass_context
def cli(ctx, debug, shell_completion, url, ca, cert, key):
    """netboot configuration utility"""
    ctx.obj = Netboot(url, ca, cert, key)


@cli.command()
@click.argument("mac")
@click.argument("os")
@click.argument("response-file", type=click.Path(dir_okay=False, readable=True, path_type=Path))
@click.argument("package-file", required=False, type=click.Path(dir_okay=False, readable=True, path_type=Path))
@click.pass_obj
def add(ctx, mac, os, response_file, package_file):
    """add host config"""
    result = ctx.add(mac, os, response_file, package_file)
    click.echo(json.dumps(result, indent=2))


@cli.command()
@click.argument("package-file", type=click.Path(dir_okay=False, readable=True, path_type=Path))
@click.pass_obj
def upload(ctx, package_file):
    """upload package tarball"""
    result = ctx.upload_package(package_file)
    click.echo(json.dumps(result, indent=2))


@cli.command
@click.pass_obj
def ls(ctx):
    """list configs"""
    result = ctx.ls()
    click.echo(json.dumps(result, indent=2))


@cli.command
@click.argument("mac")
@click.pass_obj
def rm(ctx, mac):
    """delete host config"""
    if mac == "all":
        result = ctx.delete_all()
    else:
        result = ctx.delete(mac)
    click.echo(json.dumps(result, indent=2))


if __name__ == "__main__":
    sys.exit(cli())
