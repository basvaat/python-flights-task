# This is a sample Python script.


from utils import Reader
from flights import Flights
# import argparse
import sys


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    # parser = argparse.ArgumentParser()
    # parser.add_argument("exmaplefile")
    # parser.add_argument("origin")
    # parser.add_argument("destination")
    # args = parser.parse_args()

    args = sys.argv

    filename = args[1]
    origin = args[2]
    destination = args[3]

    readed_example = Reader('./example/'+filename)
    flights_data = readed_example.csv_as_list_of_dicts()

    flight = Flights(flights_data, origin, destination)
    all_routes = flight.collect_all_routes()
    print(all_routes)
