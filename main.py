# standard library
import base64
import json

# other libraries - see 3rd party licenses
from bokeh.events import LegendItemClick
from bokeh.io import curdoc
from bokeh.layouts import layout, row
from bokeh.models import ColumnDataSource, HoverTool, Legend, Spacer
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models.ranges import DataRange1d
from bokeh.models.widgets.buttons import Toggle
from bokeh.models.widgets.inputs import FileInput
from bokeh.models.widgets.sliders import DateRangeSlider
from bokeh.palettes import Muted8
from bokeh.plotting import figure

from data_preparation import data_preparation

# local helpers
from quantity import QuantityLabels


def update_line_visibility_legend_click(legend_item_click):
    """
    Callback for legend clicks - update line visibility
    """
    if not line_toggle.active:
        return

    for idx, item in enumerate(legend_labels):
        if item[0] == legend_item_click.item.label.value:
            lines[idx].visible = not lines[idx].visible


def toggle_line_visibility(attr, new, old):
    """
    Callback for global line visibility toggle
    """
    _, _, _ = attr, new, old
    for idx, line in enumerate(lines):
        line.visible = old if scatters[idx].visible else False


def date_range_input_handler(attr, new, old):
    """
    Callback for global date range update (stable over visibility changes)
    """
    _, _ = attr, old
    fig_timeseries.x_range = DataRange1d(start=new[0], end=new[1])


def create_scatter_all_quantities(dates, values):
    for idx, (quan, color) in enumerate(zip(values, Muted8)):
        source = ColumnDataSource(data=dict(dates=dates, quan=quan))
        scatter = fig_timeseries.scatter(
            x="dates", y="quan", source=source, color=color, marker="hex", size=6
        )
        line = fig_timeseries.line(x="dates", y="quan", source=source, color=color)
        scatter.visible = True if idx == 0 else False

        scatters.append(scatter)
        lines.append(line)
        line.visible = False
        legend_labels.append((QuantityLabels.val[idx], [scatter]))

    # on hover: show date
    fig_timeseries.add_tools(
        HoverTool(
            tooltips=[("Date", "$x{%F}")],
            formatters={"$x": "datetime"},
        )
    )

    fig_timeseries.toolbar.autohide = True

    # style title
    fig_timeseries.title = "All Tracked Quantities"
    fig_timeseries.title.text_font = "sans-serif"  # pyright: ignore
    fig_timeseries.title.align = "center"  # pyright: ignore

    # x axis
    date_range_picker.update(value=(dates[0], dates[-1]), start=dates[0], end=dates[-1])

    fig_timeseries.xaxis.axis_label = "Date"
    fig_timeseries.xaxis.formatter = DatetimeTickFormatter(
        days="%d.%m.%Y", months="%m/%Y"
    )

    date_range_picker.on_change("value", date_range_input_handler)

    line_toggle.on_change("active", toggle_line_visibility)

    # style y axis
    fig_timeseries.yaxis.axis_label = "Value"
    fig_timeseries.yaxis.major_label_overrides = {
        0: "1",
        1: "2",
        2: "3",
        3: "4",
        4: "5",
    }
    fig_timeseries.yaxis.minor_tick_out = 0

    # legend
    legend = Legend(items=legend_labels)
    legend.title = "Click to show/hide!"
    legend.title_text_font_style = "italic"
    legend.click_policy = "hide"
    legend.on_event(LegendItemClick, update_line_visibility_legend_click)

    fig_timeseries.add_layout(legend, "right")


# def create_scatter_of_one_quantity(x, y):
#     source = ColumnDataSource(data=dict(date=x, value=y))
#     p = figure(x_axis_type="datetime")
#
#     p.scatter("date", "value", source=source)
#     return p


def process_file(attr, old, new):
    _, _ = attr, old
    # with open("ein-guter-plan-backup-2026-01-19-17-01-34.txt") as f:
    # raw = json.load(f)

    f = base64.b64decode(new).decode("ascii")
    raw = json.loads(f)

    dates, data = data_preparation(raw)

    # sleep_scatter = create_scatter_of_one_quantity(dates, data[Quantity.SLEEP])
    create_scatter_all_quantities(dates, data)

    row_one.children = [
        horizontal_spacer1,
        file,
        line_toggle,
        date_range_picker,
        horizontal_spacer2,
    ]
    fig_timeseries.sizing_mode = "stretch_both"
    row_two.children = [fig_timeseries]


# Use 'simple' script to work with bokeh serve
# if __name__ == "__main__":

# global widgets
file = FileInput(accept=[".txt", ".json"])
line_toggle = Toggle(label="Show connection lines", active=False)
date_range_picker = DateRangeSlider()
horizontal_spacer1 = Spacer(width_policy="max")
horizontal_spacer2 = Spacer(width_policy="max")

# file input callback
file.on_change("value", process_file)

# global storages
scatters = []
lines = []
legend_labels = []

# main timeseries figure
fig_timeseries = figure(
    x_axis_type="datetime", toolbar_location="left", tools="save, reset"
)

# layout with placeholders
row_one = row(horizontal_spacer1, file, horizontal_spacer2, sizing_mode="stretch_width")
row_two = row(sizing_mode="stretch_both")
layout = layout(children=[row_one, row_two], sizing_mode="stretch_both")
curdoc().add_root(layout)

# curdoc().theme = "dark_minimal"
