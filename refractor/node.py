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

# # Create some nodes
# node1 = Node(1, 10)
# node2 = Node(2, 5)
# node3 = Node(3, 7)

# # Add edges between nodes (using numeric edge IDs)
# node1.add_adj(node2, 1)  # Edge ID 1 connects node1 to node2
# node1.add_adj(node2, 2)  # Edge ID 2 (parallel edge) connects node1 to node2
# node1.add_adj(node3, 3)  # Edge ID 3 connects node1 to node3
# node2.add_adj(node3, 4)  # Edge ID 4 connects node2 to node3

# # Display the nodes and their connections
# print("Nodes and their connections before removal:")
# print(node1)
# print(node2)
# print(node3)

# # Remove an edge
# node1.remove_adj(node2, 1)  # Remove edge ID 1 connecting node1 to node2
# node1.remove_adj(node2, 2)  # Remove edge ID 1 connecting node1 to node2

# # Display the updated nodes
# print("\nAfter removing edge ID 1:")
# print(node1)
# print(node2)
# print(node3)

# # Remove the last edge between node1 and node2
# node1.remove_adj(node2, 102)  # Remove edge ID 102 connecting node1 to node2

# # Display the updated nodes
# print("\nAfter removing edge ID 102 (last edge):")
# print(node1)
# print(node2)
