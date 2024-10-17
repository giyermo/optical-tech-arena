#!/usr/bin/env python
import contextlib as __stickytape_contextlib

@__stickytape_contextlib.contextmanager
def __stickytape_temporary_dir():
    import tempfile
    import shutil
    dir_path = tempfile.mkdtemp()
    try:
        yield dir_path
    finally:
        shutil.rmtree(dir_path)

with __stickytape_temporary_dir() as __stickytape_working_dir:
    def __stickytape_write_module(path, contents):
        import os, os.path

        def make_package(path):
            parts = path.split("/")
            partial_path = __stickytape_working_dir
            for part in parts:
                partial_path = os.path.join(partial_path, part)
                if not os.path.exists(partial_path):
                    os.mkdir(partial_path)
                    with open(os.path.join(partial_path, "__init__.py"), "wb") as f:
                        f.write(b"\n")

        make_package(os.path.dirname(path))

        full_path = os.path.join(__stickytape_working_dir, path)
        with open(full_path, "wb") as module_file:
            module_file.write(contents)

    import sys as __stickytape_sys
    __stickytape_sys.path.insert(0, __stickytape_working_dir)

    __stickytape_write_module('constants.py', b'"""\r\nConstans for the proyect\r\n\r\nAll range constants are made like: [i, j] and not [i, j) as range() function performs.\r\n"""\r\n"""\r\n////////////////////////////////////////////////////////////////////////////////////////////\r\n- General\r\n////////////////////////////////////////////////////////////////////////////////////////////\r\n"""\r\n\r\nK = 40 # Optical wavelenghts\r\n\r\n\r\n"""\r\n////////////////////////////////////////////////////////////////////////////////////////////\r\n- Input\r\n////////////////////////////////////////////////////////////////////////////////////////////\r\n"""\r\n# 2 <= N <= 200\r\nN_BOUND_LOW = 2\r\nN_BOUND_UPP = 200\r\nN_BOUND_RANGE = range(N_BOUND_LOW, N_BOUND_UPP + 1)\r\n\r\n# 1 <= M <= 1000\r\nM_BOUND_LOW = 1\r\nM_BOUND_UPP = 1000\r\nM_BOUND_RANGE = range(M_BOUND_LOW, M_BOUND_UPP + 1)\r\n\r\n# Number of channel conversions opp\r\n# 0 <= P_i <= 20\r\nCHANNEL_CONV_OPP_LOWER_BOUND = 0\r\nCHANNEL_CONV_OPP_UPP_BOUND = 20\r\nCHANNEL_CONV_OPP_UPP_RANGE = range(CHANNEL_CONV_OPP_LOWER_BOUND, CHANNEL_CONV_OPP_UPP_BOUND + 1)\r\n\r\n# The number of services initially running on the graph\r\n# 1 <= J <= 5000\r\n\r\nNUM_SERVICES_INIT_MIN = 1\r\nNUM_SERVICES_INIT_MAX = 5000\r\nNUM_SERVICES_INIT_RANGE = range(NUM_SERVICES_INIT_MIN, NUM_SERVICES_INIT_MAX + 1)\r\n\r\n# Service value\r\n# 0 <= V <= 100.000\r\n\r\nSERVICE_VALUE_MIN = 0\r\nSERVICE_VALUE_MAX = 100_000\r\nSERVICE_VALUE_RANGE = range(SERVICE_VALUE_MIN, SERVICE_VALUE_MAX + 1)\r\n\r\n"""\r\n////////////////////////////////////////////////////////////////////////////////////////////\r\n- Scenarios\r\n////////////////////////////////////////////////////////////////////////////////////////////\r\n"""\r\n# Number of failure\r\n# 0 <= T_1 <= 30\r\nT_1_MIN = 0\r\nT_1_MAX = 30\r\n# Failures\r\n# 0 <= T_1 <= 60\r\nT_2_MIN = 0\r\nT_2_MAX = 60\r\n')
    __stickytape_write_module('network.py', b'import heapq\nimport copy\n\nclass Network:\n    def __init__(self, nodes: list, edges: list, services: list):\n        """\n        Initialize the network with the given nodes, edges and services.\n\n        :param nodes: A list of nodes\n        :param edges: A dictionary of edges, where the keys are the edge indices\n            and the values are tuples of the connected nodes.\n        :param services: A list of services, where each service is a dictionary\n            with the keys \'src\', \'dst\', \'num_edges\', \'wavelengths\', \'value\'\n            and \'path\'. The \'path\' key is a list of edge indices.\n        """\n\n        for idx, node in enumerate(nodes):\n            node_dict = {\n                "oportunities": node,\n                "adjacent": [],\n            }\n            nodes[idx] = node_dict\n        self.nodes = dict(enumerate(nodes, 1))  # List of nodes\n\n        for idx, edge in enumerate(edges):\n            edge_dict = {\n                "vertices": edge[:2],\n                "services": edge[-1],\n                "wavelengths": [],\n                "active": True\n            }\n            v1, v2 = edge_dict["vertices"]\n\n            matching_tuples = [tup for tup in self.nodes[v1]["adjacent"] if tup[0] == v2]\n            if matching_tuples:\n                if any(tup[1] == idx+1 for tup in matching_tuples):\n                    # The vertex is in the list and the edge matches\n                    pass\n                else:\n                    # The vertex is in the list but the edge doesn\'t match\n                    self.nodes[v1]["adjacent"].append((v2, idx+1))\n            else:\n                # The vertex is not in the list\n                self.nodes[v1]["adjacent"].append((v2, idx+1))\n\n            matching_tuples = [tup for tup in self.nodes[v2]["adjacent"] if tup[0] == v1]\n            if matching_tuples:\n                if any(tup[1] == idx+1 for tup in matching_tuples):\n                    # The vertex is in the list and the edge matches\n                    pass\n                else:\n                    # The vertex is in the list but the edge doesn\'t match\n                    self.nodes[v2]["adjacent"].append((v1, idx+1))\n            else:\n                # The vertex is not in the list\n                self.nodes[v2]["adjacent"].append((v1, idx+1))\n\n \n            edges[idx] = edge_dict\n        self.edges = dict(enumerate(edges, 1))  # Adjacency list to store edges (graph representation)\n\n        self.services = services  # List to store service details\n        for service in self.services:\n            for edge in service["path"]:\n                wavlength_range = range(service["wavelengths"][0], service["wavelengths"][1] + 1)\n                self.edges[edge]["wavelengths"].extend(wavlength_range)\n\n    def deactivate_edge(self, idx):\n        """Delete an undirected edge between nodes u and v."""\n        self.edges[idx]["active"] = False\n        v1, v2 = self.edges[idx]["vertices"]\n        self.nodes[v1]["adjacent"] = [tup for tup in self.nodes[v1]["adjacent"] if tup[1] != idx]\n        self.nodes[v2]["adjacent"] = [tup for tup in self.nodes[v2]["adjacent"] if tup[1] != idx]\n\n    def deactivate_service(self, idx):\n        """Delete an undirected edge between nodes u and v."""\n        self.services[idx-1]["active"] = False\n\n    def set_service_dead(self, idx):\n        """Kill a service."""\n        if not self.services[idx]["active"]:\n            self.services[idx]["dead"] = True\n\n    def failure_edge_nodes(self, service: dict):\n        """If there\'s a failure in the service\'s path return the nodes of the failed edge, otherwise None"""\n        for edge_idx in service[\'path\']: # Check all the nodes edges of the path\n            current_edge = self.edges[edge_idx - 1] #As the index starts in 1 -> index - 1 to start in 0\n            if not current_edge[\'active\']: #Check the edge is not active\n                return current_edge[\'vertices\'] # Return the edge\'s nodes\n            \n    def check_free_bandwidth(edge: dict, bw: tuple) -> bool:\n        """\n        If the bandwidth \'collides\' with the occupied wavelenghts of the edge returns False, and viceversa.\n        """\n        for edge_bw in edge[\'wavelenghts\']:\n            if not (bw[1] < edge_bw[0] or bw[0] > edge_bw[1]):\n                return False    \n        return True\n    \n    def solve_scenario(self, base_network):\n        print("0", flush=True)\n\n    # def min_dist_path1(self, start_node, end_node):\n    #     """\n    #     Find the shortest path between two nodes in a graph using flood algorithm.\n    #     Returns both node path and edge path, ensuring edges have no wavelengths.\n    #     """\n    #     visited = set()\n    #     queue = [(start_node, [], [])]\n        \n    #     # Forward search to find the end node\n    #     while queue:\n    #         current_node, node_path, edge_path = queue.pop(0)\n    #         if current_node == end_node:\n    #             visited.add(current_node)\n    #             break\n            \n    #         if current_node not in visited:\n    #             visited.add(current_node)\n    #             for neighbor, edge_id in self.nodes[current_node]["adjacent"]:\n    #                 if neighbor not in visited and not self.edges[edge_id]["wavelengths"]:\n    #                     new_node_path = node_path + [current_node]\n    #                     new_edge_path = edge_path + [edge_id]\n    #                     queue.append((neighbor, new_node_path, new_edge_path))\n        \n    #     # If end_node not found, return None\n    #     if end_node not in visited:\n    #         return None, None\n        \n    #     # Reverse search starting from end_node\n    #     reverse_node_path = [end_node]\n    #     reverse_edge_path = []\n    #     current_node = end_node\n        \n    #     while current_node != start_node:\n    #         for neighbor, edge_id in self.nodes[current_node]["adjacent"]:\n    #             if neighbor in visited and neighbor not in reverse_node_path and not self.edges[edge_id]["wavelengths"]:\n    #                 reverse_node_path.append(neighbor)\n    #                 reverse_edge_path.append(edge_id)\n    #                 current_node = neighbor\n    #                 break\n        \n    #     return list(reversed(reverse_node_path)), list(reversed(reverse_edge_path))\n\n    def min_dist_path(self, start_node, end_node, service):\n        visited = set()\n        queue = [(start_node, [start_node], [])]\n        \n        while queue:\n            current_node, node_path, edge_path = queue.pop(0)\n            \n            if current_node == end_node:\n                return node_path, edge_path\n            \n            for neighbor, edge_id in self.nodes[current_node]["adjacent"]:\n                if neighbor not in visited and self.edges[edge_id]["active"]:\n                    edge_wavelengths = set(self.edges[edge_id]["wavelengths"])\n                    service_wavelengths = set(range(service["wavelengths"][0], service["wavelengths"][1] + 1))\n                    \n                    if not service_wavelengths.intersection(edge_wavelengths):\n                        new_node_path = node_path + [neighbor]\n                        new_edge_path = edge_path + [edge_id]\n                        queue.append((neighbor, new_node_path, new_edge_path))\n                        visited.add(neighbor)\n        \n        return None\n    \n\n    def redirect_broken_service(self, service):\n        #print("\\nRedirecting broken service", service["path"])\n        start_node = service[\'src\']\n        end_node = service[\'dst\']\n        result = self.min_dist_path(start_node, end_node, service)\n\n        if result:\n            for edge in service["path"]:\n                self.edges[edge]["services"].remove(service["id"])\n                self.edges[edge]["wavelengths"] = list(set(self.edges[edge]["wavelengths"])-set(service["wavelengths"]))\n            new_node_path, new_edge_path = result\n            service[\'path\'] = new_edge_path\n            if new_edge_path:\n                for edge_id in new_edge_path:\n                    service_wavelengths = set(range(service["wavelengths"][0], service["wavelengths"][1] + 1))\n                    self.edges[edge_id]["wavelengths"].extend(service_wavelengths)\n            service[\'active\'] = True\n            service["path"] = new_edge_path\n            return new_node_path, new_edge_path\n\n        service["dead"] = True\n        return None\n\n\n        \n\n    def search_adjacent_edges(self, node, next, bandwidth):\n        """\n        Returns a reacheable edge\n        """\n        for edge in self.nodes[node][\'adjacent\']:\n            if edge[0] == next:\n                if self.check_free_bandwidth(self.edges[edge[1]], bandwidth):\n                    return edge    \n\n    def dijkstra(self, start_node, end_node, band_width: tuple) -> list:\n        """\n        Dijkstra\'s algorithm to find the shortest path between two nodes in a graph.\n\n        Args:\n            start_node: The node where the path starts.\n            end_node: The node where the path ends.\n\n        Returns:\n            A list of nodes representing the shortest path from start_node to end_node.\n            If no path is found, it returns None, which should be an error as the graph should be connected.\n        """\n        distances = {node: float(\'inf\') for node in self.nodes} #Init all nodes in a dict with infinty distance\n        distances[start_node] = 0\n        priority_queue = [(0, start_node)]\n\n        # A SLinked list would fit better\n        predecessors = [] # The value is just the next key, so you assure the path\n\n        while priority_queue:\n            current_distance, current_node = heapq.heappop(priority_queue) #pop the queue\n\n            if current_node == end_node: #reached END NODE\n                #Found end_node and create the path list\n                path = []\n                while current_node is not None:\n                    path.append(current_node)\n                    current_node = predecessors[current_node] \n                return tuple(path[::-1]) # Reversed, then it will be from start to end\n            \n            if current_distance > distances[current_node]:\n                continue\n            \n            # Neighbors are the adjacents nodes that are connected with an active edge\n            # Check neighbors via edges\n            accesible = [] # idx 0: node, idx 1: vertex that connect node with prev\n            neighbors = [node for node in self.nodes[current_node]["adjacent"]]\n            for next in neighbors:\n                acc_edge = self.search_adjacent_edges(current_distance, next, band_width)\n                if acc_edge: # The edge exists and not None\n                    accesible.append(next, acc_edge)\n            \n            for neig_node in accesible[0]:\n                distance = current_distance + 1 # The weight of an edge is 1\n                if distance < distances[neig_node]:\n                        distances[neig_node] = distance\n                        predecessors[neig_node] = accesible[1] # Save the edge for the path\n                        heapq.heappush(priority_queue, (distance, neig_node)) #push the queue\n        return None #No path is found, which should be an error as the graph should be connected      \n        \n        \n    def solve_scenatio_hmg_beta_1(self):\n        #i\'ll assume the algorythm is executed after a failure occurs in a node\n        #self.sort_services(self.services)\n        inactive_services = [service for service in self.services if not service[\'active\']]\n        sorted(inactive_services, key=lambda x: x[\'value\'], reverse=True) #sort the values by its value\n\n        for serv in inactive_services:\n            edge_nodes = self.failure_edge_nodes(serv) # Get the nodes of the broken edge\n            if not edge_nodes:\n                print(\'Error: failure in the detecting failed services system the service \',serv,\' should be damaged\')\n                continue # No failed edge found\n            else:\n                start_node, end_node = edge_nodes # Unpack the edges from the tuple\n\n            new_serv = copy.deepcopy(serv)\n            #As the edge is deleted find the sortest path\n            new_path = self.dijkstra(start_node,end_node) # Search the shortest path between the nodes of the damaged edge\n            new_serv[\'path\'] = new_path\n        \n')
    __stickytape_write_module('scenario_maker.py', b'import random\n\ndef produce_scenarios(edges):\n    """\n    Produce failure scenarios\n\n    Naive version, with random failures\n\n    Parameters\n    ----------\n    edges : list\n        List of edges of the graph\n\n    Returns\n    -------\n    list\n        List of lists of edges that fail in each scenario\n    """\n    scenarios_no = 1# random.randint(1, T_1_MAX)\n    scenarios = []\n    for scenario in range(scenarios_no):\n        scenario_edges = []\n        failures = 1#random.randint(1, min(int(len(edges)/3), T_2_MAX))\n        for _ in range(failures):\n            edge = random.randint(0, len(edges)-1)\n            if edge not in scenario_edges:\n                scenario_edges.append(edge)\n        if scenario_edges not in scenarios:\n            scenarios.append(scenario_edges)\n    return scenarios\n\ndef print_scenarios(scenarios:list):\n    """\n    Print failure scenarios to the standard output\n\n    The first line contains the number of failure scenarios.\n    The following lines describe each scenario, with the first number being\n    the number of edges that fail, and the following numbers the indices of\n    the edges that fail, counted from 1.\n    """\n    print(len(scenarios), flush=True)\n    for scenario in scenarios:\n        print(len(scenario), flush=True)\n        # Edges should be counted from 1\n        print(*[edge + 1 for edge in scenario], flush=True)')
    __stickytape_write_module('parser.py', b'import enum\n\ndef parse_network():\n    """\n    Parse the input data for the graph and services.\n\n    It reads the input data from the standard input, parses it and returns the graph and services as a tuple.\n\n    The input data is divided into four parts: The size of the graph, the nodes, the edges and the services.\n    The size of the graph contains the number of nodes and edges.\n    The nodes are given as a list of channel conversion opportunities.\n    The edges are given as a list of pairs of nodes.\n    The services are given as a list of tuples, containing the source, destination, number of edges, wavelength start, wavelength end and value of the service.\n    The path of each service is given as a list of edges.\n\n    Returns:\n        tuple: A tuple containing the nodes, edges and services of the graph.\n    """\n\n    class Kind(enum.Enum):\n        #Como el input est\xc3\xa1 dividido por partes, enum ayuda a dividirlo\n        SIZE = 0\n        NODES = 1\n        EDGES = 2\n        SERVICES_NO = 3\n        SERVICES = 4\n        END = 5\n\n    kind = Kind.SIZE\n    nodes = [] \n    edges_read = 0 #num de lineas de edges le\xc3\xaddas\n    edges: list[list] = []\n    services_read = 0 #num de lineas de services le\xc3\xaddas\n    services: list[tuple] = []\n\n    while kind != Kind.END:\n        # Set the network (graph) properties during iterations\n        l = input()\n        if kind == Kind.SIZE:\n            #Set the size of the network (graph)\n            kind = Kind.NODES # Move to nodes\n            nodes_no, edges_no = [int(x) for x in l.split()]\n        elif kind == Kind.NODES:\n            #Set the list of nodes and it\'s channel conversion oportunities\n            kind = Kind.EDGES # Move to edges\n            nodes = list(int(x) for x in l.split())\n        elif kind == Kind.EDGES:\n            # For each iteration, add a edge to the network (graph)\n            edges_read += 1\n            if edges_read == edges_no:\n                kind = Kind.SERVICES_NO\n            edge = list(int(x) for x in l.split())\n            edge.append([])\n            edges.append(edge)\n        elif kind == Kind.SERVICES_NO:\n            #Set the number of services in the network\n            kind = Kind.SERVICES\n            services_no = int(l)\n        elif kind == Kind.SERVICES:\n            # Add a service to the network (graph)\n            services_read += 1\n            if services_read == services_no:\n                kind = Kind.END\n\n            # Parse the service\n            service_tuple = tuple(int(x) for x in l.split())\n            service = {\n                \'id\': services_read,\n                \'src\': service_tuple[0],\n                \'dst\': service_tuple[1],\n                \'num_edges\': service_tuple[2],\n                \'wavelengths\': (service_tuple[3], service_tuple[4]),\n                \'value\': service_tuple[5],\n                \'path\': None,\n                \'active\': True,\n                \'dead\': False\n            }\n\n            # Parse the service edges\n            l = input()\n            service["path"] = tuple(int(x) for x in l.split())\n            for edge in service["path"]:\n                edges[edge - 1][-1].append(services_read)\n\n            # Add the service to the network\n            services.append((service))\n\n    return nodes, edges, services')
    from constants import *
    from network import *
    from parser import *
    from scenario_maker import *
    
    # Parse the network
    nodes, edges, services = parse_network()
    base_network = Network(nodes, edges, services)
    

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


        

    def search_adjacent_edges(self, node, next, bandwidth):
        """
        Returns a reacheable edge
        """
        for edge in self.nodes[node]['adjacent']:
            if edge[0] == next:
                if self.check_free_bandwidth(self.edges[edge[1]], bandwidth):
                    return edge    

    def dijkstra(self, start_node, end_node, band_width: tuple) -> list:
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

        # A SLinked list would fit better
        predecessors = [node for node in self.nodes] # The value is just the next key, so you assure the path

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue) #pop the queue

            if current_node == end_node: #reached END NODE
                #Found end_node and create the path list
                path = []
                while current_node is not None:
                    path.append(current_node)
                    prev_node, edge = predecessors[current_node]  # Obtener nodo anterior y arista
                    if edge:  # If the edge exists it's appended
                        path.append(edge)

                    current_node = prev_node
                return tuple(path[::-1]) # Reversed, then it will be from start to end
            
            if current_distance > distances[current_node]:
                continue
            
            # Neighbors are the adjacents nodes that are connected with an active edge
            # Check neighbors via edges
            accesible = [] # idx 0: node, idx 1: vertex that connect node with prev
            neighbors = [node for node in self.nodes[current_node]["adjacent"]]
            for next in neighbors:
                acc_edge = self.search_adjacent_edges(current_distance, next, band_width)
                if acc_edge: # The edge exists and not None
                    accesible.append(next, acc_edge)
            
            for neig_node in accesible[0]:
                distance = current_distance + 1 # The weight of an edge is 1
                if distance < distances[neig_node]:
                        distances[neig_node] = distance
                        predecessors[neig_node] = (accesible[1],current_node) # Save the edge for the path
                        heapq.heappush(priority_queue, (distance, neig_node)) #push the queue
        return None #No path is found, which should be an error as the graph should be connected      
        
        
    def solve_scenatio_hmg_beta_1(self, serv):
        #i'll assume the algorythm is executed after a failure occurs in a node
        #self.sort_services(self.services)
        #not used inactive_services = [service for service in self.services if not service['active']]
        #sorted(inactive_services, key=lambda x: x['value'], reverse=True) #sort the values by its value
        start_node, end_node = self.failure_edge_nodes(serv) # Get the nodes of the broken edge

        new_serv = copy.deepcopy(serv)
        #As the edge is deleted find the sortest path
        new_path = self.dijkstra(start_node,end_node) # Search the shortest path between the nodes of the damaged edge
        if new_path:
            new_serv['path'] = new_path
            serv = new_serv
        else:
            serv['dead'] = True
        return serv


def produce_scenarios(edges):
    """
    Produce failure scenarios

    Naive version, with random failures

    Parameters
    ----------
    edges : list
        List of edges of the graph

    Returns
    -------
    list
        List of lists of edges that fail in each scenario
    """
    scenarios_no = 1# random.randint(1, T_1_MAX)
    scenarios = []
    for scenario in range(scenarios_no):
        scenario_edges = []
        failures = 1#random.randint(1, min(int(len(edges)/3), T_2_MAX))
        for _ in range(failures):
            edge = random.randint(0, len(edges)-1)
            if edge not in scenario_edges:
                scenario_edges.append(edge)
        if scenario_edges not in scenarios:
            scenarios.append(scenario_edges)
    return scenarios

def print_scenarios(scenarios:list):
    """
    Print failure scenarios to the standard output

    The first line contains the number of failure scenarios.
    The following lines describe each scenario, with the first number being
    the number of edges that fail, and the following numbers the indices of
    the edges that fail, counted from 1.
    """
    print(len(scenarios), flush=True)
    for scenario in scenarios:
        print(len(scenario), flush=True)
        # Edges should be counted from 1
        print(*[edge + 1 for edge in scenario], flush=True)


# Parse the network
nodes, edges, services = parse_network()
base_network = Network(nodes, edges, services)

scenarios = produce_scenarios(edges)
print_scenarios(scenarios)


scenarios_no = int(input()) # Number of scenarios provided by the environment

for _ in range(scenarios_no):
    edges = [int(x) for x in input().split()]
    scenario = copy.deepcopy(base_network)
    broken_serv = set()
    fixed_serv = set()

    while edges[0] != -1:
        for edge in edges:
            scenario.deactivate_edge(edge)
            for service in scenario.edges[edge]["services"]:
                if not scenario.services[service-1]["dead"]:
                    broken_serv.add(service)
                scenario.deactivate_service(service-1)

            """
            #Guille's aproach
            for idx in list(broken_serv):
            service = scenario.services[idx-1]
            if not service["dead"]:
                redirect = scenario.redirect_broken_service(service)
                if redirect:
                    fixed_serv.add(idx)
                    broken_serv.remove(idx)
                else:
                    broken_serv.add(idx)
                    fixed_serv.discard(idx)
            """
            #Héctor's aproach
            list(broken_serv)
            sorted(broken_serv, key=lambda x: x['value'], reverse=True) #sort the values by its value
            for idx in list(broken_serv):
                service = scenario.services[idx-1]
                if not service["dead"]:
                    redirect = scenario.solve_scenatio_hmg_beta_1(service)
                    if redirect:
                        fixed_serv.add(idx)
                        broken_serv.remove(idx)
                    else:
                        broken_serv.add(idx)
                        fixed_serv.discard(idx)



        print(len(fixed_serv), flush=True)

        for service in fixed_serv:
            print(service, len(scenario.services[service-1]["path"]), flush=True)
            output = []
            for edge in scenario.services[service-1]["path"]:
                start, end = scenario.services[service-1]["wavelengths"]
                output.extend([edge, start, end])
            print(*output, flush=True)

        broken_serv.clear()
        fixed_serv.clear()

        edges = [int(x) for x in input().split()]
