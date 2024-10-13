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

    def solve_scenario(self, base_network):
        print("0", flush=True)
