# standard library
import base64
import json

# other libraries - see 3rd party licenses
from bokeh.io import curdoc
from bokeh.layouts import grid
from bokeh.models import ColumnDataSource, DateRangeSlider, Legend
from bokeh.models.formatters import DatetimeTickFormatter
from bokeh.models.widgets.inputs import FileInput
from bokeh.palettes import Muted8
from bokeh.plotting import figure

from data_preparation import data_preparation

# local helpers
from quantity import QuantityLabels

# def update_plot_stats():
#     p.x_range.start = datetime_picker_min.value
#     p.x_range.end = datetime_picker_max.value


def create_scatter_all_quantities(dates, values):
    fig = figure(x_axis_type="datetime", toolbar_location="left")

    legend_labels = []
    for idx, (quan, color) in enumerate(zip(values, Muted8)):
        source = ColumnDataSource(data=dict(dates=dates, quan=quan))
        c = fig.scatter(
            x="dates", y="quan", source=source, color=color, marker="hex", size=6
        )
        c.visible = True if idx == 0 else False
        legend_labels.append((QuantityLabels.val[idx], [c]))

    # TODO: on hover: show date/value

    # style title
    fig.title = "All Tracked Quantities"
    fig.title.text_font = "sans-serif"  # pyright: ignore
    fig.title.align = "center"  # pyright: ignore

    # x axis
    date_range_picker = DateRangeSlider(
        value=(dates[0], dates[-1]), start=dates[0], end=dates[-1]
    )
    fig.xaxis.axis_label = "Date"
    fig.xaxis.formatter = DatetimeTickFormatter(days="%d.%m.%Y", months="%m/%Y")

    date_range_picker.js_link("value", fig.x_range, "start", attr_selector=0)
    date_range_picker.js_link("value", fig.x_range, "end", attr_selector=1)

    # style y axis
    fig.yaxis.axis_label = "Value"
    fig.yaxis.major_label_overrides = {0: "1", 1: "2", 2: "3", 3: "4", 4: "5"}
    fig.yaxis.minor_tick_out = 0

    # legend
    legend = Legend(items=legend_labels)
    legend.title = "Click to show/hide!"
    legend.title_text_font_style = "italic"
    legend.click_policy = "hide"

    fig.add_layout(legend, "right")

    return fig, date_range_picker


def create_scatter_of_one_quantity(x, y):
    source = ColumnDataSource(data=dict(date=x, value=y))
    p = figure(x_axis_type="datetime")

    p.scatter("date", "value", source=source)
    return p


def main(attr, old, new):
    _, _ = attr, old
    # with open("ein-guter-plan-backup-2026-01-19-17-01-34.txt") as f:
    # raw = json.load(f)
    f = base64.b64decode(new).decode("ascii")
    raw = json.loads(f)
    # print(raw)
    #
    dates, data = data_preparation(raw)

    # sleep_scatter = create_scatter_of_one_quantity(dates, data[Quantity.SLEEP])
    all_scatter, date_range_picker = create_scatter_all_quantities(dates, data)
    layout = grid(
        [[all_scatter], [date_range_picker]],
        sizing_mode="stretch_both",
    )
    # show(layout)
    curdoc().theme = "dark_minimal"
    curdoc().add_root(layout)


# Use 'simple' script to work with bokeh serve
# if __name__ == "__main__":
# Load json - should be via input later
file = FileInput(accept=[".txt", ".json"])
file.on_change("value", main)
curdoc().add_root(file)
