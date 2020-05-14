'''
FligthsDetector
Pavlo Semchyshyn
'''

import sys

# adding to path so could be runnable from top-package level 
sys.path.append('./')

from modules.data_dashapps.manager import ManagerFlight


def example_run():
    '''
    Shows examples of basic operations with ADT
    ManagerFlight
    '''
    manager = ManagerFlight()
    manager.update_data("PAR", "BER")
    print("Example of ADT work with Paris and Berlin cities\n")
    print(f"Origin city: {manager.get_origin_name()}, Destination city: {manager.get_destination_name()}\n")
    print(f"Cheapest ticket price(UAH): {manager.get_cheapest_price()}, The most expensive ticket \
price(UAH): {manager.get_highest_price()}\n")
    print(f"Origin city coordinates: {manager.get_origin_coor()}, Destination city coordinates: \
{manager.get_destination_coor()}\n")
    print(f"Distance(km) between points: {manager.get_distance_between_points()}\n")
    print(f"Data structuring:\n {manager.show_table()}\n")


def example_webmap_alt_flights():
    '''
    Creates example webmap with alternative
    flights opportunities
    Can be displayed in browser via show() method
    (uses Berlin and Paris cities as example)
    '''
    manager = ManagerFlight()
    manager.update_data("PAR", "BER")
    manager.process_distances_for_alt_flights()
    return manager.create_web_map_2()

def example_webmap_origin_dest():
    '''
    Creates web map visulisation of route
    from origin to destination places
    (in example cities are Paris and Bangkok)
    Can be displayed in browser via show() method
    '''
    manager = ManagerFlight()
    manager.update_data("PAR", "HKT")
    return manager.create_web_map_1()

if __name__ == "__main__":
    example_run()
