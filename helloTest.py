# follow along https://medium.com/better-programming/building-your-first-website-with-flask-part-5-e389fff0c8ec

# run flask without venv localhost:5000 or http://127.0.0.1:5000/

# at the end point / call method hello which returns "hello world"
from flask import Flask, render_template, url_for
app = Flask(__name__)

@app.route('/<page_name>')
def html_page(page_name):
	return render_template(page_name)

def factors(num):
  return [x for x in range (1, num+1) if num%x==0]

@app.route('/factor_raw/<int:n>')
def factors_display_raw_html(n):
  list_factor = factors(int(n))
  # adding "n" and placed at the top
  html = "<h1> Factors of "+str(n)+" are</h1>"+"\n"+"<ul>"
  # make a <li> item for every output (factor)
  for f in list_factor:
    html += "<li>"+str(f)+"</li>"+"\n"
  html += "</ul> </body>" # closes tag at the end
  return html

@app.route("/")
def hello():
  return render_template('home.html')
  # return 'I just ran a Flask app without venv'

@app.route("/about")
def about():
  return render_template("about.html")

Pokemons =["Pikachu", "Charizard", "Squirtle", "Jigglypuff", "Bulbasaur", "Gengar", "Charmander", "Mew", "Lugia", "Gyarados"]
@app.route("/pokemons")
def pokemons():
  return render_template("pokemons.html",len = len(Pokemons), Pokemons = Pokemons)

import numpy as np
from bokeh.plotting import figure
from bokeh.embed import components
from bokeh.models import (HoverTool, FactorRange, Plot, LinearAxis, Grid,
                          Range1d)
from bokeh.models.glyphs import VBar
# from bokeh.charts import Bar
from bokeh.models.sources import ColumnDataSource
from bokeh.io import curdoc

@app.route('/circle')
def index():
    x = np.arange(2, 50, step=.5)
    y = np.sqrt(x) + np.random.randint(2,50)
    plot = figure(plot_width=400, plot_height=400,title=None, toolbar_location="below")
    plot.line(x,y)

    script, div = components(plot)
    kwargs = {'script': script, 'div': div}
    kwargs['title'] = 'bokeh-with-flask'
    return render_template('circle.html', **kwargs)

@app.route("/redchart/<int:bars_count>/")

def redchart(bars_count):
    if bars_count <= 0:
        bars_count = 1

    data = {"days": [], "bugs": [], "costs": []}
    for i in range(1, bars_count + 1):
        data['days'].append('Day ' + str(i))
        data['bugs'].append(np.random.randint(1,100))
        data['costs'].append(np.random.uniform(1.00, 1000.00))

    source = ColumnDataSource(data)
    x_name, y_name = "days", "bugs"
    xdr = FactorRange(factors=data[x_name])
    ydr = Range1d(start=0,end=max(data[y_name])*1.5)
    print('Days:',data['days'])
    print('Bugs:',data[y_name])
    print('Costs:',data['costs'])
    plot = figure(title="Bugs found per day",x_range=data[x_name],y_range=ydr, height=400)
    plot.vbar(x=x_name, top=y_name, source=data, width=0.9, line_color="#e12127", fill_color="#e12127")

    # Create a HoverTool: hover
    hover = HoverTool(tooltips=[('Cost','@costs{0.00}')])

    # Add the HoverTool to the plot
    plot.add_tools(hover)

    script, div = components(plot)
    kwargs = {'script': script, 'div': div}

    # fruits = ['Apples', 'Pears', 'Nectarines', 'Plums', 'Grapes', 'Strawberries']
    # counts = [5, 3, 4, 2, 4, 6]
    #
    # plot = figure(x_range=fruits, plot_height=250, title="Fruit Counts",
    #            toolbar_location=None, tools="")
    #
    # plot.vbar(x=fruits, top=counts, width=0.9)
    #
    # script, div = components(plot)
    # kwargs = {'script': script, 'div': div}
    return render_template("redchart.html", bars_count=bars_count, **kwargs)

@app.route("/scatter")
def scatter():
  # scatter.py

  # create some data
  x1 = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
  y1 = [0, 8, 2, 4, 6, 9, 5, 6, 25, 28, 4, 7]
  x2 = [2, 5, 7, 15, 18, 19, 25, 28, 9, 10, 4]
  y2 = [2, 4, 6, 9, 15, 18, 0, 8, 2, 25, 28]
  x3 = [0, 1, 0, 8, 2, 4, 6, 9, 7, 8, 9]
  y3 = [0, 8, 4, 6, 9, 15, 18, 19, 19, 25, 28]

  # select the tools we want
  TOOLS="pan,wheel_zoom,box_zoom,reset,save"

  # the red and blue graphs will share this data range
  xr1 = Range1d(start=0, end=30)
  yr1 = Range1d(start=0, end=30)

  # only the green will use this data range
  xr2 = Range1d(start=0, end=30)
  yr2 = Range1d(start=0, end=30)

  # build our figures
  p1 = figure(x_range=xr1, y_range=yr1, tools=TOOLS, plot_width=300, plot_height=300)
  p1.scatter(x1, y1, size=12, color="red", alpha=0.5)

  p2 = figure(x_range=xr1, y_range=yr1, tools=TOOLS, plot_width=300, plot_height=300)
  p2.scatter(x2, y2, size=12, color="blue", alpha=0.5)

  p3 = figure(x_range=xr2, y_range=yr2, tools=TOOLS, plot_width=300, plot_height=300)
  p3.scatter(x3, y3, size=12, color="green", alpha=0.5)

  # plots can be a single Bokeh Model, a list/tuple, or even a dictionary
  plots = {'Red': p1, 'Blue': p2, 'Green': p3}

  script, div = components(plots)
  kwargs = {'script': script, 'div': div}
  print(script)
  print(div)
  return render_template("boilerplate.html", **kwargs)

# Comment out when deploying
# if __name__ == '__main__':
#   app.run(host='0.0.0.0',debug=True)
