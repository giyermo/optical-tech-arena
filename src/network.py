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


    def solve_scenario(self, base_network):
        print("0", flush=True)

    def dijkstra(self, start_node, end_node) -> list:
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

            for neighbor in self.edges[current_node]:"""EL COMO FUNCIONA SELF.EDGES NO HACE Q VAYA COMO DEBERIA :("""
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
            """ESTO NO SE PUEDE PQ DEVUELVE NODOS Y NO LOS INDICES DE VERTICES :("""
            new_serv['path'] = new_path
