import copy
import enum
import random
import heapq


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
            #Set the list of nodes and it's channel conversion oportunities
            kind = Kind.EDGES # Move to edges
            nodes = list(int(x) for x in l.split())
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
                'path': None,
                'active': True,
                'dead': False
            }

            # Parse the service edges
            l = input()
            service["path"] = tuple(int(x) for x in l.split())
            for edge in service["path"]:
                edges[edge - 1][-1].append(services_read)

            # Add the service to the network
            services.append((service))

    return nodes, edges, services


class Network:
    def __init__(self, nodes: list, edges: list, services: list):
        """
        Initialize the network with the given nodes, edges and services.

        :param nodes: A list of nodes
        :param edges: A dictionary of edges, where the keys are the edge indices
            and the values are tuples of the connected nodes.
        :param services: A list of services, where each service is a dictionary
            with the keys 'src', 'dst', 'num_edges', 'wavelengths', 'value'
            and 'path'. The 'path' key is a list of edge indices.
        """

        for idx, node in enumerate(nodes):
            node_dict = {
                "oportunities": node,
                "adjacent": [],
            }
            nodes[idx] = node_dict
        self.nodes = dict(enumerate(nodes, 1))  # List of nodes

        for idx, edge in enumerate(edges):
            edge_dict = {
                "vertices": edge[:2],
                "services": edge[-1],
                "wavelengths": [],
                "active": True
            }
            v1, v2 = edge_dict["vertices"]

            matching_tuples = [tup for tup in self.nodes[v1]["adjacent"] if tup[0] == v2]
            if matching_tuples:
                if any(tup[1] == idx+1 for tup in matching_tuples):
                    # The vertex is in the list and the edge matches
                    pass
                else:
                    # The vertex is in the list but the edge doesn't match
                    self.nodes[v1]["adjacent"].append((v2, idx+1))
            else:
                # The vertex is not in the list
                self.nodes[v1]["adjacent"].append((v2, idx+1))

            matching_tuples = [tup for tup in self.nodes[v2]["adjacent"] if tup[0] == v1]
            if matching_tuples:
                if any(tup[1] == idx+1 for tup in matching_tuples):
                    # The vertex is in the list and the edge matches
                    pass
                else:
                    # The vertex is in the list but the edge doesn't match
                    self.nodes[v2]["adjacent"].append((v1, idx+1))
            else:
                # The vertex is not in the list
                self.nodes[v2]["adjacent"].append((v1, idx+1))

 
            edges[idx] = edge_dict
        self.edges = dict(enumerate(edges, 1))  # Adjacency list to store edges (graph representation)

        self.services = services  # List to store service details
        for service in self.services:
            for edge in service["path"]:
                wavlength_range = range(service["wavelengths"][0], service["wavelengths"][1] + 1)
                self.edges[edge]["wavelengths"].extend(wavlength_range)

    def deactivate_edge(self, idx):
        """Delete an undirected edge between nodes u and v."""
        self.edges[idx]["active"] = False
        v1, v2 = self.edges[idx]["vertices"]
        self.nodes[v1]["adjacent"] = [tup for tup in self.nodes[v1]["adjacent"] if tup[1] != idx]
        self.nodes[v2]["adjacent"] = [tup for tup in self.nodes[v2]["adjacent"] if tup[1] != idx]

    def deactivate_service(self, idx):
        """Delete an undirected edge between nodes u and v."""
        self.services[idx-1]["active"] = False

    def set_service_dead(self, idx):
        """Kill a service."""
        if not self.services[idx]["active"]:
            self.services[idx]["dead"] = True

    def failure_edge_nodes(self, service: dict):
        """If there's a failure in the service's path return the nodes of the failed edge, otherwise None"""
        for edge_idx in service['path']: # Check all the nodes edges of the path
            current_edge = self.edges[edge_idx - 1] #As the index starts in 1 -> index - 1 to start in 0
            if not current_edge['active']: #Check the edge is not active
                return current_edge['vertices'] # Return the edge's nodes
    
    def solve_scenario(self, base_network):
        print("0", flush=True)

    # def min_dist_path1(self, start_node, end_node):
    #     """
    #     Find the shortest path between two nodes in a graph using flood algorithm.
    #     Returns both node path and edge path, ensuring edges have no wavelengths.
    #     """
    #     visited = set()
    #     queue = [(start_node, [], [])]
        
    #     # Forward search to find the end node
    #     while queue:
    #         current_node, node_path, edge_path = queue.pop(0)
    #         if current_node == end_node:
    #             visited.add(current_node)
    #             break
            
    #         if current_node not in visited:
    #             visited.add(current_node)
    #             for neighbor, edge_id in self.nodes[current_node]["adjacent"]:
    #                 if neighbor not in visited and not self.edges[edge_id]["wavelengths"]:
    #                     new_node_path = node_path + [current_node]
    #                     new_edge_path = edge_path + [edge_id]
    #                     queue.append((neighbor, new_node_path, new_edge_path))
        
    #     # If end_node not found, return None
    #     if end_node not in visited:
    #         return None, None
        
    #     # Reverse search starting from end_node
    #     reverse_node_path = [end_node]
    #     reverse_edge_path = []
    #     current_node = end_node
        
    #     while current_node != start_node:
    #         for neighbor, edge_id in self.nodes[current_node]["adjacent"]:
    #             if neighbor in visited and neighbor not in reverse_node_path and not self.edges[edge_id]["wavelengths"]:
    #                 reverse_node_path.append(neighbor)
    #                 reverse_edge_path.append(edge_id)
    #                 current_node = neighbor
    #                 break
        
    #     return list(reversed(reverse_node_path)), list(reversed(reverse_edge_path))

    def min_dist_path(self, start_node, end_node, service):
        visited = set()
        queue = [(start_node, [start_node], [])]
        
        while queue:
            current_node, node_path, edge_path = queue.pop(0)
            
            if current_node == end_node:
                return node_path, edge_path
            
            for neighbor, edge_id in self.nodes[current_node]["adjacent"]:
                if neighbor not in visited and self.edges[edge_id]["active"]:
                    edge_wavelengths = set(self.edges[edge_id]["wavelengths"])
                    service_wavelengths = set(range(service["wavelengths"][0], service["wavelengths"][1] + 1))
                    
                    if not service_wavelengths.intersection(edge_wavelengths):
                        new_node_path = node_path + [neighbor]
                        new_edge_path = edge_path + [edge_id]
                        queue.append((neighbor, new_node_path, new_edge_path))
                        visited.add(neighbor)
        
        return None
    

    def redirect_broken_service(self, service):
        #print("\nRedirecting broken service", service["path"])
        start_node = service['src']
        end_node = service['dst']
        result = self.min_dist_path(start_node, end_node, service)

        if result:
            for edge in service["path"]:
                self.edges[edge]["services"].remove(service["id"])
                self.edges[edge]["wavelengths"] = list(set(self.edges[edge]["wavelengths"])-set(service["wavelengths"]))
            new_node_path, new_edge_path = result
            service['path'] = new_edge_path
            if new_edge_path:
                for edge_id in new_edge_path:
                    service_wavelengths = set(range(service["wavelengths"][0], service["wavelengths"][1] + 1))
                    self.edges[edge_id]["wavelengths"].extend(service_wavelengths)
            service['active'] = True
            service["path"] = new_edge_path
            return new_node_path, new_edge_path

        service["dead"] = True
        return None



    def dijkstra(self, start_node, end_node) -> list:
        """
        Dijkstra's algorithm to find the shortest path between two nodes in a graph.

        Args:
            start_node: The node where the path starts.
            end_node: The node where the path ends.

        Returns:
            A list of nodes representing the shortest path from start_node to end_node.
            If no path is found, it returns None, which should be an error as the graph should be connected.
        """
        distances = {node: float('inf') for node in self.nodes} #Init all nodes in a dict with infinty distance
        distances[start_node] = 0
        priority_queue = [(0, start_node)]
        # A SLinked list would be better
        predecessors = {node: None for node in self.nodes} # The value is just the next key, so you assure the path

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue) #pop the queue

            if current_node == end_node: #reached end node
                #Found end_node and create the path list
                path = []
                while current_node is not None:
                    path.append(current_node)
                    current_node = predecessors[current_node] 
                return tuple(path[::-1]) # Reversed, then it will be from start to end
            if current_distance > distances[current_node]:
                continue
            
            # Neighbors are the adjacents nodes that are connected with an active edge
            """Theretically when an edge fails and it's deleted, should be checked if the neighbour
                is still adjacent"""
            #neighbors = [node for node in self.nodes[current_node]["adjacent"]]
            for neighbor in self.nodes[current_node]["adjacent"]:
                distance = current_distance + 1 # The weight of an edge is 1
                if distance < distances[neighbor]:
                        distances[neighbor] = distance
                        predecessors[neighbor] = current_node
                        heapq.heappush(priority_queue, (distance, neighbor)) #push the queue
        return None #No path is found, which should be an error as the graph should be connected      
    
    def path_nodes_to_edges(self, path: tuple) -> tuple:
        """
        Convert a tuple of nodes path to a edge path
        """
        new_path = []
        for i in range(len(path) - 1):
            current, next = path[i], path[i+1]
            i = 0
            while edge[0] == next: # and widthwave free:
                edge =  self.nodes[current]["adjacent"][i] #index of the (v,idx_edge)
                i += 1
                if i > len(self.nodes[current]["adjacent"]): #If no edge is found then the path is incorrect
                    raise IndexError(f'There is no path between: {current} and {next}')
            new_path.append(self.edges[edge[1]]) #append the edge from the index

        return tuple(new_path)


    def solve_scenatio_hmg_beta_1(self):
        #i'll assume the algorythm is executed after a failure occurs in a node
        #self.sort_services(self.services)
        inactive_services = [service for service in self.services if not service['active']]
        for serv in inactive_services:
            edge_nodes = self.failure_edge_nodes(serv) # Get the nodes os the broken edge
            if not edge_nodes:
                print('Error: failure in the detecting failed services system the service ',serv,' should be damaged')
                continue # No failed edge found
            else:
                start_node, end_node = edge_nodes # Unpack the edges from the tuple

            new_serv = copy.deepcopy(serv)
            #As the edge is deleted find the sortest path
            new_path = self.dijkstra(start_node,end_node) # Search the shortest path between the nodes of the damaged edge
            #This path is given by nodes, then it has to be converted to edges.
            new_path = self.path_nodes_to_edges(new_path)
            new_serv['path'] = new_path


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

for _ in range(scenarios_no):
    edges = [int(x) for x in input().split()]
    scenario = copy.deepcopy(base_network)
    broken_serv = set()
    fixed_serv = set()

    while edges[0] != -1:
        for edge in edges:
            scenario.deactivate_edge(edge)
            for service in scenario.edges[edge]["services"]:
                if not scenario.services[service-1]["dead"]:
                    broken_serv.add(service)
                scenario.deactivate_service(service-1)

        for idx in list(broken_serv):
            service = scenario.services[idx-1]
            if not service["dead"]:
                redirect = scenario.redirect_broken_service(service)
                if redirect:
                    fixed_serv.add(idx)
                    broken_serv.remove(idx)
                else:
                    broken_serv.add(idx)
                    fixed_serv.discard(idx)

        print(len(fixed_serv), flush=True)

        for service in fixed_serv:
            print(service, len(scenario.services[service-1]["path"]), flush=True)
            output = []
            for edge in scenario.services[service-1]["path"]:
                start, end = scenario.services[service-1]["wavelengths"]
                output.extend([edge, start, end])
            print(*output, flush=True)

        broken_serv.clear()
        fixed_serv.clear()

        edges = [int(x) for x in input().split()]