import argparse
import subprocess
import shutil
import os
from pathlib import Path
import logging

from .image_utils import pdf_to_png

logger = logging.getLogger(__name__)


class TexInterface:
    def __init__(self, build_dir: Path | None, output_dir: Path | None):

        if build_dir:
            self.build_dir: Path = build_dir.resolve()
        else:
            self.build_dir = Path()
        if not output_dir:
            self.output_dir: Path = self.build_dir
        else:
            self.output_dir = output_dir.resolve()
        self.build_engine = "pdflatex"

    def build_pdf(self, source_path: Path, build_dir: Path):
        cmd = f"{self.build_engine} {source_path}"
        subprocess.run(cmd, shell=True, check=True, cwd=build_dir)

    def build_single(self, source_path: Path):
        logging.info("Building source: %s", source_path)

        # Make a working dir
        work_dir = self.build_dir / source_path.stem
        os.makedirs(work_dir, exist_ok=True)

        tex_path = work_dir / source_path.name
        shutil.copy(source_path, tex_path)

        self.build_pdf(tex_path, work_dir)

        pdf_path = tex_path.parent / f"{tex_path.stem}.pdf"
        pdf_to_png(pdf_path)

        # If output dir is different to build dir copy final content there
        if self.output_dir != self.build_dir:
            png_path = pdf_path.parent / f"{tex_path.stem}.png"
            shutil.copy(pdf_path, self.output_dir)
            shutil.copy(png_path, self.output_dir)

    def build(self, search_path: Path):

        if not search_path.is_absolute():
            search_path = Path(os.getcwd()) / search_path

        os.makedirs(self.output_dir, exist_ok=True)

        if search_path.is_dir():
            for tex_file in search_path.glob("*.tex"):
                self.build_single(tex_file)
        else:
            self.build_single(search_path)

        logger.info("Finished building sources")


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        help="Path to the tikz source",
    )
    parser.add_argument(
        "--build_dir",
        type=Path,
        default=Path(os.getcwd()) / "_build/tikz",
        help="Path for build output",
    )
    parser.add_argument(
        "--output_dir",
        type=Path,
        default="",
        help="Optional dir to collect build output",
    )

    logging.basicConfig(encoding="utf-8", level=logging.INFO)
    args = parser.parse_args()

    tex = TexInterface(args.build_dir, args.output_dir)
    tex.build(args.source)
