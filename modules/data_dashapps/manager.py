import pandas as pd
from data_dashapps.retrieve_data import FlightsFounder
from data_dashapps.cities_processing import df
from data_dashapps.geo import create_default_map_1, create_geo_objects

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


    def _extract_data(self, processor):
        '''
        A method, which extracts data from processor
        request to api
        '''
        try:
            data = processor.get_latest_tickets()["data"]
        except KeyError:
            data = []
        self.table_data = pd.DataFrame(data)
        if data:
            self.table_data.drop(["show_to_affiliates", "trip_class","actual", "number_of_changes"], axis=1, inplace=True)

    def update_data(self, origin, destination):
        '''
        Updates data with new origin and destination
        places in iata code values
        '''
        processor = FlightsFounder(origin, destination)
        self._extract_data(processor)
        self.origin = origin
        self.destination = destination

    def show_table(self):
        return self.table_data

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
            coors = list(self.cities_table[self.cities_table["code"] == place_iata].values[0][2].values())
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
            {"x": option[filt], "y": option["value"], "name": filt, "type": "line", "text": option[filt]}
            for option, filt in zip(data_to_pass, checklist_filter)
        ],
        "layout": {
            "title": "Analysis of flights from " + self.get_origin_name() + " to " + self.get_destination_name(),
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
