# standard library
import json

# other libraries - see 3rd party licenses
from bokeh.layouts import grid
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show

# local helpers
from data_preparation import data_preparation
from quantity import Quantity


def create_scatter_of_one_quantity(x, y):
    source = ColumnDataSource(data=dict(date=x, value=y))
    p = figure(x_axis_type="datetime")

    p.scatter("date", "value", source=source)
    return p


if __name__ == "__main__":
    # Load json - should be via input later
    with open("ein-guter-plan-backup-2026-01-19-17-01-34.txt") as f:
        raw = json.load(f)

    dates, data = data_preparation(raw)

    sleep_scatter = create_scatter_of_one_quantity(dates, data[Quantity.SLEEP])
    layout = grid([[sleep_scatter]], sizing_mode="stretch_both")
    show(layout)
