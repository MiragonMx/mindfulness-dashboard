import json
from datetime import date
from enum import IntEnum

# from numpy import nan
import numpy as np
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure, show


class Quantity(IntEnum):
    SLEEP = 0
    MOOD = 1
    FOOD = 2
    HYDRATION = 3
    EXERCISE = 4
    SELFCARE = 5
    SOCIAL = 6
    STRESS = 7
    COUNT = 8


def main(x, y):
    source = ColumnDataSource(data=dict(date=x, value=y))
    p = figure(x_axis_type="datetime")

    # p.line(x, y, legend_label="Temp.", line_width=2)
    # p.line("date", "value", source=source, line_width=2)
    p.scatter("date", "value", source=source)
    show(p)


if __name__ == "__main__":
    # Load json - should be via input later
    with open("ein-guter-plan-backup-2026-01-19-17-01-34.txt") as f:
        raw = json.load(f)
        # print(data)

    # for d in raw:
    # print(d)

    # drop diary and settings
    ampel = raw["AMPEL"]
    # drop additional ampel info

    # print(ampel)
    # print("")
    # for a in ampel:
    # print(a)

    # print("")
    all_data_points = ampel["ampelData"]

    # print(all_data_points)

    # dates = []
    dates = set()
    for pt in all_data_points:
        dates.add(date.strptime(pt["date"], "%d.%m.%Y"))
    sorted_dates = sorted(dates)
    len_dates = len(sorted_dates)

    np_dates = np.array(sorted_dates, dtype=np.datetime64)

    # values = {
    #     "sleep": np.empty(len_dates,),
    #     "mood": [nan] * (len_dates),
    #     "food": [nan] * (len_dates),
    #     "hydration": [nan] * (len_dates),
    #     "exercise": [nan] * (len_dates),
    #     "selfcare": [nan] * (len_dates),
    #     "social": [nan] * (len_dates),
    #     "stress": [nan] * (len_dates),
    # }
    #
    data = np.empty(
        (
            Quantity.COUNT,
            len_dates,
        ),
        # dtype=np.int32,
    )
    data[:] = np.nan

    # print(values["sleep"])
    # print(len(values["sleep"]))
    # print(len_dates)
    # print(len(all_data_points))
    # print(len(all_data_points) / 8)

    idx = 0
    last_date = all_data_points[0]["date"]
    # print(all_data_points[-1])
    for pt in all_data_points:
        curr_date = date.strptime(pt["date"], "%d.%m.%Y")
        idx = sorted_dates.index(curr_date)
        if pt["type"] == "sleep":
            data[Quantity.SLEEP][idx] = pt["value"]
        if pt["type"] == "mood":
            data[Quantity.MOOD][idx] = pt["value"]
        if pt["type"] == "food":
            data[Quantity.FOOD][idx] = pt["value"]
        if pt["type"] == "hydration":
            data[Quantity.HYDRATION][idx] = pt["value"]
        if pt["type"] == "exercise":
            data[Quantity.EXERCISE][idx] = pt["value"]
        if pt["type"] == "selfcare":
            data[Quantity.SELFCARE][idx] = pt["value"]
        if pt["type"] == "social":
            data[Quantity.SOCIAL][idx] = pt["value"]
        if pt["type"] == "stress":
            data[Quantity.STRESS][idx] = pt["value"]

    # TEMPLATE STUFF:
    # prepare some data
    # x = [1, 2, 3, 4, 5]
    # y = [6, 7, 2, 4, 5]
    #
    # main(x, y)
    # print(type(values["stress"]))
    # print((values["stress"]))
    # main(dates, values["stress"].copy())
    main(np_dates, data[Quantity.SLEEP])
