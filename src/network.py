import enum
import random
from constants import *

class Network:
    def __init__(self, nodes, edges, services):
        self.nodes = nodes  # List of nodes
        self.edges = edges  # Adjacency list to store edges (graph representation)
        self.services = services  # List to store service details

    def add_edge(self, u, v):
        """Add an undirected edge between nodes u and v."""
        if u not in self.edges:
            self.edges[u] = []
        if v not in self.edges:
            self.edges[v] = []
        self.edges[u].append(v)
        self.edges[v].append(u)

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
        print(l)
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
            if services_read == services_no:
                kind = Kind.END
            services_read += 1
            service = tuple(int(x) for x in l.split())
            line_no += 1 # Add a read line(he añadido esto, que antes no estaba, para q no cuente menos líneas)
            l = input()
            service_edges = tuple(int(x) for x in l.split())
            services.append((service, service_edges))
    return nodes, edges, services


def produce_scenarios(edges):
    """Produce failure scenarios

    Naive version, with random failures"""

    scenarios_no = random.randint(1, T_1_MAX)
    scenarios = []
    for scenario in range(scenarios_no):
        scenario_edges = []
        failures = random.randint(1, min(int(len(edges)/3), T_2_MAX))
        for _ in range(failures):
            edge = random.randint(0, len(edges) - 1)
            if edge not in scenario_edges:
                scenario_edges.append(edge)
        if scenario_edges not in scenarios:
            scenarios.append(scenario_edges)
    return scenarios

def print_scenarios(scenarios):
    print(len(scenarios))
    for scenario in scenarios:
        print(len(scenario))
        # Edges should be counted from 1
        print(*[edge + 1 for edge in scenario])

def read_scenarios():
    global line_no
    scenarios_no = int(input()) # Input number scenarios:
    scenarios = []
    for _ in range(scenarios_no - 1):
        line_no += 1
        edges_no = int(input())
        edges = [int(x) - 1 for x in input().split()]
        if edges_no != len(edges):
            raise ValueError("ERROR: Edges number mismatch")
        scenarios.append(edges)
    return scenarios



nodes, edges, services = parse_network()
base_network = Network(nodes, edges, services)
print("Nodes:", base_network.nodes)
print("Edges:", base_network.edges)
print("Services:", base_network.services)
scenarios = produce_scenarios(edges)
print("Scenarios:")
print_scenarios(scenarios)
print("-------------------")
scenarios = read_scenarios()
print(scenarios)
