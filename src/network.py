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
        v1, v2 = self.edges[idx]["vertices"]
        self.nodes[v1]["adjacent"] = [tup for tup in self.nodes[v1]["adjacent"] if tup[1] != idx]
        self.nodes[v2]["adjacent"] = [tup for tup in self.nodes[v2]["adjacent"] if tup[1] != idx]

    def deactivate_service(self, idx):
        """Delete an undirected edge between nodes u and v."""
        self.services[idx-1]["active"] = False

    def set_service_dead(self, idx):
        """Kill a service."""
        if not self.services[idx]["active"]:
            self.services[idx]["dead"] = True

    def failure_edge_nodes(self, service: dict):
        """If there's a failure in the service's path return the nodes of the failed edge, otherwise None"""
        for edge_idx in service['path']: # Check all the nodes edges of the path
            current_edge = self.edges[edge_idx - 1] #As the index starts in 1 -> index - 1 to start in 0
            if not current_edge['active']: #Check the edge is not active
                return current_edge['vertices'] # Return the edge's nodes
    
    def solve_scenario(self, base_network):
        print("0", flush=True)

    # def min_dist_path1(self, start_node, end_node):
    #     """
    #     Find the shortest path between two nodes in a graph using flood algorithm.
    #     Returns both node path and edge path, ensuring edges have no wavelengths.
    #     """
    #     visited = set()
    #     queue = [(start_node, [], [])]
        
    #     # Forward search to find the end node
    #     while queue:
    #         current_node, node_path, edge_path = queue.pop(0)
    #         if current_node == end_node:
    #             visited.add(current_node)
    #             break
            
    #         if current_node not in visited:
    #             visited.add(current_node)
    #             for neighbor, edge_id in self.nodes[current_node]["adjacent"]:
    #                 if neighbor not in visited and not self.edges[edge_id]["wavelengths"]:
    #                     new_node_path = node_path + [current_node]
    #                     new_edge_path = edge_path + [edge_id]
    #                     queue.append((neighbor, new_node_path, new_edge_path))
        
    #     # If end_node not found, return None
    #     if end_node not in visited:
    #         return None, None
        
    #     # Reverse search starting from end_node
    #     reverse_node_path = [end_node]
    #     reverse_edge_path = []
    #     current_node = end_node
        
    #     while current_node != start_node:
    #         for neighbor, edge_id in self.nodes[current_node]["adjacent"]:
    #             if neighbor in visited and neighbor not in reverse_node_path and not self.edges[edge_id]["wavelengths"]:
    #                 reverse_node_path.append(neighbor)
    #                 reverse_edge_path.append(edge_id)
    #                 current_node = neighbor
    #                 break
        
    #     return list(reversed(reverse_node_path)), list(reversed(reverse_edge_path))

    def min_dist_path(self, start_node, end_node, service):
        visited = set()
        queue = [(start_node, [start_node], [])]
        
        while queue:
            current_node, node_path, edge_path = queue.pop(0)
            
            if current_node == end_node:
                return node_path, edge_path
            
            for neighbor, edge_id in self.nodes[current_node]["adjacent"]:
                if neighbor not in visited and self.edges[edge_id]["active"]:
                    edge_wavelengths = set(self.edges[edge_id]["wavelengths"])
                    service_wavelengths = set(range(service["wavelengths"][0], service["wavelengths"][1] + 1))
                    
                    if not service_wavelengths.intersection(edge_wavelengths):
                        new_node_path = node_path + [neighbor]
                        new_edge_path = edge_path + [edge_id]
                        queue.append((neighbor, new_node_path, new_edge_path))
                        visited.add(neighbor)
        
        return None
    

    def redirect_broken_service(self, service):
        #print("\nRedirecting broken service", service["path"])
        start_node = service['src']
        end_node = service['dst']
        result = self.min_dist_path(start_node, end_node, service)

        if result:
            for edge in service["path"]:
                self.edges[edge]["services"].remove(service["id"])
                self.edges[edge]["wavelengths"] = list(set(self.edges[edge]["wavelengths"])-set(service["wavelengths"]))
            new_node_path, new_edge_path = result
            service['path'] = new_edge_path
            if new_edge_path:
                for edge_id in new_edge_path:
                    service_wavelengths = set(range(service["wavelengths"][0], service["wavelengths"][1] + 1))
                    self.edges[edge_id]["wavelengths"].extend(service_wavelengths)
            service['active'] = True
            service["path"] = new_edge_path
            return new_node_path, new_edge_path

        service["dead"] = True
        return None



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
                return tuple(path[::-1]) # Reversed, then it will be from start to end
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
    
    def path_nodes_to_edges(self, path: tuple) -> tuple:
        """
        Convert a tuple of nodes path to a edge path
        """
        new_path = []
        for i in range(len(path) - 1):
            current, next = path[i], path[i+1]
            i = 0
            while edge[0] == next: # and widthwave free:
                edge =  self.nodes[current]["adjacent"][i] #index of the (v,idx_edge)
                i += 1
                if i > len(self.nodes[current]["adjacent"]): #If no edge is found then the path is incorrect
                    raise IndexError(f'There is no path between: {current} and {next}')
            new_path.append(self.edges[edge[1]]) #append the edge from the index

        return tuple(new_path)


    def solve_scenatio_hmg_beta_1(self):
        #i'll assume the algorythm is executed after a failure occurs in a node
        #self.sort_services(self.services)
        inactive_services = [service for service in self.services if not service['active']]
        for serv in inactive_services:
            edge_nodes = self.failure_edge_nodes(serv) # Get the nodes os the broken edge
            if not edge_nodes:
                print('Error: failure in the detecting failed services system the service ',serv,' should be damaged')
                continue # No failed edge found
            else:
                start_node, end_node = edge_nodes # Unpack the edges from the tuple

            new_serv = copy.deepcopy(serv)
            #As the edge is deleted find the sortest path
            new_path = self.dijkstra(start_node,end_node) # Search the shortest path between the nodes of the damaged edge
            #This path is given by nodes, then it has to be converted to edges.
            new_path = self.path_nodes_to_edges(new_path)
            new_serv['path'] = new_path
