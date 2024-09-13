from pathlib import Path

from icplot.graph import Plot, LinePlotSeries
from icplot.graph.matplotlib import MatplotlibPlotter


def test_line_plot():

    plot = Plot(
        title="test",
        x_label="test_x",
        y_label="test_y",
        legend_label="test_legend"
    )

    data = [([0, 5, 10], [1, 2, 3]), ([0, 5, 10], [3, 6, 9]), ([0, 5, 10], [4, 8, 12])]

    for idx, [x, y] in enumerate(data):
        plot.add_series(LinePlotSeries(x, y, label=f"Series {idx}"))

    plot.set_x_ticks(0, 10, 5)

    output_path = Path() / "output.svg"

    plotter = MatplotlibPlotter()
    plotter.plot(plot, output_path)

    assert output_path.exists()
    output_path.unlink()
