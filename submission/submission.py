import copy
import enum
import random


class Network:
    def __init__(self, nodes: list, edges: dict, services: list):
        """
        Initialize the network with the given nodes, edges and services.

        :param nodes: A list of nodes
        :param edges: A dictionary of edges, where the keys are the edge indices
            and the values are tuples of the connected nodes.
        :param services: A list of services, where each service is a dictionary
            with the keys 'src', 'dst', 'num_edges', 'wavelengths', 'value'
            and 'path'. The 'path' key is a list of edge indices.
        """
        self.nodes = nodes  # List of nodes
        self.edges = dict(enumerate(edges))  # Adjacency list to store edges (graph representation)
        self.services = services  # List to store service details

    def delete_edge(self, idx):
        """Delete an undirected edge between nodes u and v."""
        del self.edges[idx]


    def solve_scenario(self, base_network):
        print("0", flush=True)

def parse_network():
    """
    Parse the input data for the graph and services.

    It reads the input data from the standard input, parses it and returns the graph and services as a tuple.

    The input data is divided into four parts: The size of the graph, the nodes, the edges and the services.
    The size of the graph contains the number of nodes and edges.
    The nodes are given as a list of channel conversion opportunities.
    The edges are given as a list of pairs of nodes.
    The services are given as a list of tuples, containing the source, destination, number of edges, wavelength start, wavelength end and value of the service.
    The path of each service is given as a list of edges.

    Returns:
        tuple: A tuple containing the nodes, edges and services of the graph.
    """

    class Kind(enum.Enum):
        #Como el input está dividido por partes, enum ayuda a dividirlo
        SIZE = 0
        NODES = 1
        EDGES = 2
        SERVICES_NO = 3
        SERVICES = 4
        END = 5

    kind = Kind.SIZE
    nodes = []
    edges_read = 0 #num de lineas de edges leídas
    edges: list[list] = []
    services_read = 0 #num de lineas de services leídas
    services: list[tuple] = []

    while kind != Kind.END:
        # Set the network (graph) properties during iterations
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
            edge = list(int(x) for x in l.split())
            edge.append([])
            edges.append(edge)
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
                'id': services_read,
                'src': service_tuple[0],
                'dst': service_tuple[1],
                'num_edges': service_tuple[2],
                'wavelengths': (service_tuple[3], service_tuple[4]),
                'value': service_tuple[5],
                'path': None
            }

            # Parse the service edges
            l = input()
            service["path"] = tuple(int(x) for x in l.split())
            for edge in service["path"]:
                edges[edge - 1][-1].append(services_read)

            # Add the service to the network
            services.append((service))

    return nodes, edges, services

def produce_scenarios(edges):
    """
    Produce failure scenarios

    Naive version, with random failures

    Parameters
    ----------
    edges : list
        List of edges of the graph

    Returns
    -------
    list
        List of lists of edges that fail in each scenario
    """
    scenarios_no = 1# random.randint(1, T_1_MAX)
    scenarios = []
    for scenario in range(scenarios_no):
        scenario_edges = []
        failures = 1#random.randint(1, min(int(len(edges)/3), T_2_MAX))
        for _ in range(failures):
            edge = random.randint(0, len(edges)-1)
            if edge not in scenario_edges:
                scenario_edges.append(edge)
        if scenario_edges not in scenarios:
            scenarios.append(scenario_edges)
    return scenarios

def print_scenarios(scenarios:list):
    """
    Print failure scenarios to the standard output

    The first line contains the number of failure scenarios.
    The following lines describe each scenario, with the first number being
    the number of edges that fail, and the following numbers the indices of
    the edges that fail, counted from 1.
    """
    print(len(scenarios), flush=True)
    for scenario in scenarios:
        print(len(scenario), flush=True)
        # Edges should be counted from 1
        print(*[edge + 1 for edge in scenario], flush=True)

# Parse the network
nodes, edges, services = parse_network()
base_network = Network(nodes, edges, services)

scenarios = produce_scenarios(edges)
print_scenarios(scenarios)

scenarios_no = int(input()) # Number of scenarios provided by the environment

for _ in range(scenarios_no): # For each scenario
    
    edges = [int(x) - 1 for x in input().split()] #parse edges that fail
    scenario = copy.deepcopy(base_network) # copy base network

    while edges[0] != -2:
        for edge in edges: # Delete edges that fail
            scenario.delete_edge(edge)

        scenario.solve_scenario(base_network)
        
        edges = [int(x) - 1 for x in input().split()] # set next batch of edges