# Z3 Rideshare Planner

## Introduction

This Python package provides a planner that takes in the names and addresses of multiple passengers and drivers, and the address of a destination, and gives a plan which minimizes the time for pickup process.

This package utilizes [[https://www.microsoft.com/en-us/research/project/z3-3/|Microsoft Z3 Solver]] and [[https://developers.google.com/maps|Google Map API]].

## Google Map API Key

To use this package, you need to have a Google Map API Key. You can get one for free at https://console.cloud.google.com/google/maps-apis/credentials. 

## Dependencies

- googlemaps
- matplotlib
- datetime
- folium
- z3-solver
- polyline
- numpy

## Usage

### Class: ```Planner```

- ```Planner.__init__(self, API_KEY)```
Takes in a Google API Key, returns a ```Planner``` instance.

- ```Planner.configure(self, passenger_name_addr, driver_name_addr, destination, n_seats, must_together=[])```
Takes in requirements and conditions.

    - ```passenger_name_addr```: List of 2-tuples, where the first element is the passenger name, and the second element is their address
    - ```driver_name_addr```: List of 2-tuples, where the first element is the driver name, and the second element is their address
    - ```destination```: The final destination that everyone goes to
    - ```n_seats```: Specifies the capacity (driver included) of each car. If the input is an ```int```, then it's for all drivers; If the input is a list of ```int```, then the list elements each represents the capacity of one car, according to the order of ``driver_name_addr```
    - ```must_together```: List of lists, where each element list contains a group of passengers and (at most one) driver that must be in the same car

- ```Planner.solve(self)```
If a plan is found, prints "Plan found!". Otherwise, raises ValueError.

- ```Planner.print_plan(self)```
If a plan has been found, print the plan in the string format.

- ```visualize(self, output_mode='html', relative_path=None, colormap='Set1')```
If a plan has been found, visualize it with interactive features.

    - ```output_mode```: If ```output_mode='html'```, save the visualization as an html file at ```relative_path```; If ```output_mode='display'```, returns a ```folium.Figure``` object
    - ```colormap```: A ```str``` key of ```matplotlib.colormaps```, serves as the color scheme of the markers on the map