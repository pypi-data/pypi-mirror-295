from iccore.project import Milestone
from icplot.geometry import Scene, Rectangle

from .gantt import GanttChart


class GanttRenderer:

    def _add_milestone(
        self, gantt: GanttChart, scene: Scene, milestone: Milestone, chart_range, yloc
    ):
        # chart_delta = chart_range[1] - chart_range[0]
        chart_delta = 0
        start_delta = milestone.start_date - chart_range[0]
        # milestone_delta = milestone.due_date - milestone.start_date
        milestone_delta = 0

        start_frac = float(start_delta / chart_delta)
        milestone_frac = float(milestone_delta / chart_delta)

        w = milestone_frac * gantt.width
        h = gantt.bar_max_height * gantt.height
        x = start_frac * gantt.width
        y = yloc

        rect = Rectangle(w, h)
        rect.location = (x, y)
        rect.fill = gantt.bar_color
        scene.items.append(rect)

    def _add_milestones(self, gantt: GanttChart, scene: Scene):

        if not gantt.milestones:
            return

        milestones = gantt.milestones
        # milestones.sort(key=lambda x: x.start_date, reverse=True)

        start_date = gantt.start_date
        end_date = gantt.end_date
        if not start_date:
            start_date = milestones[0].start_date

        # if not end_date:
        #    end_date = max(m.due_date for m in milestones)

        chart_range = (start_date, end_date)
        yloc = 0.0
        bar_height = gantt.bar_max_height * gantt.height
        for milestone in milestones:
            self._add_milestone(gantt, scene, milestone, chart_range, yloc)
            yloc += bar_height

    def render(self, gantt: GanttChart) -> Scene:
        scene = Scene()

        self._add_milestones(gantt, scene)

        return scene
