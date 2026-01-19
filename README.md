# Mindfulness Dashboard - Visualization for "Ein guter Plan" App Data

## The App

The small app "Ein guter Plan" by the small German brand of the same name
is a mindfulness tracker, mindfulness journal and "relaxation sound helper".
This free and digital tool focusses on some scale-tracking of different
stress-related measures to help the user keep track of their wellbeing.

## The Problem

Since July 2025, the app does not support its visualization/evaluation feature anymore.
They plan to bring it back, but there is currently no convenient way to view
an aggregated overview of the tracked values.

Even before the discontinuation of this feature,
I found the visualization a bit lacking -
it was a simple line chart with "endless scroll" to your first entry,
with the option to add or remove certain trackable values from the view.
For me, the view on a phone screen was always a bit too small for a good overview.
I also did not _love_ the plot decision to use linearly-connected lines
for the separate data points between days as that sort of implies a gradient in between.
Moreover, missed datapoints were included in this contiuous line as '0' values,
which made an overall impression of certain interconnections between different
tracked measures hard to see at a glance.

## This Project

This is where this project comes in.
I want to provide an easy-to-use interface/dashboard,
which can show the tracked data in a similar view to the one previously existing in the app
while using a plot style more fitting for discrete datapoints and
a less distracting missing-value handling.
I will possibly also include visualizations of some aggregated/averaged
values for the tracked measures.

### Scope and Stack
I will try to create a convenient interface based on the Python bokeh library.
Maybe I'll also find a way to host this as a small webapp somewhere in the future.
It should all work with data input by the user,
gathered from the "Backup" option in the app itself.
This function exports all entered data in a .txt file with the data structured in json.

### Data Description

The data put in via the app is on scales of 1-5,
with the available fields being:

- sleep ("Have you slept well and long enough?")
- mood ("How are you?")
- food ("How healthy did you eat?")
- hydration ("Did you drink enough water?")
- exercise ("Have you moved enough?")
- selfcare ("Have you done something nice for yourself?")
- social ("Did you tend to your social contacts today?")
- stress ("How high is your level of stress?")

It _should_ ideally be tracked daily,
but life can get in the way and
though you _can_ enter info on arbitrary days in the past
via the calendar,
your gut feeling of "how stressed am I" is probably not as
accurate when you try to remember a day weeks ago.

Additionally, you can add free text entries for each day,
which is intended for gratefulness journaling.
That data is not used for this project however.

## Disclaimer

I'm not involved with the company behind the app.
I don't get paid by them and
this is not supposed to be an advertisement -
I'm simply a regular user trying to get a better use out of
the data and tracking that I put in.

## Links/References

- [Website](https://einguterplan.de/app/) of the "Ein guter Plan" app.
- [Bokeh](https://bokeh.org/), the visualization library for this project.
