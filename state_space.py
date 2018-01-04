
from decimal import Decimal
import plotly.offline as py
import plotly.graph_objs as go
import numpy as np
# Create random data with numpy
import numpy as np
import operator as op
import math
import scipy
import scipy.special


def nCr(n, k):
    f = math.factorial
    return Decimal(f(n)) / Decimal(f(k)) * Decimal(f((n-k)))


comb = scipy.special.comb(64, 32)

N = 37*37
x_values = np.arange(N)
x_values = x_values[2:]
y_values = [scipy.special.comb(x, 2) for x in x_values]
max_val = max(y_values)


map_sizes = [
    (7, 7, True),
    (9, 9, False),
    (11, 11, True),
    (13, 13, False),
    (15, 15, True),
    (17, 17, False),
    (19, 19, True),
    (25, 25, False),
    (35, 35, True),
]




# Create a trace
trace = go.Scatter(
    x = x_values,
    y = y_values,
    name="Complexity"
)

trace1 = go.Scatter(
    x=[x*y for x, y, show in [(x, y, show) for x, y, show in map_sizes if show]],
    y=[max_val * 1.03 for x, y, show in [(x, y, show) for x, y, show in map_sizes if show]],
    text=["%sx%s" % (x, y) for x, y, show in [(x, y, show) for x, y, show in map_sizes if show]],
    mode="text",
    name="Maze Size/N-states"
)

trace2 = go.Scatter(
    x=[(x*y) for x, y, show in [(x, y, show) for x, y, show in map_sizes if show]],
    y=[max_val * 1.01 for x, y, show in [(x, y, show) for x, y, show in map_sizes if show]],
    text=["%s" % int(scipy.special.comb(x*y, 2)) for x, y, show in [(x, y, show) for x, y, show in map_sizes if show]],
    mode="text",
    name="States",
    showlegend=False,
)


data = [trace, trace1, trace2]

layout = {
    #'title': "Deep Maze State-Space",
    'font':dict( size=20, color='#7f7f7f'),
    'xaxis': {
        'range': [0, N],
        'showticklabels': False,
        "title": "Maze Size"
    },
    'yaxis': {
        'range': [0, max_val * 1.10],
        'tickformat': '',
        'title': "Complexity"
    },
    'shapes': [
        # Line Vertical
        {
            'type': 'line',
            'x0': x*y,
            'y0': 0,
            'x1': x*y,
            'y1': max_val,
            'line': {
                'color': 'rgb(255, 0, 0)',
                'width': 3,
            },
        } for x, y, show in map_sizes
    ]
}
fig = {
    'data': data,
    'layout': layout,
}
py.plot(
    fig,
    filename='basic-line')
