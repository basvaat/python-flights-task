import itertools
from datetime import timedelta, datetime
from utils import DateHandler
import json
class Flights:
    """Collects possible routes based on user inputs (origin, destionation, number of bags)"""
    def __init__(self, flights_data, origin, destination, bags):
        self.flights_data = flights_data
        self.origin = origin
        self.destination = destination
        self.bags = bags

    def bag_number_error(self):
        """Raise Error if number of bags >10."""
        if int(self.bags) > 10:
            raise ValueError('Maximum 10 bags allowed as argument')

    def origins_destinations_error(self):
        """Raise Error if origin or destination is not correct."""
        if self.origin not in self.origins or self.destination not in self.destinations:
            raise ValueError('Origin or destination is not correct')

    def get_origins_and_destinations(self):
        """Collects all destinations and origins from dataset."""
        self.destinations = set(
            map(lambda flight: flight['destination'], self.flights_data.values()))
        self.origins = set(
            map(lambda flight: flight['origin'], self.flights_data.values()))

    def get_all_possible_routes(self):
        """Collect all possible routes based on input data, not only direct routes."""
        all_routes = []
        all_airports = self.origins.union(self.destinations)
        for i in range(2, len(all_airports)+1):
            all_routes.append(list(itertools.permutations(all_airports, i)))
        all_routes = list(itertools.chain.from_iterable(all_routes))
        return all_routes

    def select_possible_routes(self, all_routes):
        """Selects only possible routes from origin to destination"""
        selected_possible_routes = []
        for route in all_routes:
            if route[0] == self.origin and route[-1] == self.destination:
                selected_possible_routes.append(route)
        return selected_possible_routes

    def get_all_planes_with_selected_routes(self, selected_possible_routes):
        """Groups the possible routes based on flights.
        eg. Route: A->B->C, groups: A->B, B->C
        """
        groups = {}
        for route in selected_possible_routes:
            subroutes = {}  # if route:a->b->c: subroutes: a->b and b->c
            for i in range(len(route)-1):
                possible_planes = []
                for id in self.flights_data:
                    flight = self.flights_data[id]
                    if flight['origin'] == route[i] and flight['destination'] == route[i+1]:
                        possible_planes.append(flight)
                subroutes[(route[i], route[i+1])] = possible_planes
            groups[route] = subroutes
        return groups

    def is_flight_eligible(self, flight, prev_flight):
        """Filter flights for allowed number of bags and overlay time."""
        return (int(flight["bags_allowed"]) > self.bags and timedelta(hours=1) <= datetime.fromisoformat(flight["departure"]) - datetime.fromisoformat(prev_flight["arrival"]) <= timedelta(hours=6))

    def conditional_product(self, *subroutes):
        """Get cartesian product of the subroutes and filter for conditions
        (if route A->B->C, subroutes: all flights A->B and B->C)
        conditions: number of bags, overlay time
        """
        result = [[]]
        for subroute in subroutes:
            result = [flights+[subroute[i]] for flights in result for i in range(0, len(subroute))
                      if len(flights) == 0 or self.is_flight_eligible(subroute[i], flights[-1])]
        for flights in result:
            yield tuple(flights)

    def get_all_flights_in_correct_format(self, groups):
        """Collects all flights in correct format."""
        all_flights = []
        for routes in groups:
            # direct flights
            if len(routes) == 2:
                subroute = list(groups[routes].keys())[0]
                assert routes == subroute
                for flight in groups[routes][subroute]:
                    all_flights.append({'flights': [flight]})
            # not direct fligths
            else:
                all_combinations = self.conditional_product(
                    *groups[routes].values())
                for flight in all_combinations:
                    all_flights.append({'flights': list(flight)})
        return all_flights

    def add_flight_details(self, all_flights):
        """Add flight details 
        (bags_allowed, bags_count, destination, origin, total_price, travel_time)
        """
        for flights in all_flights:
            # details to collect
            bags_allowed = 10
            bags_count = int(self.bags)
            destination = None
            origin = None
            total_price = 0
            travel_time = timedelta(0)
            departure_time = None
            arrival_time = None
            # get details of flights
            last_flight = flights['flights'][-1]
            destination = last_flight['destination']
            arrival_time = DateHandler.convert_datetime(last_flight['arrival'])
            first_flight = flights['flights'][0]
            origin = first_flight['origin']
            departure_time = DateHandler.convert_datetime(
                first_flight['departure'])
            travel_time_delta = DateHandler.calculate_date_difference(
                departure_time, arrival_time)
            travel_time = DateHandler.convert_timedelta_to_datetime(
                travel_time_delta)
            for flight in flights['flights']:
                bags_allowed = min(bags_allowed, int(flight['bags_allowed']))
                total_price += float(flight['base_price'])
                total_price += float(flight['bag_price'])*bags_count
            # add details to flights
            flights['bags_allowed'] = bags_allowed
            flights['bags_count'] = bags_count
            flights['destination'] = destination
            flights['origin'] = origin
            flights['total_price'] = total_price
            flights['travel_time'] = travel_time
        return all_flights

    def sort_by_final_price(self, all_flights):
        """Sorting by final price"""
        return sorted(all_flights, key=lambda i: i['total_price'])

    def select_where_bags_allowed(self, all_flights):
        """Filter routes based on bags allowed."""
        return list(filter(lambda flight: flight['bags_allowed'] >= int(self.bags), all_flights))

    def check_user_input(self):
        """Checks user input. 
        (Correct csv format is not checked...)
        """
        self.get_origins_and_destinations()
        self.origins_destinations_error()
        self.bag_number_error()

    def collect_all_routes(self):
        """
        Perform the serach from origin to destionation and filter based on user input.
        :return: json-compatible structured list of trips
        """
        self.get_origins_and_destinations()
        all_routes = self.get_all_possible_routes()
        selected_possible_routes = self.select_possible_routes(all_routes)
        all_flights_grouped = self.get_all_planes_with_selected_routes(
            selected_possible_routes)
        all_flights = self.get_all_flights_in_correct_format(
            all_flights_grouped)
        all_flights = self.add_flight_details(all_flights)
        all_flights = self.sort_by_final_price(all_flights)
        return json.dumps(all_flights)
