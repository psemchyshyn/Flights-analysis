'''
FligthsDetector
Pavlo Semchyshyn
'''

from datetime import datetime
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
from dash.exceptions import PreventUpdate
from data_dashapps.manager import ManagerFlight
from data_dashapps.cities_processing import df

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app1 = dash.Dash(__name__, external_stylesheets=external_stylesheets, requests_pathname_prefix="/app1/")


CURRENT_DATE = datetime.today()
FILTERING_NAV = {
        0: ["departure date", "depart_date"],
        1: ["return date", "return_date"],
        2: ["period of ticket's availability", "found_at"]
    }
MANAGER = ManagerFlight()
options = [{"label": place, "value": iata} for place, iata in zip(df["name"], df["code"])]
cols = ["value", "return_date", "origin", "gate", "found_at", "duration", "distance", "destination", "depart_date"]


app1.layout = html.Div(children=[
    html.Nav([html.Img(src="assets/logo.svg"), html.H4("FlightsDetector")]),
    html.Div([
        html.Div(children=[
            html.H3("Search Box"),
            html.Div(children=[
                html.Div(html.Span("Origin place"), className="six columns"),
                html.Div(html.Span("Destination place"), className="six columns")
            ], className="row"),
            html.Div(children=[
                html.Div(dcc.Dropdown(id="input_origin"), className="six columns", style={"color": "black"}),
                html.Div(dcc.Dropdown(id="input_destination"), className="six columns", style={"color": "black"})
            ], className="row"),
            html.Div(children=[html.Span("Indicate price range:"),
                               dcc.RangeSlider(id="slider_filter", min=0, max=10000, step=100, value=[0, 100000])
                               ], className="row", style={"margin-top": "25px", "margin-bottom": "15px"}),
            html.Div(className="row", children=html.Strong(id="slider_container")),
            html.Div(className="row", children="Chose filters on the flights search:", style={"margin-top": "25px",
                                                                                              "font-weight": "700"}),
            html.Div(dcc.Checklist(id="filter_checklist", value=["depart_date"], options=[
                {"label": k[0], "value": k[1]} for k in FILTERING_NAV.values()
            ]), style={"margin-top": "10px"})
        ], className="four columns offset-by-one column search-box"),

        html.Div(id="output_graph", children=[dcc.Graph(id="amgraph")], className="seven columns")
    ], style={"color": "white", "margin-bottom": "40px"}, className="row"),
    html.Div([
        html.Div(dcc.Graph(id="geo"), className="six columns"),
        html.Div([dash_table.DataTable(id="data_table",
                                       style_table={'maxHeight': '400px', 'overflowY': 'scroll', 'overflowX': 'scroll'},
                                       style_data={},
                                       fixed_rows={'headers': True, 'data': 0},
                                       style_cell={
                                           'minWidth': '0px', 'maxWidth': '180px',
                                           'overflow': 'hidden',
                                           'textOverflow': 'ellipsis',
                                       },
                                       style_cell_conditional=[
                                           {
                                               'if': {'column_id': col},
                                               'textAlign': 'left'
                                           } for col in cols
                                       ],
                                       style_header={
                                           'backgroundColor': 'white',
                                           'fontWeight': 'bold'
                                       },
                                       columns=[{"name": col, "id": col} for col in cols])],
                 className="six columns")
    ], className="row")
])

################# Update Slider ######################
@app1.callback(
    [dash.dependencies.Output("slider_filter", "max"),
     dash.dependencies.Output("slider_filter", "min"),
     dash.dependencies.Output("slider_filter", "value"),
     dash.dependencies.Output("slider_filter", "marks"),
     dash.dependencies.Output("data_table", "data")],
    [dash.dependencies.Input("input_origin", "value"),
     dash.dependencies.Input("input_destination", "value")]
)
def slider_update_max_min(origin, destination):
    MANAGER.update_data(origin, destination)
    max_bound = MANAGER.get_highest_price()
    min_bound = MANAGER.get_cheapest_price()
    marks = {min_bound: {"label": f"{min_bound} UAH", "style": {"color": "white"}},
             max_bound: {"label": f"{max_bound} UAH", "style": {"color": "white"}}}
    return max_bound, min_bound, [min_bound, max_bound], marks, MANAGER.get_data_table()


@app1.callback(
    dash.dependencies.Output("slider_container", "children"),
    [dash.dependencies.Input("slider_filter", "value")]
)
def update_slider_values(value):
    return f"You have chosen prices between {value[0]} and {value[1]} UAH"
############################################


@app1.callback(
    [dash.dependencies.Output("amgraph", "figure"),
    dash.dependencies.Output("geo", "figure")],
    [dash.dependencies.Input("slider_filter", "value"),
     dash.dependencies.Input("filter_checklist", "value"),
     dash.dependencies.Input("input_origin", "value"),
     dash.dependencies.Input("input_destination", "value")]
)
def create_graph(filter_val, checklist_filter, origin, destination):
    MANAGER.update_data(origin, destination)
    MANAGER.filter_price(filter_val[0], filter_val[1])
    return MANAGER.create_layout_graph(checklist_filter), MANAGER.create_web_map_1()


############ Options of inputs ####################
@app1.callback(
    dash.dependencies.Output("input_destination", "options"),
    [dash.dependencies.Input("input_destination", "search_value")]
)
def update_options_destination(search_value):
    if not search_value:
        raise PreventUpdate
    return [option for option in options if search_value in option["label"]]


@app1.callback(
    dash.dependencies.Output("input_origin", "options"),
    [dash.dependencies.Input("input_origin", "search_value")]
)
def update_options_origin(search_value):
    if not search_value:
        raise PreventUpdate
    return [option for option in options if search_value in option["label"]]
