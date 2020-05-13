'''
FligthsDetector
Pavlo Semchyshyn
'''

import plotly.graph_objects as go


def create_geo_objects(coor1: list, coor2: list, origin: str, destination: str):
    '''
    Creates a web map with a line connecting two
    cities with coordinates coor1 and coor2.
    Can be displayed in browser using show()
    method
    '''
    fig = go.Figure(data=go.Scattergeo(
        lat=[coor1[0], coor2[0]],
        lon=[coor1[1], coor2[1]],
        mode='lines',
        line=dict(width=3, color='blue'),
    ))

    fig.update_layout(
        title_text=origin + '-' + destination,
        showlegend=False,
        geo=dict(
            resolution=50,
            showland=True,
            showlakes=True,
            landcolor='rgb(204, 204, 204)',
            countrycolor='rgb(204, 204, 204)',
            lakecolor='rgb(255, 255, 255)',
            projection_type="equirectangular",
            coastlinewidth=2
        )
    )
    return fig


def create_default_map_1():
    '''
    Creates a web map with a customly
    defined filters.
    Can be displayed in browser using show()
    method
    '''
    fig = go.Figure(go.Scattergeo())
    fig.update_layout(showlegend=False, geo=dict(
                            resolution=50,
                            showland=True,
                            showlakes=True,
                            landcolor='rgb(204, 204, 204)',
                            countrycolor='rgb(204, 204, 204)',
                            lakecolor='rgb(255, 255, 255)',
                            projection_type="equirectangular",
                            coastlinewidth=2
                        )
                      )
    return fig


def create_default_map_2():
    '''
    Creates a web map with a customly
    defined filters.
    Can be displayed in browser using show()
    method
    '''
    fig = go.Figure(go.Scattermapbox())
    fig.update_layout(mapbox={"style": "stamen-terrain"})
    return fig


def create_alt_lines(origin_coor: list, process_df):
    '''
    Creates a web map connecting
    20 closest cities to which there are flights
    to the city with origin_coor coordinates
    '''
    fig = go.Figure()
    count = 0
    for _, row in process_df.iterrows():
        coor = row["coordinates"]
        fig.add_trace(go.Scattermapbox(
            mode="lines",
            lon=[origin_coor[1], coor[1]],
            lat=[origin_coor[0], coor[0]],
            name=row["destination"],
            customdata=[row["destination"]]
        ))
        count += 1
        if count > 20:
            break

    fig.update_layout(
        mapbox={
            'center': {'lon': origin_coor[1], 'lat': origin_coor[0]},
            'style': "stamen-terrain",
            'zoom': 2})
    return fig
