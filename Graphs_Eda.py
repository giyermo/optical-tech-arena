"""
Created by: Héctor Molina Garde

Es el código de grafos de EDA, que los suma todos desde el final.
Tanto el codigo basico de grafos y Djikstra como los ejercicios
Dado que el problema va en base 
"""
import sys
import random


# Classes and functions
class AdjacentVertex:
	"""This class allows us to represent a tuple with an adjacent vertex
	and the weight associated (by default 1, for non-unweighted graphs)"""

	def __init__(self, vertex, weight=None):
		self._vertex = vertex
		self._weight = weight

	def __str__(self):
		if self._weight is not None:
			return '(' + str(self._vertex) + ',' + str(self._weight) + ')'
		else:
			return str(self._vertex)


class Graph:
	def __init__(self, vertices, directed=True):
		"""We use a dictionary to represent the graph
		the dictionary's keys are the vertices
		The value associated for a given key will be the list of their neighbours.
		Initially, the list of neighbours is empty"""
		self._vertices = {}
		for v in vertices:
			self._vertices[v] = []
		self._directed = directed

	def addEdge(self, start, end, weight=None):
		if start not in self._vertices.keys():
			print(start, ' does not exist!')
			return
		if end not in self._vertices.keys():
			print(end, ' does not exist!')
			return

		# adds to the end of the list of neigbours for start
		self._vertices[start].append(AdjacentVertex(end, weight))

		if self._directed == False:
			# adds to the end of the list of neigbours for end
			self._vertices[end].append(AdjacentVertex(start, weight))

	def containsEdge(self, start, end):
		if start not in self._vertices.keys():
			print(start, ' does not exist!')
			return 0
		if end not in self._vertices.keys():
			print(end, ' does not exist!')
			return 0

		# we search the AdjacentVertex whose v is end
		for adj in self._vertices[start]:
			if adj._vertex == end:
				if adj._weight != None:
					return adj._weight
				else:
					return 1  # unweighted graphs
		return 0  # does not exist

	def removeEdge(self, start, end):
		if start not in self._vertices.keys():
			print(start, ' does not exist!')
			return
		if end not in self._vertices.keys():
			print(end, ' does not exist!')
			return

		# we must look for the adjacent AdjacentVertex (neighbour)  whose vertex is end, and then remove it
		for adj in self._vertices[start]:
			if adj._vertex == end:
				self._vertices[start].remove(adj)
		if self._directed == False:
			# we must also look for the AdjacentVertex (neighbour)  whose vertex is end, and then remove it
			for adj in self._vertices[end]:
				if adj._vertex == start:
					self._vertices[end].remove(adj)

	def __str__(self):
		result = ''
		for v in self._vertices:
			result += '\n' + str(v) + ':'
			for adj in self._vertices[v]:
				result += str(adj) + "  "
		return result

	"""--/////////// TRAVERSALS ///////////--"""

	# Function to return a BFS of graph from vertex v
	def _bfs(self, v, visited):
		"""This functions obtains the BFS traversal from the vertex
		whose index is indexV."""

		output = []

		# Create a queue for BFS. It will save the indices of vertices to visit
		queue = []
		# mark the source vertex as visited
		visited[v] = True
		# and enqueue it
		queue.append(v)

		while queue:
			# Dequeue a vertex from queue
			s = queue.pop(0)

			# we add the vertex to the output list
			output.append(s)

			# Get all adjacent vertices of the dequeued index.
			# If an adjacent vertex has not been visited,
			# then mark it visited and enqueue it
			for adj in self._vertices[s]:
				if visited[adj._vertex] == False:
					queue.append(adj.vertex)
					visited[adj.vertex] = True

		return output

	# Function to return a DFS of graph from vertex v
	def _dfs(self, v, visited, dfslist):
		visited[v] = True
		dfslist.append(v)
		for adj in self._vertices[v]:
			if visited[adj._vertex] == False:
				self._dfs(adj._vertex, visited, dfslist)


class GraphDijkstra(Graph):

	def minDistance(self, distances, visited):
		"""This functions returns the vertex (index) whose associated value in
		the dictionary distances is the smallest value. We
		only consider the set of vertices that have not been visited"""
		# Initilaize minimum distance for next node
		min = sys.maxsize

		# returns the vertex with minimum distance from the non-visited vertices
		for vertex in self._vertices.keys():
			if distances[vertex] <= min and visited[vertex] == False:
				min = distances[vertex]  # update the new smallest
				min_vertex = vertex  # update the index of the smallest

		return min_vertex

	def dijkstra(self, origin):
		""""This function takes a vertex v and calculates its mininum path
		to the rest of vertices by using the Dijkstra algoritm"""

		# visisted is a dictionary whose keys are the verticies of our graph.
		# When we visite a vertex, we must mark it as True.
		# Initially, all vertices are defined as False (not visited)
		visited = {}
		for v in self._vertices.keys():
			visited[v] = False

		# this dictionary will save the previous vertex for the key in the minimum path
		previous = {}
		for v in self._vertices.keys():
			# initially, we defines the previous vertex for any vertex as None
			previous[v] = None

		# This distance will save the accumulate distance from the
		# origin to the vertex (key)
		distances = {}
		for v in self._vertices.keys():
			distances[v] = sys.maxsize

		# The distance from origin to itself is 0
		distances[origin] = 0

		for n in range(len(self._vertices)):
			# Pick the vertex with the minimum distance vertex.
			# u is always equal to origin in first iteration
			u = self.minDistance(distances, visited)

			visited[u] = True

			# Update distance value of the u's adjacent vertices only if the current
			# distance is greater than new distance and the vertex in not in the shotest path tree

			# we must visit all adjacent vertices (neighbours) for u
			for adj in self._vertices[u]:
				i = adj.vertex
				w = adj.weight
				if visited[i] == False and distances[i] > distances[u] + w:
					# we must update because its distance is greater than the new distance
					distances[i] = distances[u] + w
					previous[i] = u

		# finally, we print the minimum path from origin to the other vertices
		self.printSolution(distances, previous, origin)

	def printSolution(self, distances, previous, origin):
		print("Mininum path from ", origin)

		for i in self._vertices.keys():

			if distances[i] == sys.maxsize:
				print("There is not path from ", origin, ' to ', i)
			else:

				# minimum_path is the list wich contains the minimum path from origin to i
				minimum_path = []
				prev = previous[i]
				# this loop helps us to build the path
				while prev != None:
					minimum_path.insert(0, prev)
					prev = previous[prev]

				# we append the last vertex, which is i
				minimum_path.append(i)

				# we print the path from v to i and the distance
				print(origin, '->', i, ":", minimum_path, distances[i])


"""///////////////////////////////////////////////////////////////////////////////////"""


class Graph2(GraphDijkstra):

	def get_adjacents(self, vertex):
		if vertex in self._vertices.keys():
			adjac = []
			for adj in self._vertices[vertex]:
				adjac.append(adj._vertex)
			return adjac
		return

	def get_origins(self, vertex):
		if vertex in self._vertices.keys():
			origin = []
			for key in self._vertices.keys():
				for edge in self._vertices[key]:
					if edge._vertex == vertex:
						origin.append(key)
			return origin

	def vertices_with_max_edges(self, max_num):
		result = []
		for key in self._vertices.keys():
			if len(self._vertices[key]) >= max_num:
				result.append(key)
		return result

	def get_reachable_bfs(self, vertex):
		if vertex in self._vertices.keys():
			output, queue, visited = [], [], {}
			for v in self._vertices.keys():
				visited[v] = False
			visited[vertex] = True
			queue.append(vertex)
			while queue:
				s = queue.pop(0)
				output.append(s)
				for adj in self._vertices[s]:
					if visited[adj._vertex] is False:
						queue.append((adj._vertex))
						visited[adj._vertex] = True
			return output

	def get_reachable_dfs(self, vertex):
		visited = {}
		for v in self._vertices.keys():
			visited[v] = False
		self._dfs(vertex, visited, [])
		return [key for key in visited if visited[key]]

	def non_accesible(self, vertex):
		visited = {}
		for v in self._vertices.keys():
			visited[v] = False
		self._dfs(vertex, visited, [])
		return [key for key in visited if not visited[key]]

	def checkPath(self, station1, station2):
		def dfs(v, visited):
			visited[v] = True
			for adj in self._vertices[v]:
				if not visited[adj._vertex]:
					dfs(adj._vertex, visited)

		visited = {}
		for v in self._vertices.keys():
			visited[v] = False
		dfs(station1, visited)
		return visited[station2]

	def get_suggestions(self, p, min_jumps):
		distances, previous = self.dijkstra(p)
		result = []
		for v in distances.keys():
			if distances < sys.maxsize and distances[v] >= min_jumps:
				result.append(v)
		return result

	def print_connected_components(self):
		visited = {}
		count = 0
		for v in self._vertices:
			visited[v] = False

		for v in self._vertices:
			if not visited[v]:
				queue, connection = [], []
				queue.append(v)
				while queue:
					s = queue.pop(0)
					connection.append(s)
					for adj in self._vertices[s]:
						if not visited[adj._vertex]:
							queue.append(adj._vertex)
							visited[adj._vertex] = True
				print(connection)
				count += 1
		return count


class MyGraph:
	def _init_(self, n):
		"""Creates a graph with n vertices (0,1,..,n-1) """
		self.vertices = {}
		for i in range(n):
			self.vertices[i] = []

	def addConnection(self, i, j):
		if i not in self.vertices.keys():
			return
		if j not in self.vertices.keys():
			return
		self.vertices[i].append(j)

	def check_path(self, i, j):
		if all((i, j)) in self.vertices.keys():
			visited = {}
			for v in self.vertices:
				visited[v] = False
			self._dfs(i, visited)
			return visited[j]

	def _dfs(self, v, visited):
		visited[v] = True
		for adj in self.vertices:
			if not visited[adj]:
				self._dfs(adj, visited)

	def get_list_no_path(self, start):
		if start in self.vertices.keys():
			visited = {}
			for v in self.vertices:
				visited[v] = False
			self._dfs(start, visited)
			return [key for key in visited if not [visited]]

	def get_mothers(self):
		result = []
		for v in self.vertices.keys():
			if self.count_bfs(v) == len(self.vertices.keys()):
				result.append(v)
		return result

	def count_bfs(self, vertex):
		if vertex in self.vertices:
			queue, visited, count= [], {}, 0
			for v in self.vertices:
				visited[v] = False
			visited[vertex] = True
			queue.append(vertex)
			while queue:
				u = queue.pop(0)
				count += 1
				for adj in self.vertices[u]:
					if not visited[adj]:
						visited[adj] = True
						queue.append(adj)
			return count

	def is_strongly_conn(self):
		for vertex in self.vertices.keys():
			visited = {}
			for v in self.vertices.keys():
				visited[v] = False
			self.connected_dfs(vertex, visited)
			if not any(visited.values()):
				return False
		return True

	def connected_dfs(self, vertex, visited):
		visited[vertex] = True
		for adj in self.vertices[vertex]:
			self.connected_dfs(adj, visited)
		

if __name__ == '__main__':
	vertices = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j')
	G = Graph2(vertices)
	G.addEdge('a', 'b', 2)
	G.addEdge('b', 'c', 2)
	G.addEdge('f', 'c', 8)
	G.addEdge('d', 'a', 1)
	G.addEdge('d', 'f', 3)
	G.addEdge('e', 'f', 4)
	G.addEdge('a', 'f', 5)
	G.addEdge('b', 'd', 4)
	G.addEdge('c', 'e', 6)
	G.addEdge('g', 'a', 3)
	G.addEdge('h', 'b', 7)
	G.addEdge('i', 'c', 9)
	G.addEdge('j', 'd', 10)
	G.addEdge('g', 'e', 1)
	G.addEdge('h', 'f', 5)
	G.addEdge('i', 'g', 2)
	G.addEdge('j', 'h', 3)
	G.addEdge('i', 'a', 4)
	G.addEdge('j', 'b', 5)
	G.addEdge('g', 'c', 6)
	G.addEdge('h', 'd', 7)
	G.addEdge('i', 'e', 8)
	G.addEdge('j', 'f', 9)
	print(G)
	input_needed = True
	exercise = int(input("exercise\n>>")) if input_needed else 1
	if exercise == 1:
		print(G.get_adjacents('b'))
		print(G.get_adjacents('d'))
	elif exercise == 2:
		print(G.get_origins('b'))
		print(G.get_origins('c'))
		print(G.get_origins('d'))
	elif exercise == 3:
		print(G.vertices_with_max_edges(0))
		print(G.vertices_with_max_edges(1))
		print(G.vertices_with_max_edges(2))
	elif exercise == 4:
		for vertex in vertices:
			print(vertex)
			print(G.get_reachable_bfs(vertex))
			print(G.get_reachable_dfs(vertex))
			print('-' * 20)
	elif exercise == 5:
		for vertex in vertices:
			print(vertex)
			print(G.non_accesible(vertex))
			print('-' * 20)
	elif exercise == 6:
		# Create a graph with 100 stations
		stations = [f'S{i}' for i in range(1, 101)]
		G = Graph2(stations)

		# Randomly add edges between stations
		num_edges = 150  # You can adjust this number based on the desired density of the network

		for _ in range(num_edges):
			from_station = random.choice(stations)
			to_station = random.choice(stations)
			if from_station != to_station:
				weight = random.randint(1, 10)  # Random weight between 1 and 10
				G.addEdge(from_station, to_station, weight)
