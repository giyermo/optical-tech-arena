from node import Node
from edge import Edge
from service import Service
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


