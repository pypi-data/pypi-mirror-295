#!/usr/bin/env python3
import argparse
import logging
from pathlib import Path

from iccore import logging_utils
from iccore import runtime

from icplot.image_utils import pdf_to_png, svg_to_png, svg_to_pdf

logger = logging.getLogger(__name__)


def launch_common(args):
    runtime.ctx.set_is_dry_run(args.dry_run)
    logging_utils.setup_default_logger()


def convert(args):
    launch_common(args)

    logger.info("Attempting coversion between %s %s", args.source, args.target)

    if args.target:
        target = Path(args.target).resolve()
    else:
        target = None

    if args.source.suffix == ".pdf":
        pdf_to_png(args.source.resolve(), target)
    elif args.source.suffix == ".svg":
        if target:
            if target.suffix == ".png":
                svg_to_png(args.source.resolve(), target)
            elif target.suffix == ".pdf":
                svg_to_pdf(args.source.resolve(), target)
        else:
            svg_to_png(args.source)
    logger.info("Finished conversion")


def main_cli():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry_run",
        type=int,
        default=0,
        help="Dry run script - 0 can modify, 1 can read, 2 no modify - no read",
    )
    subparsers = parser.add_subparsers(required=True)

    convert_parser = subparsers.add_parser("convert")
    convert_parser.add_argument(
        "--source",
        type=Path,
        help="Path to file to be converted from",
    )
    convert_parser.add_argument(
        "--target",
        type=str,
        default="",
        help="Path to file to be converted to",
    )
    convert_parser.set_defaults(func=convert)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main_cli()
