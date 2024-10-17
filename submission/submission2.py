class Edge:
    def __init__(self, id, node1, node2):
        self.id = id  # Edge identifier
        self.nodes = (node1, node2)  # Tuple of nodes that this edge connects
        self.services = {}  # Dictionary of services {service_id: (start_wavelength, end_wavelength)}
        self.active = True  # Edge active status, initially set to active

    def add_service(self, service_id, wavelength_range):
        """Add a service to the edge with the specified wavelength range."""
        start, end = wavelength_range

        # Validate the range to ensure it falls between 1 and 40
        if 1 <= start <= 40 and 1 <= end <= 40 and start <= end:
            self.services[service_id] = (start, end)
        else:
            raise ValueError("Wavelength range must be between 1 and 40.")

    def remove_service(self, service_id):
        """Remove a service from the edge."""
        if service_id in self.services:
            del self.services[service_id]

    def deactivate(self):
        """Deactivate the edge. Once deactivated, it cannot be activated again."""
        if self.active:  # Only deactivate if it is currently active
            self.active = False
        # Return the list of services that were associated with this edge
        associated_services = list(self.services.keys())
        return associated_services

    def has_available_wavelengths(self, start, end):
        """Check if there are available wavelengths in the edge for the given range."""
        # Check for overlap with existing services
        for existing_service_id, (existing_start, existing_end) in self.services.items():
            # Check for overlap
            if (start <= existing_end and end >= existing_start):
                return False  # There is a collision in wavelength ranges
        return True  # No collisions found, wavelengths are available

    def __repr__(self):
        return (f"Edge(id={self.id}, nodes={self.nodes}, "
                f"services={self.services}, active={self.active})")


class Node:
    def __init__(self, id, opportunities):
        self.id = id  # Node identifier
        self.opps = opportunities  # Number of conversion opportunities
        self.adj = {}  # Dictionary for adjacent nodes and lists of edge IDs

    def add_adj(self, node, edge_id):
        # Add an edge ID to the list for the given adjacent node ID
        if node.id in self.adj:
            self.adj[node.id].append(edge_id)  # Append to the existing list of edge IDs
        else:
            self.adj[node.id] = [edge_id]  # Create a new list if this is the first edge

    def remove_adj(self, node, edge_id):
        # Remove the specified edge ID to the adjacent node ID
        if node.id in self.adj:
            if edge_id in self.adj[node.id]:
                self.adj[node.id].remove(edge_id)  # Remove the specific edge ID
                if not self.adj[node.id]:  # If no more edges remain, remove the entry
                    del self.adj[node.id]

    def get_adj(self):
        # Return the list of adjacent node IDs
        return list(self.adj.keys())

    def get_edges(self, node):
        # Return the list of edge IDs to a specific adjacent node ID
        return self.adj.get(node.id, [])

    def __repr__(self):
        # Return a string representation of the node
        return (f"Node(id={self.id}, "
                f"opps={self.opps}, "
                f"adj={self.adj})")

class Service:
    def __init__(self, id, src, dst):
        self.id = id  # Unique identifier for the service
        self.src = src  # Source node
        self.dst = dst  # Destination node
        self.path = []  # List of edge IDs in the service path
        self.wavelengths = []  # List of tuples (start, end) for each edge in the path
        self.active = True  # Indicates if the service is active
        self.dead = False  # Indicates if the service is marked as dead
        self.value = 10000  # Value attribute with upper limit

    def add_edge(self, edge_id, wavelength_range):
        """Add an edge ID and its corresponding wavelength range to the service."""
        self.path.append(edge_id)  # Add the edge ID to the path
        self.wavelengths.append(wavelength_range)  # Add the wavelength range

    def deactivate(self):
        """Deactivate the service."""
        self.active = False

    def mark_as_dead(self):
        """Mark the service as dead."""
        self.dead = True

    def __repr__(self):
        return (f"Service(id={self.id}, src={self.src}, dst={self.dst}, "
                f"path={self.path}, wavelengths={self.wavelengths}, "
                f"active={self.active}, dead={self.dead}, value={self.value})")

from collections import deque

class Network:
    def __init__(self, node_list, edge_list, service_list):
        self.nodes = {}  # Dictionary of nodes {node_id: Node}
        self.edges = {}  # Dictionary of edges {edge_id: Edge}
        self.services = {}  # Dictionary of services {service_id: Service}

        # Initialize the network with given nodes, edges, and services
        self._initialize_nodes(node_list)
        self._initialize_edges(edge_list)
        self._initialize_services(service_list)

    def _initialize_nodes(self, node_list):
        """Initialize nodes with channel conversion opportunities."""
        for idx, conversion_opportunities in enumerate(node_list, start=1):
            self.nodes[idx] = Node(idx, conversion_opportunities)

    def _initialize_edges(self, edge_list):
        """Initialize edges with pairs of connected nodes."""
        for idx, (node1, node2) in enumerate(edge_list, start=1):
            self.add_edge(idx, node1, node2)

    def _initialize_services(self, service_list):
        """Initialize services based on the given list format."""
        for service_id, (src, dst, num_edges, start_wl, end_wl, value, path) in enumerate(service_list, start=1):
            self.add_service(service_id, src, dst, path, (start_wl, end_wl), value)

    def add_edge(self, edge_id, node1, node2):
        """Add an edge to the network, connecting two nodes."""
        if edge_id not in self.edges:
            # Add nodes if they don't exist
            if node1 not in self.nodes:
                self.nodes[node1] = Node(node1, 0)  # Create node if it doesn't exist
            if node2 not in self.nodes:
                self.nodes[node2] = Node(node2, 0)  # Create node if it doesn't exist

            # Create the new edge
            edge = Edge(edge_id, node1, node2)
            self.edges[edge_id] = edge
            
            # Update adjacency lists in nodes
            self.nodes[node1].add_adj(self.nodes[node2], edge_id)
            self.nodes[node2].add_adj(self.nodes[node1], edge_id)
        else:
            raise ValueError(f"Edge {edge_id} already exists.")

    def add_service(self, service_id, src, dst, path, wavelength_range, value):
        """Add a service to the network, specifying source, destination, path, wavelength, and value."""
        if service_id not in self.services:
            if all(edge_id in self.edges for edge_id in path):
                # Create the service and add it to the network
                service = Service(service_id, src, dst)
                for edge_id in path:
                    service.add_edge(edge_id, wavelength_range)  # Add edge and wavelength to service
                    self.edges[edge_id].add_service(service_id, wavelength_range)  # Register service with edge

                # Cap the service value at 100,000
                service.value = min(value, 100000)
                self.services[service_id] = service
            else:
                raise ValueError("Invalid path. Some edges in the path do not exist in the network.")
        else:
            raise ValueError(f"Service {service_id} already exists.")

    def deactivate_edge(self, edge_id):
        """Deactivate an edge and mark all services passing through it as inactive, returning their IDs."""
        if edge_id in self.edges:
            edge = self.edges[edge_id]
            if edge.active:
                # Deactivate the edge
                associated_services = edge.deactivate()  # Get associated services and deactivate the edge
                deactivated_service_ids = []  # List to hold IDs of deactivated services

                # Mark all services using this edge as deactivated
                for service_id in associated_services:
                    if service_id in self.services:
                        service = self.services[service_id]
                        if not service.dead:  # Check if the service is not dead
                            service.deactivate()  # Mark service as inactive
                            deactivated_service_ids.append(service_id)  # Add service ID to the list

                return deactivated_service_ids
            else:
                raise ValueError(f"Edge {edge_id} is already deactivated.")
        else:
            raise ValueError(f"Edge {edge_id} does not exist in the network.")


    def remove_service_from_edges(self, service_id):
        """Remove the specified service from all edges in its path without clearing the path."""
        if service_id not in self.services:
            raise ValueError(f"Service ID {service_id} does not exist in the network.")

        service = self.services[service_id]
        edge_ids = service.path  # Get the list of edge IDs in the service path

        for edge_id in edge_ids:
            if edge_id in self.edges:
                edge = self.edges[edge_id]
                edge.remove_service(service_id)  # Remove the service from the edge
            else:
                raise ValueError(f"Edge ID {edge_id} does not exist in the network.")


    def redirect_service(self, service):
        """Attempt to redirect a service to a new path, checking for available wavelengths."""
        src = service.src
        dst = service.dst

        # Initialize BFS queue and visited set
        queue = deque([(src, [])])  # Start from the source node
        visited = set()  # Keep track of visited nodes

        while queue:
            current_node, path = queue.popleft()

            # If we've reached the destination
            if current_node == dst:
                return path  # Return the new path

            if current_node in visited:
                continue

            visited.add(current_node)

            # Get adjacent edges from the current node
            current_adj_nodes = self.nodes[current_node].get_adj()
            for adj_node_id in current_adj_nodes:
                edges_to_adj = self.nodes[current_node].get_edges(self.nodes[adj_node_id])
                for edge_id in edges_to_adj:
                    edge = self.edges[edge_id]
                    
                    # Check if the edge is active and has available wavelengths
                    if edge.active:
                        for (start, end) in service.wavelengths:  # Assuming service.wavelengths is a list of tuples
                            if edge.has_available_wavelengths(start, end):
                                # Append the edge ID to the path and enqueue the adjacent node
                                queue.append((adj_node_id, path + [edge_id]))
                                break  # Move to the next edge since we found an available wavelength

        return None  # Failed to redirect the service


    def __repr__(self):
        return (f"Network(nodes={list(self.nodes.keys())}, "
                f"edges={list(self.edges.keys())}, "
                f"services={list(self.services.keys())})")


import enum

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
    edges = []
    services_read = 0 #num de lineas de services leídas
    services = []

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
            service = list(int(x) for x in l.split())

            # Parse the service edges
            l = input()
            service.append(list(int(x) for x in l.split()))

            # Add the service to the network
            services.append(service)

    return nodes, edges, services

import random

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
            edge = random.randint(1, len(edges))
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
        print(*[edge for edge in scenario], flush=True)

def process_scenario(network, edge_ids):
    """
    Deactivate edges, mark associated services as inactive, 
    and attempt to redirect the services.

    :param network: The Network object containing edges and services.
    :param edge_ids: A list of edge IDs to deactivate.
    :return: A tuple containing:
             - A list of service IDs that were successfully redirected.
             - The updated network.
    """
    redirected_services = []  # List to collect IDs of successfully redirected services
    deactivated_services = []  # List to collect all deactivated service IDs

    for edge_id in edge_ids:
        # Deactivate the edge and mark associated services as inactive
        try:
            # Deactivate the edge and get the associated services that were deactivated
            deactivated_services.extend(network.deactivate_edge(edge_id))  # Use .extend() for better performance
        except ValueError as e:
            # Raise an exception if the edge does not exist
            raise ValueError(f"Error: {e}")

    # After processing all edges, attempt to redirect the deactivated services
    for service_id in deactivated_services[:1]:
        service = network.services.get(service_id)
        # Check if the service is not dead and not active
        if service and not service.dead and not service.active:  
            # Attempt to redirect the service
            redirection = network.redirect_service(service)
            if redirection:  # Redirect the service
                network.remove_service_from_edges(service_id)  # Remove the service from edges
                network.services[service_id].path = redirection
                redirected_services.append(service_id)  # Add to redirected list
            else:
                service.mark_as_dead()  # Mark service as dead if redirection fails

    return redirected_services, network  # Return the list of redirected services and the updated network

import copy

nodes, edges, services = parse_network()
base_network = Network(nodes, edges, services)

scenarios = produce_scenarios(edges)
print_scenarios(scenarios)

n_scenarios = int(input())


for _ in range(n_scenarios):
    scenario = copy.deepcopy(base_network)

    continuee = True

    while continuee:
        line = input()

        if line == "-1":
            continuee = False
        else:
            edges_ids = [int(x) for x in line.split()]

            redirected_services, scenario = process_scenario(scenario, edges_ids[:1])

            print(len(redirected_services), flush=True)
            for service in redirected_services:
                print(service, len(scenario.services[service].path), flush=True)
                path = scenario.services[service].path
                wavelengths = scenario.services[service].wavelengths
                stuff = []
                for edge, (w_start, w_end) in zip(path, wavelengths):
                    stuff.extend([edge, w_start, w_end])

                print(*stuff, flush=True)
