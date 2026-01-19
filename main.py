import json
from datetime import date

from numpy import nan

#
# def main(x, y):
#     p = figure(title="Simple Line", x_axis_label="x", y_axis_label="y")
#     # p.line(x, y, legend_label="Temp.", line_width=2)
#     show(p)


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

    values = {
        "sleep": [nan] * (len_dates),
        "mood": [nan] * (len_dates),
        "food": [nan] * (len_dates),
        "hydration": [nan] * (len_dates),
        "exercise": [nan] * (len_dates),
        "selfcare": [nan] * (len_dates),
        "social": [nan] * (len_dates),
        "stress": [nan] * (len_dates),
    }

    print(values["sleep"])
    print(len(values["sleep"]))
    print(len_dates)
    print(len(all_data_points))
    print(len(all_data_points) / 8)

    idx = 0
    last_date = all_data_points[0]["date"]
    print(all_data_points[-1])
    for pt in all_data_points:
        curr_date = date.strptime(pt["date"], "%d.%m.%Y")
        idx = sorted_dates.index(curr_date)
        if pt["type"] == "sleep":
            values["sleep"][idx] = pt["value"]
        if pt["type"] == "mood":
            values["mood"][idx] = pt["value"]
        if pt["type"] == "food":
            values["food"][idx] = pt["value"]
        if pt["type"] == "hydration":
            values["hydration"][idx] = pt["value"]
        if pt["type"] == "exercise":
            values["exercise"][idx] = pt["value"]
        if pt["type"] == "selfcare":
            values["selfcare"][idx] = pt["value"]
        if pt["type"] == "social":
            values["social"][idx] = pt["value"]
        if pt["type"] == "stress":
            values["stress"][idx] = pt["value"]

    # for date in sorted_dates:
    # print(date)

    print(values["sleep"])
    print(values["mood"])
    print(values["food"])
    print(values["stress"])

    # for val in values["mood"]:
    # print(val)

    #     curr_date = date.strptime(pt["date"], "%d.%m.%Y")
    #     if not (dates[-1] == curr_date):
    #         dates.append(curr_date)
    #         for key, val in values:
    #             val.append(nan)
    #

    # for date in sorted_dates:
    #     print(date)

    # TEMPLATE STUFF:
    # prepare some data
    # x = [1, 2, 3, 4, 5]
    # y = [6, 7, 2, 4, 5]
    #
    # main(x, y)
