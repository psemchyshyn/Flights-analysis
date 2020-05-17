'''
FligthsDetector
Pavlo Semchyshyn
'''

import sys

# adding to path so could be runnable from top-package level 
sys.path.append('./')

from modules.data_dashapps.manager import ManagerFlight


def example_run(origin, destination):
    '''
    Shows examples of basic operations with ADT
    ManagerFlight
    '''
    manager = ManagerFlight()
    manager.update_data(origin, destination)
    print("Example of ADT work with Paris and Berlin cities\n")
    print(f"Origin city: {manager.get_origin_name()}, Destination city: {manager.get_destination_name()}\n")
    print(f"Cheapest ticket price(UAH): {manager.get_cheapest_price()}, The most expensive ticket \
price(UAH): {manager.get_highest_price()}\n")
    print(f"Origin city coordinates: {manager.get_origin_coor()}, Destination city coordinates: \
{manager.get_destination_coor()}\n")
    print(f"Distance(km) between points: {manager.get_distance_between_points()}\n")
    print(f"Data structuring:\n {manager.show_table()}\n")


def example_webmap_alt_flights(origin, destination):
    '''
    Creates example webmap with alternative
    flights opportunities
    Can be displayed in browser via show() method
    (uses Berlin and Paris cities as example)
    '''
    manager = ManagerFlight()
    manager.update_data(origin, destination)
    manager.process_distances_for_alt_flights()
    return manager.create_web_map_2()

def example_webmap_origin_dest(origin, destination):
    '''
    Creates web map visulisation of route
    from origin to destination places
    (in example cities are Paris and Bangkok)
    Can be displayed in browser via show() method
    '''
    manager = ManagerFlight()
    manager.update_data(origin, destination)
    return manager.create_web_map_1()


def user_input():
    '''
    Gets the user input of origin and destination
    cities
    '''
    while True:
        origin = input("Enter the origin city IATA code: ")
        if len(origin) != 3 or not origin.isupper():
            print("Origin is not an IATA code")
            continue
        else:
            break
    while True:
        destination = input("Enter the destination city IATA code: ")
        if len(destination) != 3 or not destination.isupper():
            print("Destination is not an IATA code")
            continue
        else:
            break
    return origin, destination


if __name__ == "__main__":
    origin, destination = user_input()
    example_run(origin, destination)
    example_webmap_origin_dest(origin, destination).show()
    example_webmap_alt_flights(origin, destination).show()
