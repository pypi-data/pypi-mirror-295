from pathlib import Path

from .gantt import GanttChart


class PgfGanttRenderer:

    def __init__(self):
        self.template: str = ""

    def _load_template(self):
        if self.template:
            return

        with open(Path(__file__).parent / "pgfgantt.tex", "r", encoding="utf-8") as f:
            self.template = f.read()

    def render(self, gantt: GanttChart) -> str:

        output = self.template

        if gantt.title:
            title_str = f"\\title{{{gantt.title}}}"
            output.replace("%%TITLE%%", title_str)

        return output
