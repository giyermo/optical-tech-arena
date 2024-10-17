import enum

def parse_network():
    """
    Parse the input data for the graph and services.

    It reads the input data from the standard input, parses it and returns the graph and services as a tuple.

    The input data is divided into four parts: The size of the graph, the nodes, the edges and the services.
    The size of the graph contains the number of nodes and edges.
    The nodes are given as a list of channel conversion opportunities.
    The edges are given as a list of pairs of nodes.
    The services are given as a list of tuples, containing the source, destination, number of edges, wavelength start, wavelength end and value of the service.
    The path of each service is given as a list of edges.

    Returns:
        tuple: A tuple containing the nodes, edges and services of the graph.
    """

    class Kind(enum.Enum):
        #Como el input está dividido por partes, enum ayuda a dividirlo
        SIZE = 0
        NODES = 1
        EDGES = 2
        SERVICES_NO = 3
        SERVICES = 4
        END = 5

    kind = Kind.SIZE
    nodes = [] 
    edges_read = 0 #num de lineas de edges leídas
    edges = []
    services_read = 0 #num de lineas de services leídas
    services = []

    while kind != Kind.END:
        # Set the network (graph) properties during iterations
        l = input()
        if kind == Kind.SIZE:
            #Set the size of the network (graph)
            kind = Kind.NODES # Move to nodes
            nodes_no, edges_no = [int(x) for x in l.split()]
        elif kind == Kind.NODES:
            #Set the list of nodes and it's channel conversion oportunities
            kind = Kind.EDGES # Move to edges
            nodes = list(int(x) for x in l.split())
        elif kind == Kind.EDGES:
            # For each iteration, add a edge to the network (graph)
            edges_read += 1
            if edges_read == edges_no:
                kind = Kind.SERVICES_NO
            edge = list(int(x) for x in l.split())
            edges.append(edge)
        elif kind == Kind.SERVICES_NO:
            #Set the number of services in the network
            kind = Kind.SERVICES
            services_no = int(l)
        elif kind == Kind.SERVICES:
            # Add a service to the network (graph)
            services_read += 1
            if services_read == services_no:
                kind = Kind.END

            # Parse the service
            service = list(int(x) for x in l.split())

            # Parse the service edges
            l = input()
            service.append(list(int(x) for x in l.split()))

            # Add the service to the network
            services.append(service)

    return nodes, edges, services