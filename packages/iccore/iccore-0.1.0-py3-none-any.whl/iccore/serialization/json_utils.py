from pathlib import Path
import logging

import json

from iccore.runtime import ctx

logger = logging.getLogger(__name__)


def read_json(path: Path):

    if not ctx.can_read():
        ctx.add_cmd(f"read_json {path}")
        return {}

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def write_json(payload: dict, path: Path, indent: int = 4):

    if not ctx.can_modify():
        ctx.add_cmd(f"write_json {path}")
        return

    with open(path, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=indent)
