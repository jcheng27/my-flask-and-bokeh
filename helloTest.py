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

# Comment out when deploying
# if __name__ == '__main__':
#  app.run(host='0.0.0.0',debug=True)
