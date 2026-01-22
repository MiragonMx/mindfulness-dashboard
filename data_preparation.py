# standard library
from datetime import date

# other libraries - see 3rd party licenses
import numpy as np

# local helpers
from quantity import Quantity


def data_preparation(raw):
    # drop diary and settings
    ampel = raw["AMPEL"]
    # drop additional ampel info
    all_data_points = ampel["ampelData"]

    # get all dates with *any* quantity entered and convert to valid datetime
    dates = set()
    for pt in all_data_points:
        dates.add(date.strptime(pt["date"], "%d.%m.%Y"))
    # create numpy array of ordered dates for interfacing with other data
    np_dates = np.array(sorted(dates), dtype=np.datetime64)

    # create matrix of size: (quantities x dates) for data storage
    # use enum for convenient/readable indexing
    data = np.empty(
        (
            Quantity.COUNT,
            np_dates.size,
        ),
        # dtype=np.int32,  <-- would be cleaner, but NaN cant be int...
    )
    # initialize with NaN
    data[:] = np.nan

    # fill data matrix:
    # 1. get date of current datapoint
    # 2. get index of that date in all sorted
    # 3. set value at the respective quantities row index in data matrix

    # TODO: may be possible to merge both all_data_points loops,
    # but json might not be fully date sorted so might be tricky...
    # This is done just once when reading anyways so
    # it should not have a big impact - not too much data expected anyways

    idx = 0
    for pt in all_data_points:
        curr_date = date.strptime(pt["date"], "%d.%m.%Y")
        idx = np.where(np_dates == curr_date)[0][0]
        if pt["type"] == "sleep":
            data[Quantity.SLEEP][idx] = pt["value"]
            continue
        if pt["type"] == "mood":
            data[Quantity.MOOD][idx] = pt["value"]
            continue
        if pt["type"] == "food":
            data[Quantity.FOOD][idx] = pt["value"]
            continue
        if pt["type"] == "hydration":
            data[Quantity.HYDRATION][idx] = pt["value"]
            continue
        if pt["type"] == "exercise":
            data[Quantity.EXERCISE][idx] = pt["value"]
            continue
        if pt["type"] == "selfcare":
            data[Quantity.SELFCARE][idx] = pt["value"]
            continue
        if pt["type"] == "social":
            data[Quantity.SOCIAL][idx] = pt["value"]
            continue
        if pt["type"] == "stress":
            data[Quantity.STRESS][idx] = pt["value"]
            continue

    return np_dates, data
