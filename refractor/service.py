from edge import Edge
from node import Node

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

# # Create sample edges
# edge1 = Edge(id=1, node1=1, node2=2)
# edge2 = Edge(id=2, node1=2, node2=3)
# edge3 = Edge(id=3, node1=3, node2=4)

# # Create a service
# service1 = Service(id=1, src=1, dst=4)

# # Add edge IDs to the service with corresponding wavelength ranges
# service1.add_edge(edge_id=1, wavelength_range=(10, 15))
# service1.add_edge(edge_id=2, wavelength_range=(20, 25))
# service1.add_edge(edge_id=3, wavelength_range=(30, 35))

# # Display the service state
# print("Initial service state:")
# print(service1)

# # Deactivate the service
# service1.deactivate()

# # Mark the service as dead
# service1.mark_as_dead()

# # Display the service state after changes
# print("\nService state after deactivation and marking as dead:")
# print(service1)
