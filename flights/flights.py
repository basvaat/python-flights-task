import itertools
from datetime import timedelta
from utils import DateHandler

class Flights:

    def __init__(self, flights_data, origin, destination):
        self.flights_data = flights_data
        self.origin = origin
        self.destination = destination
    
    def get_origins_and_destinations(self):
        # get origins and destinations
        self.destinations = set(map(lambda flight: flight['destination'], self.flights_data.values()))
        self.origins = set(map(lambda flight: flight['origin'], self.flights_data.values()))
        if self.origin not in self.origins or self.destination not in self.destinations:
            raise ValueError('Origin or destination is not correct')
        
    def drop_incorrect_routes_based_on_origins_and_destinations(self, all_routes):
        # drop routes where origins to in origins or destination not in destinations
        all_routes_filtered = []
        for route in all_routes:
            if route[0] in self.origins:
                for airport in route[1:]:
                    # inner airports are origins and destinations
                    if airport in self.origins and airport in self.destinations and route not in all_routes_filtered:
                        all_routes_filtered.append(route)
                    # check that last airport in destinations
                    if airport == route[-1] and airport in self.destinations and route not in all_routes_filtered:
                        all_routes_filtered.append(route)

        return all_routes_filtered

    
    def get_all_possible_routes(self):
        # get possible routes
        all_routes = []
        all_airports = self.origins.union(self.destinations)
        for i in range(2,len(all_airports)+1):
            all_routes.append(list(itertools.permutations(all_airports, i)))
        all_routes = list(itertools.chain.from_iterable(all_routes))

        all_routes_filtered = self.drop_incorrect_routes_based_on_origins_and_destinations(all_routes)

        return all_routes_filtered


    def select_possible_routes(self, all_routes):
        # select possible routes (with origin and destiantion)
        selected_possible_routes = []
        for route in all_routes:
            if route[0] == self.origin and route[-1] == self.destination:
                selected_possible_routes.append(route)
        return selected_possible_routes

    
    def get_all_planes_with_selected_routes(self, selected_possible_routes):
        
        # all planes with this selected routes
        groups = {} # group planes based on possible routes (a->c,a->b->c, etc.)

        for route in selected_possible_routes:
            subroutes = {} # if route:a->b->c: subroutes: a->b and b->c
            # print(route)
            
            for i in range(len(route)-1):
                # print(route[i],route[i+1])

                possible_planes =[] 
                for id in self.flights_data:
                    flight = self.flights_data[id]
                    # print(flight)

                    if flight['origin'] == route[i] and flight['destination'] == route[i+1]:
                        # print('add')
                        possible_planes.append(flight)
                    # print('')
                subroutes[(route[i], route[i+1])] = possible_planes
            groups[route] = subroutes

        return groups


    def get_all_flights_in_correct_format(self, groups):
        all_flights = []
        for routes in groups:
            # print(routes)
            # direkt flights
            if len(routes) == 2:
                subroute = list(groups[routes].keys())[0]
                assert routes == subroute
                
                for flight in groups[routes][subroute]:
                    all_flights.append({'flights':[flight]})
                    
            # here we need to combine all routes
            else: 
                all_combinations = list(itertools.product(*groups[routes].values()))
                for flight in all_combinations:
                    all_flights.append({'flights':list(flight)})

        return all_flights


    def filter_overlay_time(self, all_flights):
        all_flights_filtered_datetime = []

        for flts in range(len(all_flights)):
            flights = all_flights[flts]
            if len(flights['flights']) > 1: # not direct rout
                for flight_no in range(len(flights['flights'])-1):

                    departure_time = DateHandler.convert_datetime(flights['flights'][flight_no+1]['departure'])
                    arrival_time = DateHandler.convert_datetime(flights['flights'][flight_no]['arrival'])
                    diff = DateHandler.calculate_date_difference(departure_time, arrival_time)
            
                    if diff.total_seconds() >= 60*60 and diff.total_seconds() <= 6*60*60: # 1h <= diff <= 6h
                        all_flights_filtered_datetime.append(all_flights[flts])
                        break
            else:
                all_flights_filtered_datetime.append(all_flights[flts])

        return all_flights_filtered_datetime


    def add_flight_details(self, all_flights):
        for flights in all_flights:

            bags_allowed = 10
            bags_count = 0
            destination = None
            origin = None
            total_price = 0
            travel_time = timedelta(0)
            departure_time = None
            arrival_time = None

            last_flight = flights['flights'][-1]
            destination = last_flight['destination']
            arrival_time = DateHandler.convert_datetime(last_flight['arrival'])

            first_flight = flights['flights'][0]
            origin = first_flight['origin']
            departure_time = DateHandler.convert_datetime(first_flight['departure'])
            
            travel_time_delta = DateHandler.calculate_date_difference(departure_time, arrival_time)
            travel_time = DateHandler.convert_timedelta_to_datetime(travel_time_delta)

            for flight in flights['flights']:
                bags_allowed = min(bags_allowed, int(flight['bags_allowed']))

                total_price += float(flight['base_price'])
                total_price += float(flight['bag_price'])*bags_count

            flights['bags_allowed'] = bags_allowed
            flights['bags_count'] = bags_count
            flights['destination'] = destination
            flights['origin'] = origin
            flights['total_price'] = total_price
            flights['travel_time'] = travel_time

        return all_flights


    def sort_by_final_price(self, all_flights):
        
        return sorted(all_flights, key = lambda i: i['total_price'])

    def collect_all_routes(self):
        self.get_origins_and_destinations()
        all_routes = self.get_all_possible_routes()
        selected_possible_routes = self.select_possible_routes(all_routes)
        all_flights_grouped = self.get_all_planes_with_selected_routes(selected_possible_routes) 
        all_flights = self.get_all_flights_in_correct_format(all_flights_grouped)
        all_flights = self.filter_overlay_time(all_flights)
        all_flights = self.add_flight_details(all_flights)
        all_flights = self.sort_by_final_price(all_flights)

        return all_flights
    

