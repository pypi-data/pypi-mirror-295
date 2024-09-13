from pathlib import Path

from iccore.serialization import read_json
from icplot.graph import LinePlotSeries
from icplot.graph.matplotlib import MatplotlibPlotter
from ictasks.tasks import TaskCollection


class PlotGenerator:
    def __init__(
        self,
        tasks: TaskCollection,
        plots: dict,
        colormap: dict,
        series_label: str,
        x_axis: str,
        result_filename: str,
        result_dir: Path,
    ):
        self.tasks = tasks
        self.results: list[dict] = []
        self.plotter = MatplotlibPlotter()
        self.plots = plots
        self.colormap = colormap
        self.series_label = series_label
        self.x_axis = x_axis
        self.result_filename = result_filename
        self.result_dir = result_dir

    def plot_result(self, result, plot_key, series_val):
        xval = int(result[self.x_axis])
        if plot_key == "runtime":
            start_time = result["start_time"]
            end_time = result["end_time"]
            series_val.add_entry(xval, end_time - start_time)

    def plot_label(self, label: str):
        if label in self.colormap:
            color = self.colormap[label]
        else:
            color = None

        series = {}
        for plot_key in self.plots.keys():
            series[plot_key] = LinePlotSeries(label=label, color=color)

        for result in self.results:
            if result["state"] == "finished":
                if result["circuit_label"] == label:
                    for plot_key, series_val in series.items():
                        self.plot_result(result, plot_key, series_val)

        for key, value in series.items():
            value.sort()
            self.plots[key].add_series(value)

    def make_plots(self):

        self.tasks.load_from_job_dir()
        for task in self.tasks:
            task_dir = task.get_task_dir()
            self.results.append(read_json(task_dir / self.result_filename))

        labels = set()
        for result in self.results:
            labels.add(result[self.series_label])

        for label in labels:
            self.plot_label(label)

        for key, plot in self.plots.items():
            self.plotter.plot(plot, self.result_dir / f"{key}.svg")
