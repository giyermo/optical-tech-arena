from Graphs_Eda import AdjacentVertex
from Graphs_Eda import Graph


class Edge:
    """K = 40 optical wavelengths
    Pueden ser paralelos"""
    def __init__(self):
        pass

class Optical_network(Graph):
    """Es como la clase de grafo de EDA del año pasado"""

    def __init__(self, vertices: list):
        super().__init__(vertices, directed=False)

    def ONSC_challenge(self):
        """Optical Network Service Continuity
Optimization Challenge"""
        pass

def gen_vertices_list(v: int):
    """Return list with n vertices from 1 to v"""
    return [i for i in range(1, v + 1)]


if __name__ == '__main__':
    # Para guardar los inputs, al usar input, directamente \n se aplica
    # 2 <= n <= 200, 1 <= m <= 1000
    n, m = map(int, input().split())  # Leer número de nodos y aristas
    conversion_opportunities = list(map(int, input().split()))  # Leer oportunidades de conversión
    edges = [tuple(map(int, input().split())) for _ in range(m)]  # Leer aristas
    s = int(input())  # Leer número de servicios

    services = []
    for _ in range(s):
        service_info = list(map(int, input().split()))  # Leer información del servicio
        service_edges = list(map(int, input().split()))  # Leer las aristas del servicio
        services.append((service_info, service_edges))
