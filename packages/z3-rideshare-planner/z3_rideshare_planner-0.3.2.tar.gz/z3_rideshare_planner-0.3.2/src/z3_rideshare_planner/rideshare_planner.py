import carshare
import googlemaps

class Planner:
    def __init__(self, API_KEY):
        """
        Initializes a Planner instance.

        Parameters:
        - API_KEY (str): The Google API Key used for accessing the Google Maps API.
        """
        self.gmaps_client = googlemaps.Client(key=API_KEY)
        self.API_KEY = API_KEY
        self.plan = None

    def configure(self, passenger_name_addr, driver_name_addr, destination, n_seats, must_together=[]):
        """
        Configures the rideshare planner with the given requirements and conditions.

        Args:
            passenger_name_addr (list): List of 2-tuples, where the first element is the passenger name, and the second element is their address.
            driver_name_addr (list): List of 2-tuples, where the first element is the driver name, and the second element is their address.
            destination (str): The final destination that everyone goes to.
            n_seats (int or list): Specifies the capacity (driver included) of each car. If the input is an int, then it's for all drivers; If the input is a list of ints, then the list elements each represent the capacity of one car, according to the order of driver_name_addr.
            must_together (list, optional): List of lists, where each element list contains a group of passengers and (at most one) driver that must be in the same car. Defaults to an empty list.
        """
        carshare.setup(passenger_name_addr, driver_name_addr, destination, self.API_KEY, must_together=must_together)
        self.destination = destination
        self.n_seats = n_seats

    def solve(self):
        """
        Solves the rideshare planning problem.

        If a plan is found, prints "Plan found!". Otherwise, raises ValueError.

        Returns:
            If a plan is found, it sets the `plan` attribute of the object to the ride plan.
            If no plan is found, it raises a ValueError.

        Raises:
            ValueError: If no plan is found.
        """
        try:
            model = carshare.search_opt(self.n_seats)
        except ValueError as e:
            return e
        paths, max_time = carshare.parse_plan(model)
        # return RidesharePlanner.RidePlan(paths, max_time, self.passenger_df, self.driver_df, self.destination, self.API_KEY)
        self.plan = self._RidePlan(paths, max_time, self.API_KEY)
        print('Plan found!')

    def print_plan(self):
        """
        Print the plan in string format if a plan has been found.
        """
        if self.plan == None:
            print('Error: No plan found')
            return
        print(self.plan)

    def visualize_plan(self, output_mode='display', relative_path=None, colormap='Set1'):
        """
        Visualizes the plan with interactive features.

        Args:
            output_mode (str, optional): The output mode for visualization. 
                If 'html', the visualization is saved as an html file at `relative_path`. 
                If 'display', it returns a `folium.Figure` object. 
                Defaults to 'display'.
            relative_path (str, optional): The relative path to save the visualization as an html file. 
                Required if `output_mode` is 'html'. Defaults to None.
            colormap (str, optional): The color scheme of the markers on the map. 
                A string key of `matplotlib.colormaps`. Defaults to 'Set1'.

        Raises:
            ValueError: If no plan is found.

        Returns:
            None: If `output_mode` is 'display'.
            str: The path to the saved html file, if `output_mode` is 'html'.
        """
        if self.plan is None:
            raise ValueError('Error: No plan found')
        return self.plan.visualize(output_mode=output_mode, relative_path=relative_path, colormap=colormap)


    class _RidePlan:
        def __init__(self, paths, time_bound, KEY):
            self.paths = paths
            self.time_bound = time_bound
            self.KEY = KEY
        
        def __str__(self):
            return carshare.print_plan(self.paths, self.time_bound)

        def visualize(self, output_mode='html', relative_path=None, colormap='Set1'):
            # if output_mode == 'html': store the output as html file, relative_path required
            # if output_mode == 'display': return the Folium figure object
            if output_mode == 'html' and relative_path is None:
                raise ValueError('relative_path must be provided when output_mode is html')
            figure = carshare.draw_plan(self.paths, googlemaps.Client(key=self.KEY), colormap=colormap, output_mode=output_mode)
            if output_mode == 'html':
                figure.save(relative_path)
                return 
            elif output_mode == 'display':
                return figure
            else:
                raise ValueError("output_mode should be either 'html' or 'display'." )

