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

# # Create an edge
# edge1 = Edge(id=1, node1=1, node2=2)

# # Add services to the edge with their wavelength ranges
# edge1.add_service(service_id=101, wavelength_range=(10, 20))
# edge1.add_service(service_id=102, wavelength_range=(15, 25))

# # Display the edge state
# print("Edge state after adding services:")
# print(edge1)

# # Remove a service
# edge1.remove_service(service_id=101)

# # Display the edge state after removal
# print("\nEdge state after removing service 101:")
# print(edge1)

# # Deactivate the edge
# deactivated_services = edge1.deactivate()

# # Display the edge state after deactivation
# print("\nEdge state after deactivation:")
# print(edge1)

# # List of deactivated services
# print("\nDeactivated services:", deactivated_services)
