
from utils import Reader
from flights import Flights
import argparse

if __name__ == '__main__':

    # parse arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    parser.add_argument("origin", type=str)
    parser.add_argument("destination", type=str)
    parser.add_argument('--bags', type=int, required=True)
    args = parser.parse_args()

    # read in file
    readed_example = Reader('./example/'+args.filename)
    flights_data = readed_example.csv_as_list_of_dicts()

    # collect all routes and print
    flight = Flights(flights_data, args.origin, args.destination, args.bags)
    flight.check_user_input()
    print(flight.collect_all_routes())
