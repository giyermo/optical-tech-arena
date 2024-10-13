"""
Constans for the proyect

All range constants are made like: [i, j] and not [i, j) as range() function performs.
"""
"""
////////////////////////////////////////////////////////////////////////////////////////////
- General
////////////////////////////////////////////////////////////////////////////////////////////
"""

K = 40 # Optical wavelenghts


"""
////////////////////////////////////////////////////////////////////////////////////////////
- Input
////////////////////////////////////////////////////////////////////////////////////////////
"""
# 2 <= N <= 200
N_BOUND_LOW = 2
N_BOUND_UPP = 200
N_BOUND_RANGE = range(N_BOUND_LOW, N_BOUND_UPP + 1)

# 1 <= M <= 1000
M_BOUND_LOW = 1
M_BOUND_UPP = 1000
M_BOUND_RANGE = range(M_BOUND_LOW, M_BOUND_UPP + 1)

# Number of channel conversions opp
# 0 <= P_i <= 20
CHANNEL_CONV_OPP_LOWER_BOUND = 0
CHANNEL_CONV_OPP_UPP_BOUND = 20
CHANNEL_CONV_OPP_UPP_RANGE = range(CHANNEL_CONV_OPP_LOWER_BOUND, CHANNEL_CONV_OPP_UPP_BOUND + 1)

# The number of services initially running on the graph
# 1 <= J <= 5000

NUM_SERVICES_INIT_MIN = 1
NUM_SERVICES_INIT_MAX = 5000
NUM_SERVICES_INIT_RANGE = range(NUM_SERVICES_INIT_MIN, NUM_SERVICES_INIT_MAX + 1)

# Service value
# 0 <= V <= 100.000

SERVICE_VALUE_MIN = 0
SERVICE_VALUE_MAX = 100_000
SERVICE_VALUE_RANGE = range(SERVICE_VALUE_MIN, SERVICE_VALUE_MAX + 1)

"""
////////////////////////////////////////////////////////////////////////////////////////////
- Scenarios
////////////////////////////////////////////////////////////////////////////////////////////
"""
# Number of failure
# 0 <= T_1 <= 30
T_1_MIN = 0
T_1_MAX = 30
# Failures
# 0 <= T_1 <= 60
T_2_MIN = 0
T_2_MAX = 60

import enum
import random
import copy

class Network:
    def __init__(self, nodes, edges, services):
        self.nodes = nodes  # List of nodes
        self.edges = edges  # Adjacency list to store edges (graph representation)
        self.services = services  # List to store service details

    def delete_edge(self, idx):
        """Delete an undirected edge between nodes u and v."""
        del self.edges[idx]

    def add_service(self, src, dst, num_edges, wavelength_start, wavelength_end, value, edge_sequence):
        """Add a service to the network with the given parameters."""
        service = {
            'src': src,
            'dst': dst,
            'num_edges': num_edges,
            'wavelengths': (wavelength_start, wavelength_end),
            'value': value,
            'path': edge_sequence
        }
        self.services.append(service)

line_no = 0
def parse_network():
    class Kind(enum.Enum):
        #Como el input está dividido por partes, enum ayuda a dividirlo
        SIZE = 0
        NODES = 1
        EDGES = 2
        SERVICES_NO = 3
        SERVICES = 4
        END = 5

    global line_no # Para contar las lineas del input que se pasan
    kind = Kind.SIZE
    nodes = []
    edges_read = 0 #num de lineas de edges leídas
    edges: list[tuple] = []
    services_read = 0 #num de lineas de services leídas
    services: list[tuple] = [] #Shouldn't we use a dict for this?

    while kind != Kind.END:
        # Set the network (graph) properties during iterations
        line_no += 1 # Add a read line
        l = input()
        if kind == Kind.SIZE:
            #Set the size of the network (graph)
            kind = Kind.NODES # Move to nodes
            nodes_no, edges_no = [int(x) for x in l.split()]
        elif kind == Kind.NODES:
            #Set the list of nodes
            kind = Kind.EDGES # Move to edges
            nodes.append(tuple(int(x) for x in l.split()))
        elif kind == Kind.EDGES:
            # For each iteration, add a edge to the network (graph)
            edges_read += 1
            if edges_read == edges_no:
                kind = Kind.SERVICES_NO
            edges.append(tuple(int(x) for x in l.split()))
        elif kind == Kind.SERVICES_NO:
            #Set the number of services in the network
            kind = Kind.SERVICES
            services_no = int(l)
        elif kind == Kind.SERVICES:
            # Add a service to the network (graph)
            services_read += 1
            if services_read == services_no:
                kind = Kind.END

            # Parse the service
            service_tuple = tuple(int(x) for x in l.split())
            service = {
                'src': service_tuple[0],
                'dst': service_tuple[1],
                'num_edges': service_tuple[2],
                'wavelengths': (service_tuple[3], service_tuple[4]),
                'value': service_tuple[5],
                'path': None
            }

            # Parse the service edges
            line_no += 1 # Add a read line(he añadido esto, que antes no estaba, para q no cuente menos líneas)
            l = input()
            service["path"] = tuple(int(x) for x in l.split())

            # Add the service to the network
            services.append((service))

    return nodes, edges, services


def produce_scenarios(edges):
    """Produce failure scenarios

    Naive version, with random failures"""

    scenarios_no = 1# random.randint(1, T_1_MAX)
    scenarios = []
    for scenario in range(scenarios_no):
        scenario_edges = []
        failures = 1#random.randint(1, min(int(len(edges)/3), T_2_MAX))
        for _ in range(failures):
            edge = random.randint(0, len(edges) - 1)
            if edge not in scenario_edges:
                scenario_edges.append(edge)
        if scenario_edges not in scenarios:
            scenarios.append(scenario_edges)
    return scenarios

def print_scenarios(scenarios):
    print(len(scenarios), flush=True)
    for scenario in scenarios:
        print(len(scenario), flush=True)
        # Edges should be counted from 1
        print(*[edge + 1 for edge in scenario], flush=True)

def read_scenario(base_network, edges):
    global line_no

    scenario = copy.deepcopy(base_network)
    
    line_no += 1

    # if edges != len(edges):
    #     raise ValueError("ERROR: Edges number mismatch")
    
    for edge in edges: 
        scenario.delete_edge(edge)

    return scenario


def solve_scenario(scenario, base_network):
    print("0", flush=True)

# Parse the network
nodes, edges, services = parse_network()
base_network = Network(nodes, edges, services)


scenarios = produce_scenarios(edges)
print_scenarios(scenarios)

scenarios_no = int(input()) # Input number scenarios:
line_no += 1
for _ in range(scenarios_no - 1):
    edges = [int(x) - 1 for x in input().split()]
    print(line_no)
    print("edges", edges)
    if edges[0] == -2: break
    while edges[0] != -1:
        scenario = read_scenario(base_network, edges)
        solve_scenario(scenario, base_network)
        edges = [int(x) - 1 for x in input().split()]

print("finished")
