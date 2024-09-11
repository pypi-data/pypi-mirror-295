#!/usr/bin/env python3

"""
This is the main entrypoint for the iccore utility
"""

import argparse
import logging
import json
import os
from pathlib import Path

from iccore.network import HttpClient
from iccore import logging_utils
from iccore import runtime
from iccore.serialization import write_json
from iccore.version_control import GitlabClient, GitlabToken, GitlabInstance

logger = logging.getLogger(__name__)


def launch_common(args):
    runtime.ctx.set_is_dry_run(args.dry_run)
    logging_utils.setup_default_logger()


def get_milestones(args):
    launch_common(args)

    logger.info("Fetching milestones for %s %s", args.resource_type, args.resource_id)

    token = GitlabToken(args.token, args.token_type)
    instance = GitlabInstance(args.url)
    gitlab = GitlabClient(instance, token)

    milestones = gitlab.get_milestones(args.resource_id, args.resource_type)
    output = [m.serialize() for m in milestones]
    output_json = json.dumps(output, indent=4)

    if args.output:
        write_json(output_json, args.output)
    else:
        print(output_json)

    logger.info("Finished fetching milestones")


def get_latest_release(args):
    launch_common(args)

    logger.info("Getting latest release for project %s", args.project_id)
    token = GitlabToken(args.token, args.token_type)
    instance = GitlabInstance(args.url)
    gitlab = GitlabClient(instance, token)

    version = gitlab.get_latest_release(
        args.project_id, args.asset_name, args.download_dir
    )
    if version:
        print(version)

    logger.info("Finished getting latest release")


def download(args):

    launch_common(args)
    logger.info("Attempting to download from %s", args.url)

    headers = {args.token_header: args.token}

    http_client = HttpClient()
    http_client.download_file(args.url, args.download_dir, headers)


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry_run",
        type=int,
        default=0,
        help="Dry run script - 0 can modify, 1 can read, 2 no modify - no read",
    )
    subparsers = parser.add_subparsers(required=True)

    gitlab_parser = subparsers.add_parser("gitlab")
    gitlab_parser.add_argument(
        "--token",
        type=str,
        default="",
        help="Access token for the Gitlab resource - if required",
    )
    gitlab_parser.add_argument(
        "--token_type",
        type=str,
        help="Type of token - corresponding to the header key in http requests",
        default="PRIVATE-TOKEN",
    )
    gitlab_parser.add_argument(
        "--url",
        type=str,
        help="URL for the Gitlab repo instance",
        default="https://git.ichec.ie",
    )

    gitlab_subparsers = gitlab_parser.add_subparsers(required=True)

    milestones_subparser = gitlab_subparsers.add_parser("milestone")
    milestones_subparser.add_argument(
        "resource_id", type=int, help="Id of the group or project being queried"
    )
    milestones_subparser.add_argument(
        "--resource_type",
        type=str,
        default="project",
        help="Whether to query 'project' or 'group' milestones",
    )
    milestones_subparser.add_argument(
        "--output",
        type=str,
        default="",
        help="Path to output, if not given the output is dumped to terminal",
    )
    milestones_subparser.set_defaults(func=get_milestones)

    latest_release_parser = gitlab_subparsers.add_parser("latest_release")
    latest_release_parser.add_argument(
        "project_id", type=int, help="Id of the project being queried"
    )
    latest_release_parser.add_argument(
        "--asset_name", type=str, help="Name of a release asset to download", default=""
    )
    latest_release_parser.add_argument(
        "--download_dir",
        type=Path,
        help="Directory to download release assets to",
        default=Path(os.getcwd()),
    )
    latest_release_parser.set_defaults(func=get_latest_release)

    download_parser = gitlab_subparsers.add_parser("download")
    download_parser.add_argument("url", type=str, help="Url to download")
    download_parser.add_argument(
        "--token", type=str, help="Optional auth token", default=""
    )
    download_parser.add_argument(
        "--token_header", type=str, help="Optional auth token header key", default=""
    )
    download_parser.add_argument(
        "--download_dir",
        type=Path,
        help="Directory to download to",
        default=Path(os.getcwd()),
    )
    download_parser.set_defaults(func=download)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main_cli()
