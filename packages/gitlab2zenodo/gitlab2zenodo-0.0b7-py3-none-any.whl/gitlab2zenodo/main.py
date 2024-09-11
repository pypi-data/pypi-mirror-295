#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse
import json
import logging
import sys
from pathlib import Path

from gitlab2zenodo.deposit import get_metadata, send
from gitlab2zenodo.settings import Settings


def g2z_meta_command():
    usage = """Gitlab2Zenodo: get zenodo metadata."""
    parser = argparse.ArgumentParser(description=usage,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("-t", "--token",
                        dest="zenodo_token",
                        help="The zenodo access token",
                        type=str)
    parser.add_argument("-i", "--id",
                        dest="zenodo_record",
                        help="The zenodo record ID to get the metadata for",
                        type=str)
    parser.add_argument("-s", "--sandbox",
                        help="send to sandbox zenodo (for development)",
                        action="store_true")
    parser.add_argument("-o", "--out",
                        dest="out_file",
                        default="stdout",
                        help="file to save the metadata to. Defaults to : 'stdout",
                        type=str)
    parser.add_argument("zenodo_record_pos",
                        help="DEPRECATED: zenodo identifier. Use --id instead",
                        type=str,
                        nargs="*")
    args = parser.parse_args()

    # Print help if ID is not given as named or positional argument
    if not args.zenodo_record_pos and not args.zenodo_record:
        parser.print_help(sys.stderr)
        sys.exit(1)

    # Handle zenodo ID given as argument or positional
    if args.zenodo_record_pos and not args.zenodo_record:
        args.zenodo_record = args.zenodo_record_pos[0]
    # Remove the positional record ID
    del args.zenodo_record_pos

    logging.basicConfig(level=logging.INFO)
    settings=Settings(args)

    deposit = get_metadata(settings=settings)
    out_str = json.dumps(deposit["metadata"], indent=4)
    if args.out_file == "stdout":
        print(out_str, file=sys.stdout)
    else:
        with open(args.out_file, "w", encoding="utf-8") as f:
            f.write(out_str)



def g2z_command():
    usage = """Gitlab2Zenodo: upload a gitlab archive to zenodo."""
    parser = argparse.ArgumentParser(description=usage,
                                     formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("archive", help="archive to upload", type=Path)
    parser.add_argument("-t", "--token",
                        dest="zenodo_token",
                        help="The zenodo access token.",
                        type=str)
    parser.add_argument("-i", "--id",
                        dest="zenodo_record",
                        help="The zenodo record ID to upload the archive to.",
                        type=str)
    parser.add_argument("-v", "--version",
                        dest="version",
                        help=(
                            "The new version of the zenodo record. "
                            "If not given here, it is extracted from the "
                            "environment variable `CI_COMMIT_TAG` "
                            "- if present"),
                        type=str)
    parser.add_argument("-s", "--sandbox",
                        help="send to sandbox zenodo (for development)",
                        action="store_true")
    parser.add_argument("-p", "--publish",
                        help="publish on zenodo (be careful, this can not be undone)",
                        action="store_true")
    parser.add_argument("-m", "--metadata", help="path to metadata file",
                        default=".zenodo.json", type=Path)
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO)

    send(settings=Settings(args))
