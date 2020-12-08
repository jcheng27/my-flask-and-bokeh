import numpy as np
from bokeh.plotting import figure
from bokeh.io import curdoc
from bokeh.embed import components
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
# from bokeh.charts import Bar
from bokeh.models.sources import ColumnDataSource

# data = {"days": [], "bugs": [], "costs": []}
# for i in range(1, bars_count + 1):
#     data['days'].append(i)
#     data['bugs'].append(np.random.randint(1,100))
#     data['costs'].append(np.random.uniform(1.00, 1000.00))

# plot = figure(title="Bugs found per day")
# plot.vbar(x=['a','b','c'], top=[10, 20, 30], width=0.9)

fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
counts = [5, 3, 4, 2, 4, 6]

plot = figure(x_range=fruits, plot_height=250, title="Fruit Counts",
           toolbar_location=None, tools="")

plot.vbar(x=fruits, top=counts, width=0.9)

# curdoc().add_root(p)
# curdoc().add_root(plot)
