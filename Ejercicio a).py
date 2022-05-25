import pandas as pd

df = pd.read_excel('iMDb (dataset).xlsx')

df.head()


countries_split = df.copy()
countries_split['Production Countries'] = countries_split['Production Countries'].str.split(', ')
countries_split = countries_split.explode('Production Countries')
pd.unique(countries_split['Production Countries'])


countries = (countries_split.groupby(by='Production Countries')
                    .agg({'Title':'count', 'Budget': 'sum'})
                    .sort_values(by='Title',ascending=False)
                    .reset_index()
                    .rename(columns={'Title':'Number of Films','Budget':'Total Budget',"Production Countries":"Production Country"})
)
countries.head(10)


import plotly.express as px
from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)

fig = px.choropleth(countries,locationmode="country names",locations="Production Country",
                    color="Total Budget", 
                    hover_name="Production Country", 
                    color_continuous_scale=['#f0f9e8','#ccebc5','#a8ddb5','#7bccc4','#4eb3d3','#2b8cbe','#08589e']
                    )

fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor="White",
)

app.layout = html.Div([
    html.H4('Interactive map of production countries by budget'),
    dcc.Graph(id='Production Countries',
        figure=fig,
        style={'width': '200vh', 'height': '90vh'}),
])


app.run_server(debug=True)