import enum
import random

line_no = 0
def read_network():
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
    edges = []
    services_read = 0 #num de lineas de services leídas
    services = []

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

    scenarios_no = random.randint(1, 30)
    scenarios = []
    for scenario in range(scenarios_no):
        scenario_edges = []
        failures = random.randint(1, min(int(len(edges)/3), 60))
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
    scenarios_no = int(input())
    scenarios = []
    for _ in range(scenarios_no - 1):
        line_no += 1
        edges_no = int(input())
        edges = [int(x) - 1 for x in input().split()]
        if edges_no != len(edges):
            raise ValueError("ERROR: Edges number mismatch")
        scenarios.append(edges)
    return scenarios

nodes, edges, services = read_network()
print("Nodes:", nodes)
print("Edges:", edges)
print("Services:", services)
scenarios = produce_scenarios(edges)
print("Scenarios:", scenarios)
print("Scenarios:")
print_scenarios(scenarios)
scenarios = read_scenarios()
print(scenarios)
