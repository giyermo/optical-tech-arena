class OpticalNetwork:
    def __init__(self):
        self.nodes = []  # List of nodes
        self.edges = {}  # Adjacency list to store edges (graph representation)
        self.conversion_opportunities = []  # List to store channel conversion opportunities for each node
        self.services = []  # List to store service details

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

def parse_input():
    # Initialize the optical network
    network = OpticalNetwork()

    # Step 1: Read the number of nodes (n) and edges (m)
    n, m = map(int, input().strip().split())
    network.nodes = list(range(1, n + 1))  # Node IDs from 1 to n

    # Step 2: Read the channel conversion opportunities for each node
    network.conversion_opportunities = list(map(int, input().strip().split()))

    # Step 3: Read edges of the graph (m edges)
    for _ in range(m):
        u, v = map(int, input().strip().split())
        network.add_edge(u, v)

    # Step 4: Read the number of services
    s = int(input().strip())

    # Step 5: Parse each service's details
    for _ in range(s):
        # Read service details (6 values: src, dst, num_edges, wavelength_start, wavelength_end, value)
        src, dst, num_edges, wavelength_start, wavelength_end, value = map(int, input().strip().split())

        # Read the edge sequence for the service
        edge_sequence = list(map(int, input().strip().split())) if num_edges > 0 else []

        # Add the service to the network
        network.add_service(src, dst, num_edges, wavelength_start, wavelength_end, value, edge_sequence)

    return network

# Step 6: Initialize the network from input
optical_network = parse_input()

# Print the graph representation and the parsed data for verification
print("Nodes:", optical_network.nodes)
print("Edges:", optical_network.edges)
print("Conversion Opportunities:", optical_network.conversion_opportunities)
print("Services:")
for service in optical_network.services:
    print(service)
