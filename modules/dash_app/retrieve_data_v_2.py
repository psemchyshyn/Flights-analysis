import requests
import json


BASEULR = "https://api.travelpayouts.com/v2/prices/"
URLS = {
    "latest": BASEULR + "latest",
    "month": BASEULR + "month-matrix",
    "nearest_places": BASEULR + "nearest-places-matrix",
    "week": BASEULR + "week-matrix",
}

class FlightsFounder:
    '''
    class for representing objects, which
    will serve as wrapper to travelpayouts api
    '''

    headers = {'x-access-token': 'a9664d3d8dd5b9242289e5ca43869cf8'}

    def __init__(self, origin, destination=None, currency="UAH"):
        '''
        Constructor method, initializes FlightsFounder object with
        inputted origin place and named parameters of destination("-" means
        all destinations) and currency of UAH
        '''
        self.destination = destination
        self.base_querystring = {"origin": origin, "destination": destination, "currency": currency, "show_to_affiliates": "false"}


    def get_latest_tickets(self, beginning_of_period=None, period_type=None, sorting="price") -> dict:
        '''
        Method for retrieving cheapest tickets by entering depart and return date.
        If they remain None, then the result will be covering
        random depart and return date
        Writes result to data.json file
        '''
        url = URLS["latest"]
        querystring = self.base_querystring.copy()
        querystring.update({"beginning_of_period": beginning_of_period, "period_type": period_type, "limit": "1000"})
        return self.send_request(url, querystring)

    def get_calendar_prices_month(self, month=None) -> dict:
        '''
        Method for retrieving non-stop tickets by entering depart and return date.
        If they remain None, then the result will be covering
        random depart and return date
        Writes result to data.json file
        '''
        url = URLS["month"]
        querystring = self.base_querystring.copy()
        querystring.update({"month": month})
        return self.send_request(url, querystring)

    def get_alternative_directions(self, depart_date=None, return_date=None, flexibilty=0) -> dict:
        '''
        Method for retrieving  tickets for each day in the month
        by entering depart and return date.
        If they remain None, then the result will be covering
        random depart and return date
        Writes result to data.json file
        '''
        url = URLS["nearest_places"]
        querystring = self.base_querystring.copy()
        querystring.update({"depart_date": depart_date, "return_date": return_date, "flexibilty": flexibilty})
        return self.send_request(url, querystring)

    def get_grouped_by_month_tickets(self, depart_date=None, return_date=None) -> dict:
        '''
        Method for retrieving cheapest tickets in each month(12 max)
        by entering depart and return date.
        If they remain None, then the result will be covering
        random depart and return date
        Writes result to data.json file
        '''
        url = URLS["week"]
        querystring = self.base_querystring.copy()
        querystring.update({"depart_date": depart_date, "return_date": return_date})
        return self.send_request(url, querystring)

    def send_request(self, url, querystring) -> dict:
        '''
        Method, responsible for sending http get requests to
        the entered url, writing result to json file and
        returning it as dict
        '''
        response = requests.request("GET", url, headers=FlightsFounder.headers, params=querystring).json()
        with open("dash_app/api_v_2.json", "w", encoding="utf-8") as file:
            json.dump(response, file, indent=4)
        return response




class ProcessFlights:
    def __init__(self, origin, destination):
        self.flight_founder = FlightsFounder(origin, destination)

    def get_tickets_for_filtering(self, beginning_of_period=None):
        try:
            if beginning_of_period is None:
                data_response = self.flight_founder.get_latest_tickets()["data"]
            else:
                data_response = self.flight_founder.get_latest_tickets(beginning_of_period)["data"]
        except KeyError:
            return {}
        return data_response  

    def filter_flights(self, data_response, filter_type="depart_date"):
        if filter_type == "return_date":
            new_data = {v["return_date"]: v for v in sorted(data_response, \
                key=lambda flight: flight["return_date"])}
        elif filter_type == "depart_date":
            new_data = {v["depart_date"]: v for v in sorted(data_response, \
                key=lambda flight: flight["depart_date"])}
        elif filter_type == "found_at":
            new_data = {v["found_at"]: v for v in sorted(data_response, \
                key=lambda flight: flight["found_at"])}
        return new_data


processor = ProcessFlights("Sel", "Sel")
data_response = processor.get_tickets_for_filtering()
print(processor.filter_flights(data_response))
