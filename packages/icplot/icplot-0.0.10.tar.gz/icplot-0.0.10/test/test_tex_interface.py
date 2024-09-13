import os
import shutil
from pathlib import Path
from icplot.tex_interface import TexInterface


def test_tex_interface():

    build_dir = Path(os.getcwd()) / "tmp_build"
    tex = TexInterface(build_dir, build_dir)

    data_dir = Path(__file__).parent / "data"
    tex_file = data_dir / "test.tex"

    tex = TexInterface(build_dir, build_dir)
    tex.build(tex_file)

    shutil.rmtree(build_dir)
