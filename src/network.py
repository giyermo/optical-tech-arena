import heapq
import copy

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

    def deactivate_service(self, idx):
        """Delete an undirected edge between nodes u and v."""
        self.services[idx]["active"] = False

    def failure_edge_nodes(self, service: dict):
        """If there's a failure in the service's path return the nodes of the failed edge, otherwise None"""
        for edge_idx in service['path']: # Check all the nodes edges of the path
            current_edge = self.edges[edge_idx]
            if not current_edge['active']: #Check the edge is not active
                return current_edge['vertices'] # Return the edge's nodes
    
    def solve_scenario(self, base_network):
        print("0", flush=True)

    def min_dist_path(self, start_node, end_node):
        """
        Find the shortest path between two nodes in a graph using Guillermo's algorithm.
        """
        s_adj = self.nodes[start_node]["adjacent"]
        e_adj = self.nodes[end_node]["adjacent"]

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
                return path[::-1] # Reversed, then it will be from start to end
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
    
    def solve_scenatio_hmg_beta_1(self):
        #i'll assume the algorythm is executed after a failure occurs in a node
        self.sort_services(self.services)
        #Assuming my proposition on self.services
        broken_services = [] #Aassuming a segregation of the services that fail
        for serv in broken_services:
            new_serv = copy.deepcopy(serv)
            #As the edge is deleted find the sortest path
            new_path = self.dijkstra(serv['src'],serv['dst'])
            """ESTO NO SE PUEDE PQ DEVUELVE NODOS Y NO LOS INDICES DE LAS ARISTAS :("""
            new_serv['path'] = new_path
