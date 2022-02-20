# Python weekend entry task

**Kiwi Python Weekend Entry Task**

### Usage

To run
```
python -m solution example0.csv RFZ WIW --bags=1
```
- It performs a search RFZ -> WIW for flights which allow at least 1 piece of baggage
- Example files are stored in example folder. 
You only have to provide the name of the csv file (if it is in example folder as sample files)
- There is `bags` feature
- There is no `return` feature.
- First 3 input arguments are strings, `bags` is int
- Output is json-compatible structured list of trips sorted by price (as print not as file)
- Only standard library and built-in data structures are used.

**NOTE:** There are lots of `for` loops, and it can be slow for larger inputs...

### How it works
 
- stores the data from csv file in dictionary
- collect all the possible routes from origin to destination (not only direct routes)
- search for possible routes in flights data
- groups the routes based on different routes
   - Origin -> B -> C -> Destination
   groups (3): Origin->B, B->C, C->Destination
- collects all flights in groups
- combine all flights in a route to get a full list of routes
- filter these routes based on overlay time (1h <= time <= 6h)
- file details added: 
    - `bags_allowed`
    - `bags_count`
    - `destination`
    - `origin`
    - `total_price`
    - `travel_time`



#### Output
The output is a json-compatible structured list of trips sorted by price. The trip has the following schema:
| Field          | Description                                                   |
|----------------|---------------------------------------------------------------|
| `flights`      | A list of flights in the trip according to the input dataset. |
| `origin`       | Origin airport of the trip.                                   |
| `destination`  | The final destination of the trip.                            |
| `bags_allowed` | The number of allowed bags for the trip.                      |
| `bags_count`   | The searched number of bags.                                  |
| `total_price`  | The total price for the trip.                                 |
| `travel_time`  | The total travel time.                                        |


