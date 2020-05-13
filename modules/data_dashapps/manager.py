'''
FligthsDetector
Pavlo Semchyshyn
'''


import pandas as pd
from geopy.distance import distance
from data_dashapps.retrieve_data import FlightsFounder
from data_dashapps.cities_processing import df
from data_dashapps.geo import create_default_map_1, create_geo_objects, \
 create_default_map_2, create_alt_lines


class ManagerFlight:
    '''
    Represents ManagerFlight ADT
    for manipulating flight data
    '''
    def __init__(self):
        '''
        Inittializes ManagerFlight object
        with cities table, origin and destination
        in iata code attributes
        '''
        self.cities_table = df
        self.origin = None
        self.destination = None
        self.table_data = pd.DataFrame()


    def _extract_data(self, processor, departure=None):
        '''
        A method, which extracts data from processor
        request to api
        '''
        try:
            data = processor.get_latest_tickets(departure)["data"]
        except KeyError:
            data = []
        self.table_data = pd.DataFrame(data)
        if data:
            self.table_data.drop(["show_to_affiliates", "trip_class", "actual",
                                 "number_of_changes", "duration"], axis=1, inplace=True)

    def update_data(self, origin=None, destination=None, departure=None):
        '''
        Updates data with new origin and destination
        places in iata code values
        '''
        processor = FlightsFounder(origin, destination)
        self._extract_data(processor, departure)
        self.origin = origin
        self.destination = destination

    def show_table(self):
        '''
        Shows the beginning of the table
        in which flight data is stored
        '''
        return self.table_data.head()

    def filter_price(self, lower, upper):
        '''
        Filters prices in table_data attribute
        by indicating lower and upper boundaries of
        the price range
        '''
        if not self.table_data.empty:
            self.table_data.query("value > @lower and value < @upper", inplace=True)

    def sort_multiple(self, filters):
        '''
        Sorts stored data by indicating a list of filters.
        Returns a python list of DataFrame objects filtered
        by filter parameter if there is any data stored
        '''
        if not self.table_data.empty:
            return [self.table_data.sort_values(by=filt) for filt in filters]
        else:
            return []

    def _sort_one(self, filt):
        '''
        Helper method, sorts dataframe object
        without returning anything
        '''
        if not self.table_data.empty:
            self.table_data.sort_values(by=filt, inplace=True)

    def get_origin_coor(self):
        '''
        Returns an origin city coordiantes if
        its iata was correctly indicated else returns
        None
        '''
        return self._get_coors(self.origin)

    def get_destination_coor(self):
        '''
        Returns an destination city coordinates if
        its iata was correctly indicated else returns
        None
        '''
        return self._get_coors(self.destination)

    def _get_coors(self, place_iata):
        '''
        Helper method for processing a coordiantes of the city
        by giving its iata code
        '''
        try:
            coors = self.cities_table[self.cities_table["code"] == place_iata].values[0][2].values()
            coors = list(coors)[:: -1]
        except (IndexError, KeyError):
            coors = None
        return coors

    def get_origin_name(self):
        '''
        Returns an destination city name if
        its iata was correctly indicated else returns
        None
        '''
        return self._get_city_name(self.origin)

    def get_destination_name(self):
        '''
        Returns an destination city name if
        its iata was correctly indicated else returns
        None
        '''
        return self._get_city_name(self.destination)

    def _get_city_name(self, place_iata):
        '''
        Helper method for processing a name of the city
        by giving its iata code
        '''
        try:
            city_name = self.cities_table[self.cities_table["code"] == place_iata].values[0][1]
        except (IndexError, KeyError):
            city_name = "-"
        return city_name

    def create_layout_graph(self, checklist_filter):
        '''
        Method, which creates a layout to graph, which accepts
        a python dictionary as a input
        '''
        data_to_pass = self.sort_multiple(checklist_filter)
        return  {
            "data": [
                {"x": option[filt], "y": option["value"], "name": filt, "type": "line",
                 "text": option[filt]}
                for option, filt in zip(data_to_pass, checklist_filter)
            ],
            "layout": {
                "title": "Analysis of flights from " + self.get_origin_name() + " to " \
                     + self.get_destination_name(),
                "xaxis": {"title": "Date"},
                "yaxis": {"title": "Price, UAH", "type": "log"}
            }
        }

    def create_web_map_1(self):
        '''
        Creates interactive web map using defined
        in geo module functions
        '''
        dest_coor = self.get_destination_coor()
        origin_coor = self.get_origin_coor()
        if dest_coor and origin_coor:
            return create_geo_objects(origin_coor, dest_coor,
                                      self.get_origin_name(), self.get_destination_name())
        else:
            return create_default_map_1()

    def get_cheapest_price(self):
        '''
        Gets the price of the cheapest route
        by indicated direction
        '''
        if self.table_data.empty:
            result = 0
        else:
            result = self.table_data["value"].min()
        return result

    def get_highest_price(self):
        '''
        Gets the price of the most expensive tickets
        by indicated direction
        '''
        if self.table_data.empty:
            result = 10000
        else:
            result = self.table_data["value"].max()
        return result

    def get_data_table(self):
        '''
        Presents stored in ADT data
        as python dictionary
        '''
        return self.table_data.to_dict("records")

    def get_distance_between_points(self):
        '''
        Gets distance in kilometer between origin and
        destination
        '''
        origin_coor = self.get_origin_coor()
        dest_coor = self.get_destination_coor()
        if origin_coor and dest_coor:
            return distance(origin_coor, dest_coor).km

    def get_locations_between(self, max_distance: int) -> None:
        '''
        Sorts the table_data attribute by leaving the elements with
        distance to the final point less than max_distance
        Note:
        Can be used only if in update method destination parameter is
        set to None
        '''
        if max_distance:
            self.table_data.query("distance < @max_distance", inplace=True)

    def process_distances_for_alt_flights(self):
        '''
        Method searches and calculates the distance for alternative
        flights analysis by changing table_data attribute (adding
        new column with coordinates).
        '''
        base_distance = self.get_distance_between_points()
        self.update_data(self.origin)
        if base_distance and not self.table_data.empty:
            self.get_locations_between(base_distance)
            self._sort_one("destination")
            temp = self.cities_table[self.cities_table["code"].isin(self.table_data["destination"])]
            temp.sort_values(by="code", inplace=True)
            coordinates = []
            for _, row in temp.iterrows():
                coor = row["coordinates"]
                if isinstance(coor, dict):
                    coor = list(coor.values())[:: -1]
                    coordinates.append(coor)
                else:
                    coordinates.append(None)
            self.table_data["coordinates"] = coordinates
            self._sort_one("distance")

    def create_web_map_2(self):
        '''
        Creates a web map for app2
        '''
        if "coordinates" in self.table_data:
            result = create_alt_lines(self.get_origin_coor(), self.table_data)
        else:
            result = create_default_map_2()
        return result

    def create_bubble_layout(self):
        '''
        Creates a layout for a graph in app2
        '''
        if self.table_data.empty:
            return {
                "data": [],
                "layout": {
                    "title": "Alternative flights analysis",
                    "xaxis": {"title": "Date"},
                    "yaxis": {"title": "Distance, km", "type": "log"}
                }
        }
        else:
            return {
                "data": [
                    {
                    "x": self.table_data["depart_date"],
                    "y": self.table_data["distance"],
                    "mode": 'markers',
                    "marker": {
                        'size': 15,
                        'opacity': 0.5,
                        'line': {'width': 0.5, 'color': 'white'},
                    },
                    'customdata': self.table_data["destination"]
                    }
                ],
                "layout": {
                    "title": "Alternative flights analysis",
                    "xaxis": {"title": "Date"},
                    "yaxis": {"title": "Distance, km", "type": "log"},
                    "hovermode": 'closest',
                    "clickmode": "event+select"
                }
            }
