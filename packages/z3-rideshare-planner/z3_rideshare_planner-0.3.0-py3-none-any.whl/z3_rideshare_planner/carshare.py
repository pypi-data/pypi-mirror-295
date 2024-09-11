import googlemaps
from z3 import *
from datetime import datetime
import folium
import polyline as pl
import numpy as np
import matplotlib.pyplot as plt


# Main #

def setup(passenger_name_addr, driver_name_addr, destination_, API_KEY, must_together=[]):
    global KEY, passengers, drivers, destination, n_p, n_d, passenger_groups
    global passenger_driver_bindings, distances, people, t_list, T_list, N_list, gmaps_client
    
    #Initialization
    KEY = API_KEY
    passengers = passenger_name_addr
    drivers = driver_name_addr
    destination = destination_
    n_p = len(passengers)
    n_d = len(drivers)
    passenger_addresses = [p[1] for p in passengers]
    driver_addresses = [d[1] for d in drivers]
    distances = construct_distance_matrix(passenger_addresses + driver_addresses + [destination], KEY)
    people = {p[0]: p[1] for p in passengers + drivers}

    # Variable declaration
    t_list = [Bool('t_%s' % i) for i in range(n_d * (n_p + 1) ** 2)]
    T_list = [Int('T_%s' % i) for i in range(n_d * (n_p + 1))]
    N_list = [Int('N_%s' % i) for i in range(n_d * (n_p + 1))]

    # encode must_together conditions
    driver_list, passenger_list = [d[0] for d in drivers], [p[0] for p in passengers]
    passenger_groups = []
    passenger_driver_bindings = {}
    for group in must_together:
        drivers_in_group = list(filter(lambda x: x in driver_list, group))
        assert len(drivers_in_group) < 2, 'Cannot have more than one driver in a group'
        if len(drivers_in_group) == 1:
            driver = drivers_in_group[0]
            group.remove(driver)
            assert len(group) > 0, 'Group must have at least one passenger'
            passenger_driver_bindings[passenger_list.index(group[0])] = driver_list.index(driver)
        passenger_groups.append([passenger_list.index(p) for p in group])
        
    return
    
def encode_must_together(must_together, driver_list, passenger_list):
    passenger_groups = []
    passenger_driver_bindings = {}
    for group in must_together:
        drivers_in_group = list(filter(lambda x: x in driver_list, group))
        assert len(drivers_in_group) < 2, 'Cannot have more than one driver in a group'
        if len(drivers_in_group) == 1:
            driver = drivers_in_group[0]
            group.remove(driver)
            assert len(group) > 0, 'Group must have at least one passenger'
            passenger_driver_bindings[passenger_list.index(group[0])] = driver_list.index(driver)
        passenger_groups.append([passenger_list.index(p) for p in group])
    return passenger_groups, passenger_driver_bindings

#---------------------#

# Distance Matrix functions #

# Google Map distanceMatrix API can support up to 11 addresses at one time
def get_distance_matrix(origins, destinations, API_KEY):
    gmaps_client = googlemaps.Client(key=API_KEY)

    distances = {}
    for origin in origins:
        for destination in destinations:
            distances[(origin, destination)] = None

    rows = gmaps_client.distance_matrix(origins, destinations)['rows']
    row_idx = 0
    for row in rows:
        elements = row['elements']
        col_idx = 0
        for element in elements:
            if element['status'] == 'OK':
                distances[(origins[row_idx], destinations[col_idx])] = element['duration']['value']
            else:
                print(f'DISTANCE NOT FOUND: {origins[row_idx]} - {destinations[col_idx]}')
            col_idx += 1
        row_idx += 1
    return distances

def split_addresses(addrs, maxlen=10):
    l = len(addrs)
    if l <= maxlen:
        return [addrs]
    n = l // maxlen
    output = []
    for i in range(n):
        output.append(addrs[i * maxlen: (i+1) * maxlen])
    output.append(addrs[n * maxlen:])
    return output

def construct_distance_matrix(addrs, API_KEY, maxlen=10):
    addrs_splitted = split_addresses(addrs, maxlen)
    out = {}
    for sublist1 in addrs_splitted:
        for sublist2 in addrs_splitted:
            out.update(get_distance_matrix(sublist1, sublist2, API_KEY))
    return out

#---------------------#

# Z3 functions #

# Map to variable
def t(i, j, k):
    if not (i >= 0 and i < n_d and j >= -1 and j <= n_p and k >= 0 and k <= n_p):
        print(f'Error: Index t({i}, {j}, {k}) not valid')
        return
    return (t_list[i * (n_p + 1) ** 2 + j * (n_p + 1) + k] if j != -1 else t(i, n_p, k))

def T(i, j):
    if not (i >= 0 and i < n_d and j >= 0 and j <= n_p):
        print(f'Error: Index T({i}, {j}) not valid')
        return
    return T_list[i * n_d + j]

def N(i, j):
    if not (i >= 0 and i < n_d and j >= 0 and j <= n_p):
        print(f'Error: Index N({i}, {j}) not valid')
        return
    return N_list[i * n_d + j]

#---------------------#

# Proposition Construction #

def drives(driver, passenger):
    if passenger == -1:
        return Bool(True)
    return Or(*tuple(
        [t(driver, prevPassenger, passenger) for prevPassenger in range(-1, n_p) if prevPassenger != passenger]
        ))


def T_update(driver, prevPassenger, passenger):
    if prevPassenger == -1:
        if passenger == n_p:
            d = distances[(people[drivers[driver][0]], destination)]
        else:
            d = distances[(people[drivers[driver][0]], people[passengers[passenger][0]])]
        return T(driver, passenger) == d
    else:
        if passenger == n_p:
            d = distances[(people[passengers[prevPassenger][0]], destination)]
        else:
            d = distances[(people[passengers[prevPassenger][0]], people[passengers[passenger][0]])]
        return T(driver, passenger) == T(driver, prevPassenger) + d
    
    
def N_update(driver, prevPassenger, passenger):
    if passenger == n_p and prevPassenger == -1:
        return N(driver, passenger) == 1
    if prevPassenger == -1:
        return N(driver, passenger) == 2
    if passenger == n_p:
        return N(driver, passenger) == N(driver, prevPassenger)
    return N(driver, passenger) == N(driver, prevPassenger) + 1


def D(driver, prevPassenger, passenger):
    conjunctive_list = []
    conjunctive_list.append(t(driver, prevPassenger, passenger))

    for alt_d in range(n_d):
        for alt_p in range(-1, n_p):
            if alt_p != prevPassenger or alt_d != driver:
                conjunctive_list.append(Not(t(alt_d, alt_p, passenger)))
        for alt_p in range(0, n_p + 1):
            if prevPassenger != -1 and (alt_p != passenger or alt_d != driver):
                conjunctive_list.append(Not(t(alt_d, prevPassenger, alt_p)))
            elif prevPassenger == -1 and alt_d == driver and alt_p != passenger:
                conjunctive_list.append(Not(t(alt_d, prevPassenger, alt_p)))
    
    conjunctive_list.append(drives(driver, prevPassenger))
    
    conjunctive_list = list(set(conjunctive_list))
    
    return And(*tuple(conjunctive_list), T_update(driver, prevPassenger, passenger), N_update(driver, prevPassenger, passenger))


def driverGuarantee(driver, seats):
    disjunctive_list = [
        And(
            t(driver, prevPassenger, n_p),
            *tuple(
                [Not(t(driver, alt_p, n_p)) for alt_p in range(-1, n_p) if alt_p != prevPassenger]
            ),
            drives(driver, prevPassenger),
            T_update(driver, prevPassenger, n_p),
            N_update(driver, prevPassenger, n_p)
        )
        for prevPassenger in range(-1, n_p)
    ]
    disjunctive_list = list(set(disjunctive_list))
    return And(Or(*tuple(disjunctive_list)), N(driver, n_p) <= seats)

    
def cost_limit(cost):
    return And(
        *tuple(
            [(T(driver, n_p) < cost) for driver in range(n_d)]
        )
    )


def passengerGuarantee(passenger, driver=None):
    disjunctives = []

    if driver is not None:
        for prevPassenger in range(-1, n_p):
            if prevPassenger != passenger:
                disjunctives.append(D(driver, prevPassenger, passenger))
    
    for driver in range(n_d):
        for prevPassenger in range(-1, n_p):
            if prevPassenger != passenger:
                disjunctives.append(D(driver, prevPassenger, passenger))

    return Or(*tuple(disjunctives))

def passenger_binding(passengers):
    def pair_binding(p1, p2):
        return Or(
            *tuple([And(drives(driver, p1), drives(driver, p2))
            for driver in range(n_d)])
        )
    passengers_copy = passengers[1:]
    passengers = passengers[:-1]
    return And(*tuple([pair_binding(p1, p2) for p1, p2 in zip(passengers, passengers_copy)]))

    
#---------------------#
    
# Find and parse optimal solution #

def search_opt(n_seats):
    def generate_plan(cost, n_seats, ignore_cost=False):
        s = Solver()

        if isinstance(n_seats, int) or isinstance(n_seats, float):
            if n_seats * n_d < n_d + n_p:
                print('Error: Seats insufficient')
                return (False, None)
            for driver in range(n_d):
                s.add(driverGuarantee(driver, n_seats))
        elif (isinstance(n_seats, tuple) or isinstance(n_seats, list)) and len(n_seats) == n_d:
            if sum(n_seats) * n_d < n_d + n_p:
                print('Error: Seats insufficient')
                return (False, None)
            for driver, n in enumerate(n_seats):
                s.add(driverGuarantee(driver, n))
        else:
            print('Error: n_seats format wrong')
            return (False, None)
            
        for passenger in range(n_p):
            if passenger in passenger_driver_bindings:
                s.add(passengerGuarantee(passenger, passenger_driver_bindings[passenger]))
            else:
                s.add(passengerGuarantee(passenger))
        
        for group in passenger_groups:
            s.add(passenger_binding(group))
            
        if s.check() == sat:
            if ignore_cost:
                # print('SUCCESS: Found one plan ignoring the cost')
                return (True, s.model())
        else:
            print('Not Satisfied')
            return (False, None)
        s.add(cost_limit(cost))
        if s.check() == sat:
            # print('SUCCESS')
            return (True, s.model())
        else:
            # print('No plan under the cost')
            return (False, None)
        
    attempt = generate_plan(0, n_seats, True)
    if attempt[0]:
        model = attempt[1]
        time = max([model.eval(T(i, n_p)).as_long() for i in range(n_d)])
    else:
        raise ValueError('Error: No plan found')
    while time > 0:
        attempt = generate_plan(time - 1, n_seats)
        if not attempt[0]:
            break
        model = attempt[1]
        time = max([model.eval(T(i, n_p)).as_long() for i in range(n_d)])
    return model

def reverse_t(i):
    driver = i // ((n_p + 1) ** 2)
    i = i % ((n_p + 1) ** 2)
    prevPassenger = i // (n_p + 1)
    i = i % (n_p + 1)
    if prevPassenger == n_p:
        prevPassenger = -1
    return (driver, prevPassenger, i)

def reverse_T(T_val):
    return (T_val % n_d, T_val // n_d)

def parse_plan(model):
    def backtrace(driver, passenger):
        if passenger == -1:
            return []
        prev = next(filter(lambda e: e[0] == driver and e[2] == passenger, edges))[1]
        return backtrace(driver, prev) + [passenger]

    t_indices = [i for i in range(len(t_list)) if is_true(model.eval(t_list[i]))]
    max_time = max([model.eval(T(i, n_p)).as_long() for i in range(n_d)])
    
    edges = [reverse_t(i) for i in t_indices]
    paths = [backtrace(driver, n_p) for driver in range(n_d)]
    return (paths, max_time)

def print_plan(paths, max_time):
    output = ''
    for d in range(len(paths)):
        s = f"{drivers[d][0]}: {drivers[d][0]}"
        for passenger in paths[d]:
            if passenger != n_p:
                s += f" -> {passengers[passenger][0]}"
            else:
                s += f' -> destination'
        output += s + '\n'
    output += f'Time bound: {max_time}'
    return output

#---------------------#

# Visualization functions #

def draw_plan(paths, gmaps_client, colormap='Set1', output_mode='display'):
    def draw_path(map, path, driver, color):
        def draw_section(start, end):
            polyline = gmaps_client.directions(start, end, mode="driving", departure_time=datetime.now())[0]['overview_polyline']['points']
            points = pl.decode(polyline)
            folium.PolyLine(points, color= f"#{color[0]:02x}{color[1]:02x}{color[2]:02x}", weight=4, opacity=1).add_to(map)
            return
        
        driver_location = get_lat_lon(drivers[driver][1])
        if len(path) == 0:
            end = get_lat_lon(destination)
            draw_section(driver_location, end)
            add_marker(map, driver_location, 0, drivers[driver][0] + ' (driver)', color)
            return
        draw_section(driver_location, get_lat_lon(people[passengers[path[0]][0]]))
        add_marker(map, driver_location, 0, drivers[driver][0] + ' (driver)', color)
        for i in range(len(path)):
            start = get_lat_lon(people[passengers[path[i]][0]])
            if i == len(path) - 1:
                end = get_lat_lon(destination)
            else:
                end = get_lat_lon(people[passengers[path[i+1]][0]])
            draw_section(start, end)
            add_marker(map, start, i + 1, passengers[path[i]][0], color)

        return

    def add_marker(map, location, index, label, color):
        icon_html = lambda d: f'''
            <div style="background-color: rgb({color[0]},{color[1]},{color[2]}); border-radius: 50%; 
                width: 30px; height: 30px; text-align: center; line-height: 30px; 
                color: {'gray' if index == 0 else 'white'}; font-size: 14pt;">
                {d}
            </div>
        '''
        folium.Marker(location=location,
                popup=folium.Popup(label, max_width=70),
                icon=folium.DivIcon(html=icon_html(index))).add_to(map)
        return
    
    def get_lat_lon(address):
        result = gmaps_client.geocode(address)
        if len(result) == 0:
            print(f'Error: Address {address} not found')
            return
        loc = result[0]['geometry']['location']
        return (loc['lat'], loc['lng'])

    # Initialize the map
    passenger_addresses = [p[1] for p in passengers]
    driver_addresses = [d[1] for d in drivers]
    all_addrs = passenger_addresses + driver_addresses + [destination]
    all_addrs = np.array([get_lat_lon(addr) for addr in all_addrs])
    southwest, northeast =  all_addrs.min(axis=0), all_addrs.max(axis=0)
    difference  = northeast - southwest
    southwest -= difference * 0.2
    northeast += difference * 0.2
    bounds = [southwest.tolist(), northeast.tolist()]
    figure = folium.Figure(width=1000, height=500)
    if output_mode == 'display':
        map = folium.Map(location=all_addrs.mean(axis=0), zoom_start=12, min_zoom = 11, max_bounds=True,
                         min_lat=bounds[0][0], max_lat=bounds[1][0], min_lon=bounds[0][1], 
                         max_lon=bounds[1][1]).add_to(figure)
    else:
        map = folium.Map(location=all_addrs.mean(axis=0), tiles='Stadia.OSMBright', zoom_start=12, min_zoom = 11, max_bounds=True,
                        min_lat=bounds[0][0], max_lat=bounds[1][0], min_lon=bounds[0][1], 
                        max_lon=bounds[1][1]).add_to(figure)
    
    paths = [path[:-1] for path in paths] # Remove destination from all paths

    # Figure the colors
    colors = list(plt.colormaps[colormap].colors)
    colors = [tuple(int(255 * c) for c in color) for color in colors]
    if len(paths) + 1 > len(colors):
        colors += [tuple(np.random.randint(0, 256, 3)) for _ in range(len(paths) + 1 - len(colors))]
    else:
        colors = colors[:len(paths) + 1]

    for i in range(len(paths)):
        draw_path(map, paths[i], i, colors[i]) # Draw path for driver i
    add_marker(map, get_lat_lon(destination), 'D', destination, colors[-1])
    return figure



