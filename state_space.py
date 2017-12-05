
from decimal import Decimal
import plotly.offline as py
import plotly.graph_objs as go
import numpy as np


# Create random data with numpy
import numpy as np

import operator as op



import math

def nCr(n, k):
    f = math.factorial
    return Decimal(f(n)) / Decimal(f(k)) * Decimal(f((n-k)))

N = 55*55
x_values = np.arange(N)
x_values = x_values[2:]
y_values = [nCr(x, 2) for x in x_values]

print(y_values)

# Create a trace
trace = go.Scatter(
    x = x_values,
    y = y_values
)

data = [trace]

py.plot(data, filename='basic-line')