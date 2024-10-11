class OpticalNetwork:
    def __init__(self):
        self.nodes = []  # List of nodes
        self.edges = {}  # Dictionary to represent the graph as an adjacency list
        self.conversion_opportunities = []  # List to store channel conversion opportunities for each node
        self.services = []  # List to store service details

def parse_input():
    network = OpticalNetwork()

    # Step 1: Read the number of nodes (n) and edges (m)
    n, m = map(int, input().strip().split())
    print("number of nodes read")
    network.nodes = list(range(1, n + 1))  # Node IDs from 1 to n

    # Step 2: Read the channel conversion opportunities for each node
    network.conversion_opportunities = list(map(int, input().strip().split()))
    print("Read channel conversions")

    # Step 3: Read edges of the graph
    for _ in range(m):
        u, v = map(int, input().strip().split())
        print("Read edges")
        # Create the adjacency list for the graph
        if u not in network.edges:
            network.edges[u] = []
        if v not in network.edges:
            network.edges[v] = []
        network.edges[u].append(v)  # Add edge u -> v
        network.edges[v].append(u)  # Add edge v -> u (undirected graph)

    # Step 4: Read the number of services
    s = int(input().strip())
    print("Read number of services")

    # Step 5: Parse each service's details
    for _ in range(s):
        # Read service details
        service_details = list(map(int, input().strip().split()))
        print("Read service details", service_details)
        src, dst, num_edges, bandwidth, wavelength_start, wavelength_end, value = service_details

        # Read the edge sequence
        edge_sequence = list(map(int, input().strip().split()))
        print("Read the edge sequence")

        # Store the service details in a dictionary
        service_info = {
            'src': src,
            'dst': dst,
            'num_edges': num_edges,
            'bandwidth': bandwidth,
            'wavelengths': (wavelength_start, wavelength_end),
            'value': value,
            'path': edge_sequence
        }
        network.services.append(service_info)

    return network

# Step 6: Initialize the network from input
optical_network = parse_input()

# Print the graph representation for verification
print("Nodes:", optical_network.nodes)
print("Edges:", optical_network.edges)
print("Conversion Opportunities:", optical_network.conversion_opportunities)
print("Services:")
for service in optical_network.services:
    print(service)
