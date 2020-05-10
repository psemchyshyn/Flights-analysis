import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.exceptions import PreventUpdate
from data_dashapps.cities_processing import calc_distance, df
from data_dashapps.retrieve_data import FlightsFounder
from data_dashapps.geo import create_alt_lines, create_default_map_2
from datetime import datetime

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app2 = dash.Dash(__name__, external_stylesheets=external_stylesheets, requests_pathname_prefix="/app2/")

CURRENT_DATE = datetime.today()

options = [{"label": place, "value": iata} for place, iata in zip(df["name"], df["code"])]


app2.layout = html.Div(children=[
    html.Nav([html.Img(src="assets/logo.svg"), html.H4("FlightsDetector")]),
    html.Div([
        html.Div(children=[
        html.H3("Search box"),
        html.Div(html.Strong("Choose date of departure:")),
        html.Div(dcc.DatePickerSingle(id="depart_date", min_date_allowed=CURRENT_DATE, placeholder="Enter a date",
                                      className="date")),
        html.Div(children=[
            html.Div(html.Strong("Origin and destination cities:"), className="row"),
            html.Div([html.Div(dcc.Dropdown(id="input_origin"), className="six columns", style={"color": "black"}),
                     html.Div(dcc.Dropdown(id="input_destination"), className="six columns", style={"color": "black"})],
                     className="row")
        ], className="row", style={"padding": "50px 5px"}),
        html.Div(html.Button("Submit", id="submit", n_clicks=0), className="button_cont")
    ], className="four columns offset-by-one column search-box"),
        html.Div(dcc.Graph(id="geo"), className="six columns")
    ], className="row"),

    html.Div([
        html.Div(
            dcc.Graph(id="alt-scatter", hoverData={}),
            className="six columns"),
        html.Div([
            dcc.Graph(id="x-times")
        ], className="five columns")
    ], className="row")
])

@app2.callback(
    [dash.dependencies.Output("alt-scatter", "figure"),
    dash.dependencies.Output("geo", "figure")],
    [dash.dependencies.Input("submit", "n_clicks")],
    [dash.dependencies.State("depart_date", "date"),
     dash.dependencies.State("input_origin", "value"),
     dash.dependencies.State("input_destination", "value")]
)
def create_graph(n_clicks, depart_date, origin, destination):
    try:
        processor = FlightsFounder(origin)
        process_df = pd.DataFrame(processor.get_latest_tickets()["data"])
        calc_distance(origin, destination, process_df)
        origin_place_coor = list(df.loc[df["code"] == origin].values[0][2].values())[:: -1]
        webmap = create_alt_lines(origin_place_coor, process_df)
        process_df.sort_values(by="depart_date", inplace=True)

    except (KeyError, IndexError):
        return {
            "data": [],
            "layout": {
                "title": "Alternative flights analysis",
                "xaxis": {"title": "Date"},
                "yaxis": {"title": "Distance, km", "type": "log"}
                }
        }, create_default_map_2()
    return {
        "data": [
            {"x": process_df["depart_date"], "y": process_df["distance"], "mode": 'markers',
             "marker": {
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'},
            },
             'customdata': process_df["destination"]
             }
        ],
        "layout": {
            "title": "Alternative flights analysis",
            "xaxis": {"title": "Date"},
            "yaxis": {"title": "Distance, km", "type": "log"},
            "hovermode": 'closest',
            "clickmode": "event+select"
        }
    }, webmap


@app2.callback(
    dash.dependencies.Output("x-times", "figure"),
    [dash.dependencies.Input("alt-scatter", "hoverData")],
    [dash.dependencies.State("input_origin", "value"),
     dash.dependencies.State("depart_date", "date")]
)
def update_x_times(chosen_point, origin, date):
    try:
        destination = chosen_point["points"][0]["customdata"]
        processor = FlightsFounder(origin, destination)
        point_df = pd.DataFrame(processor.get_latest_tickets(date)["data"])
    except KeyError:
        return {
            "data": [],
            "layout": {
                "title": "Alternative flights analysis",
                "xaxis": {"title": "Date"},
                "yaxis": {"title": "Distance, km", "type": "log"}
                }
        }
    origin = df.loc[df["code"] == origin].values[0][1]
    destination = df.loc[df["code"] == destination].values[0][1]
    point_df.sort_values(by="depart_date", inplace=True)
    return {
        "data": [
            {"x": point_df["depart_date"], "y": point_df["value"], "type": "line+markers"}
        ],
        "layout": {
            "title": "Flights from " + origin + " to " + destination,
            "xaxis": {"title": "Date"},
            "yaxis": {"title": "Price, UAH", "type": "log"}
        }
    }


############ Options of inputs ####################
@app2.callback(
    dash.dependencies.Output("input_destination", "options"),
    [dash.dependencies.Input("input_destination", "search_value")]
)
def update_options_destination(search_value):
    if not search_value:
        raise PreventUpdate
    return [option for option in options if search_value in option["label"]]


@app2.callback(
    dash.dependencies.Output("input_origin", "options"),
    [dash.dependencies.Input("input_origin", "search_value")]
)
def update_options_origin(search_value):
    if not search_value:
        raise PreventUpdate
    return [option for option in options if search_value in option["label"]]

