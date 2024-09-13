from pathlib import Path
import os
import shutil

from icplot.cairo_interface import CairoInterface
from icplot.geometry import Scene, Rectangle, TextPath
from icplot.color import Color


def test_cairo_interface():

    cairo_interface = CairoInterface()
    scene = Scene()

    rect = Rectangle(20, 20)
    rect.location = (10, 10)
    rect.fill = Color.from_rgba(0.5, 0.5, 1, 0.5)
    rect.stroke = Color.from_rgba(0.5, 0.0, 0.0, 0.5)
    scene.items.append(rect)

    text = TextPath("Hello World")
    text.location = (5, 5)
    scene.items.append(text)

    output_dir = Path(os.getcwd()) / "test_cairo_interface"
    os.makedirs(output_dir, exist_ok=True)
    cairo_interface.draw_svg(scene, output_dir / "output.svg")
    shutil.rmtree(output_dir)
    
