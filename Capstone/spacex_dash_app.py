# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

launch_sites = list(spacex_df['Launch Site'].unique())
launch_sites.append('All Sites')

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown', options=launch_sites, value='All Sites'),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000,
                                                step=1000, value=[min_payload, max_payload]
                                                ),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)

def pie_chart(option):
  if option == 'All Sites':
    success_df = spacex_df[spacex_df['class'] == 1]
    fig = px.pie(
        data_frame=success_df,
        names='Launch Site',
        title='Total Success by Launch Sites'
        # values='class'
    )
  else:
    launch_df = spacex_df[spacex_df['Launch Site'] == option]
    fig = px.pie(
        data_frame=launch_df,
        names='class',
        title=f'Total Success Launchs for site {option}'
        # values='Flight Number'
    )
  return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)

def scatter(site, range):
  range_df = spacex_df[spacex_df['Payload Mass (kg)'].between(range[0], range[1])]
  if site == 'All Sites':
    fig = px.scatter(
        data_frame=range_df,
        x='Payload Mass (kg)',
        y='class',
        color="Booster Version Category",
        title='Correlation between Payload and Success for all Sites'
    )
  else:
    site_range_df = range_df[range_df['Launch Site'] == site]
    fig = px.scatter(
        data_frame=site_range_df,
        x='Payload Mass (kg)',
        y='class',
        color="Booster Version Category",
        title=f'Correlation between Payload and Success for site {site}'
    )
  return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
