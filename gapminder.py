import pandas as pd
data = pd.read_csv('https://assets.datacamp.com/production/repositories/401/datasets/09378cc53faec573bcb802dce03b01318108a880/gapminder_tidy.csv',index_col='Year')
print(data.head())

# Make a list of the unique values from the region column: regions_list
regions_list = data.region.unique().tolist()

# Perform necessary imports
from bokeh.models import ColumnDataSource, Select, Slider, HoverTool, Legend
# from bokeh.io import curdoc
from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row, widgetbox

# Import CategoricalColorMapper from bokeh.models and the Spectral6 palette from bokeh.palettes
from bokeh.models import CategoricalColorMapper
from bokeh.palettes import Spectral6

# Make the ColumnDataSource: source
source = ColumnDataSource(data={
    'x'       : data.loc[1970].fertility,
    'y'       : data.loc[1970].life,
    'country' : data.loc[1970].Country,
    'pop'     : (data.loc[1970].population / 20000000) + 2,
    'region'  : data.loc[1970].region,
})

# Save the initial minimum and maximum values of the fertility column: xmin, xmax
xmin, xmax = min(data.fertility), max(data.fertility)

# Save the initial minimum and maximum values of the life expectancy column: ymin, ymax
ymin, ymax = min(data.life), max(data.life)

# Make a color mapper: color_mapper
color_mapper = CategoricalColorMapper(factors=regions_list, palette=Spectral6)

# Create the figure: plot
plot = figure(name="bokeh_jinja_figure",title='Gapminder Data for 1970', plot_height=400, plot_width=700,
              x_range=(xmin, xmax), y_range=(ymin, ymax))

# Set the legend outside
plot.add_layout(Legend(), 'right')

# Add the color mapper to the circle glyph
plot.circle(x='x', y='y', fill_alpha=0.8, source=source,
            color=dict(field='region', transform=color_mapper), legend='region')

# Legend inside the plot (top right)
# plot.legend.location = 'top_right'

# Set the initial x-axis label
# plot.xaxis.axis_label ='Fertility (children per woman)'

# Set the initial y-axis label
# plot.yaxis.axis_label = 'Life Expectancy (years)'

# Define the callback function: update_plot
def update_plot(attr, old, new):
    # Read the current value off the slider and 2 dropdowns: yr, x, y
    yr = slider.value
    x = x_select.value
    y = y_select.value
    # Label axes of plot
    plot.xaxis.axis_label = x
    plot.yaxis.axis_label = y
    # Set new_data
    new_data = {
        'x'       : data.loc[yr][x],
        'y'       : data.loc[yr][y],
        'country' : data.loc[yr].Country,
        'pop'     : (data.loc[yr].population / 20000000) + 2,
        'region'  : data.loc[yr].region,
    }
    # Assign new_data to source.data
    source.data = new_data

    # Set the range of all axes
    plot.x_range.start = min(data[x])
    plot.x_range.end = max(data[x])
    plot.y_range.start = min(data[y])
    plot.y_range.end = max(data[y])

    # Add title to plot
    plot.title.text = 'Gapminder data for %d' % yr

# Make a slider object: slider
slider = Slider(title='Year',start=1970, end=2010, step=1, value=1970)

# Attach the callback to the 'value' property of slider
slider.on_change('value',update_plot)

# Create a HoverTool: hover
hover = HoverTool(tooltips=[('Country','@country')])

# Add the HoverTool to the plot
plot.add_tools(hover)

# Create a dropdown Select widget for the x data: x_select
x_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='fertility',
    title='x-axis data'
)

# Attach the update_plot callback to the 'value' property of x_select
x_select.on_change('value', update_plot)

# Create a dropdown Select widget for the y data: y_select
y_select = Select(
    options=['fertility', 'life', 'child_mortality', 'gdp'],
    value='life',
    title='y-axis data'
)

# Attach the update_plot callback to the 'value' property of y_select
y_select.on_change('value', update_plot)

curdoc().title = 'Gapminder'
# Create layout and add to current document
layout = row(widgetbox(slider, x_select, y_select), plot)
curdoc().add_root(layout)