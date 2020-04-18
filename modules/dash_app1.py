import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import random
from dash.exceptions import PreventUpdate
from datetime import datetime, time
from dash_app.retrieve_data_v_2 import FlightsFounder, ProcessFlights

CURRENT_DATE = datetime.today()
FILTERING_NAV = {
        0: ["departure date", "depart_date"],
        1: ["return date", "return_date"],
        2: ["period of ticket's availability", "found_at"]
    }
###################### All airport cities
df = pd.read_csv("dash_app/airport_cities.csv")
options = [{"label": place, "value": iata} for place, iata in zip(df["place"], df["iata"])]
#############################
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app1 = dash.Dash(__name__, external_stylesheets=external_stylesheets, requests_pathname_prefix='/origin_destination_analysis/')


app1.layout = html.Div(children=[
    html.Div(children=[
        html.H3("Search Box"),
        html.Div(children=[
            html.Div(dcc.Dropdown(id="input_origin"), className="six columns"),
            html.Div(dcc.Dropdown(id="input_destination"), className="six columns")
        ], className="row"),
        html.Div(children=[
            dcc.RangeSlider(id="slider_filter", min=0, max=10000, step=100, value=[0, 100000])
        ], className="row", style={"margin-top": "25px", "margin-bottom": "15px"}),
        html.Div(className="row", children=html.Strong(id="slider_container")),
        html.Div(className="row", children="Chose filters on the flights search:", style={"margin-top": "25px", "font-weight": "700"}),
        html.Div(dcc.Checklist(id="filter_checklist", value=["depart_date"], options=[
            {"label": k[0], "value": k[1]} for k in FILTERING_NAV.values()
        ]), style={"margin-top": "10px"})
    ], className="four columns offset-by-one column"),

    html.Div(id="output_graph", children=[dcc.Graph(id="amgraph")], className="seven columns")
])

################# Update Slider ######################
  
@app1.callback(
    [dash.dependencies.Output("slider_filter", "max"),
    dash.dependencies.Output("slider_filter", "min"),
    dash.dependencies.Output("slider_filter", "value"),
    dash.dependencies.Output("slider_filter", "marks")],
    [dash.dependencies.Input("input_origin", "value"),
    dash.dependencies.Input("input_destination", "value")]
)
def slider_update_max_min(origin, destination):
    processor = ProcessFlights(origin, destination)
    tickets =  processor.get_tickets_for_filtering()
    if tickets:
        max_bound = max([x["value"] for x in processor.get_tickets_for_filtering()])
        min_bound = min([x["value"] for x in processor.get_tickets_for_filtering()])
    else:
        min_bound = 0
        max_bound = 10000
    return max_bound, min_bound, [min_bound, max_bound], {min_bound: f"{min_bound} UAH", max_bound: f"{max_bound} UAH"}


@app1.callback(
    dash.dependencies.Output("slider_container", "children"),
    [dash.dependencies.Input("slider_filter", "value")]
)
def update_slider_values(value):
    return f"You have chosen prices between {value[0]} and {value[1]} UAH"
############################################


@app1.callback(
    dash.dependencies.Output("amgraph", "figure"),
    [dash.dependencies.Input("slider_filter", "value"),
    dash.dependencies.Input("filter_checklist", "value"),
    dash.dependencies.Input("input_origin", "value"),
    dash.dependencies.Input("input_destination", "value")]
)
def create_graph(filter_val, checklist_filter, origin, destination):
    processor = ProcessFlights(origin, destination)
    data_response = processor.get_tickets_for_filtering()
    data_response = list(filter(lambda x: filter_val[0] <= x["value"] <= filter_val[1], data_response))
    flights_container = [processor.filter_flights(data_response, filter_type=filt) for filt in checklist_filter]
    prices_container = [[flights[k]["value"] for k in flights] for flights in flights_container]
    dates_container = [[k for k in flights] for flights in flights_container]
    try:
        origin = df.loc[df["iata"] == origin].values[0][0]
        destination = df.loc[df["iata"] == destination].values[0][0]
    except IndexError:
        origin, destination = "-", "-"
    return {
            "data": [
                {"x": dates, "y": prices, "type": "line", "name": filt, 'text': dates}
                for dates, prices, filt in zip(dates_container, prices_container, checklist_filter)
            ],
            "layout":{
                "title": "Analysis of flights from " + origin + " to " + destination,
                "xaxis": {"title": "Date"},
                "yaxis": {"title": "Price, UAH", "type": "log"}

            }
        }

############ Options of inputs ####################
@app1.callback(
    dash.dependencies.Output("input_destination", "options"),
    [dash.dependencies.Input("input_destination", "search_value")]
)
def update_options_destination(search_value):
    if not search_value:
        raise PreventUpdate
    return [o for o in options if search_value in o["label"]]


@app1.callback(
    dash.dependencies.Output("input_origin", "options"),
    [dash.dependencies.Input("input_origin", "search_value")]
)
def update_options_origin(search_value):
    if not search_value:
        raise PreventUpdate
    return [o for o in options if search_value in o["label"]]
#######################################################

if __name__ == "__main__":
    app1.run_server(debug=True)