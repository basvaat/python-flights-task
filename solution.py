
from utils import Reader
from flights import Flights
import argparse

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type=str)
    parser.add_argument("origin", type=str)
    parser.add_argument("destination", type=str)
    parser.add_argument('--bags', type=int, required=True)
    args = parser.parse_args()
    
    readed_example = Reader('./example/'+args.filename)
    flights_data = readed_example.csv_as_list_of_dicts()

    flight = Flights(flights_data, args.origin, args.destination, args.bags)
    all_routes = flight.collect_all_routes()
    print(all_routes)
