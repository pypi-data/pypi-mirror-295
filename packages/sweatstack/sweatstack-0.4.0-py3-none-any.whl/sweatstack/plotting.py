from typing import List, Tuple

import plotly.graph_objects as go
from plotly.subplots import make_subplots


METRIC_LABELS = {
    "power": "power [Watt]",
    "heart_rate": "heart rate [bpm]",
    "speed": "speed [m/s]",
    "cadence": "cadence [/min])",
    "distance": "distance [m]",
}


METRIC_COLORS = {
    "power": "blue",
    "heart_rate": "red",
    "speed": "green",
    "cadence": "orange",
}


plotting_backend = "plotly"


class PlottingMixin:
    def _get_plotting_backend(self):
        global plotting_backend
        match plotting_backend:
            case "plotly":
                return PlotlyPlottingBackend()
            case _:
                raise ValueError(f"Unsupported plotting backend: {plotting_backend}")

    def plot_activity_data(self, activity_id, metrics=None, subplots=True):
        plotting_backend = self._get_plotting_backend()

        activity_data = self.get_activity_data(activity_id)

        return plotting_backend.plot_activity_data(activity_data, metrics, subplots)

    def plot_latest_activity_data(self, metrics=None, subplots=True):
        latest_activity = self.get_latest_activity()
        return self.plot_activity_data(latest_activity.id, metrics, subplots)
    
    def plot_scatter(self, x, y, x_label=None, y_label=None):
        plotting_backend = self._get_plotting_backend()
        return plotting_backend.plot_scatter(
            x=x,
            y=y,
            x_label=x_label,
            y_label=y_label
        )

class BasePlottingBackend:
    def plot_activity_data(self, data, metrics=None, subplots=True):
        raise NotImplementedError("Subclass must implement abstract method")

    def plot_scatter(self, x, y, x_label=None, y_label=None):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def preprocess_metrics(self, metrics: List[str], columns: List[str]) -> List[Tuple[str, str, str]]:
        """
        Preprocess the given metrics.

        Args:
            metrics (List[str]): A list of metric names.

        Returns:
            List[Tuple[str, str, str]]: An ordered list of tuples, each containing
            a metric name, its corresponding label, and its color.
        """

        if not metrics:
            metrics = [col for col in columns if col not in ["sport", "sub_sport", "lap", "lap_trigger", "duration"]]
        elif missing_metrics := set(metrics) - set(columns):
            raise ValueError(f"The following metrics are not present in the data: {', '.join(missing_metrics)}")

        priority_metrics = ["power", "heart_rate", "speed", "cadence"]
        existing_priority_metrics = [metric for metric in priority_metrics if metric in metrics]
        remaining_metrics = sorted(col for col in metrics if col not in existing_priority_metrics)

        sorted_metrics = existing_priority_metrics + remaining_metrics

        return [(metric, METRIC_LABELS.get(metric, metric), METRIC_COLORS.get(metric, None)) for metric in sorted_metrics]


class PlotlyPlottingBackend(BasePlottingBackend):
    def plot_activity_data(self, data, metrics=None, subplots=True):
        metrics = self.preprocess_metrics(metrics, data.columns)
        if subplots:
            fig = make_subplots(
                rows=len(metrics),
                cols=1,
                shared_xaxes=True,
                vertical_spacing=0.02
            )

            for i, (metric, label, color) in enumerate(metrics, 1):
                params = {}
                if color:
                    params["line"] = dict(color=color)
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=data[metric],
                        name=metric,
                        **params,
                    ),
                    row=i,
                    col=1,
                )
            
                fig.update_layout(
                    height=600,
                    yaxis_title=metrics[0][1],
                    hovermode="x unified",
                    spikedistance=-1,
                    hoverdistance=-1,
                )
                fig.update_yaxes(
                    title_text=label,
                    row=i,
                    col=1,
                )

        else:
            fig = go.Figure()
            for i, (metric, label, color) in enumerate(metrics):
                params = {}
                if color:
                    params["line"] = dict(color=color)
                fig.add_trace(
                    go.Scatter(
                        x=data.index,
                        y=data[metric],
                        name=metric,
                        yaxis=f"y{i+1}",
                        **params,
                    )
                )
                if i > 0:
                    fig.update_layout({
                        f'yaxis{i+1}': {'overlaying': 'y', 'side': 'right', 'title': label, "position": 1 - (i * 0.07), "color": color}
                    
                    })
                else:
                    fig.update_layout({
                        "yaxis1": {"color": color}
                    })

            
            fig.update_layout(
                height=600,
                yaxis_title=metrics[0][1],
                xaxis=dict(domain=[0, 1 - (len(metrics) - 1) * 0.07]),
                hovermode="x unified",
                spikedistance=-1,
                hoverdistance=-1,
            )
        
        return fig

    def plot_scatter(self, x, y, x_label=None, y_label=None):
        fig = go.Figure(
            data=go.Scatter(x=x, y=y, mode='markers'),
            layout=go.Layout(
                xaxis_title=x_label if x_label is not None else x.name,
                yaxis_title=y_label if y_label is not None else y.name,
                width=800,
                height=800
            )
        )
        
        fig.show()