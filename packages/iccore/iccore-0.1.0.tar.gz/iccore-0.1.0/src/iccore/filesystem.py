"""
This module has wrappers over Python built-ins for filsystem operations
"""

import shutil
from pathlib import Path

from .runtime import ctx


def copy(src: Path, dst: Path) -> None:
    """
    Copy the file or directory from `src` to `dst`
    :param src: The location to copy from
    :param dst: The location to copy to
    """

    if ctx.can_modify():
        shutil.copy(src, dst)
    else:
        ctx.add_cmd(f"copy {src} {dst}")


def make_archive(archive_name: Path, fmt: str, src: Path) -> None:
    """
    Create an archive with name `archive_name` and chosen format, e.g. zip
    from the content in `src`
    :param archive_name: The path to the created archive
    :param fmt: The desired archive format, e.g. zip
    :param src: The src of the content to be archived
    """

    if ctx.can_modify():
        shutil.make_archive(str(archive_name), fmt, src)
    else:
        ctx.add_cmd(f"make_archive {archive_name} {fmt} {src}")


def unpack_archive(src: Path, dst: Path) -> None:
    """
    Extract the archive at `src` to `dst`
    """

    if ctx.can_modify():
        shutil.unpack_archive(src, dst)
    else:
        ctx.add_cmd(f"unpack_archive {src} {dst}")
