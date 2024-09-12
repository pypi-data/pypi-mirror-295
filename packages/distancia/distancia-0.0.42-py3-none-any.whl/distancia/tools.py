#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  tools.py
#  

def check_bin(str_):
    if str(str_) in "01":
        return True
    return False
    
def check_probability(number):
    if number>=0 and number <=1.0:
        return True
    else: return False
    
def factorial(n):
    if n == 0:
        return 1
    else:
        return n * factorial(n - 1)


def exp(x, terms=20):
    """
    Calculate the exponential of x using Taylor series expansion.
    
    Parameters:
    x (float): The exponent
    terms (int): Number of terms to use in the Taylor series (default: 20)
    
    Returns:
    float: An approximation of e^x
    """
    result = 0
    for n in range(terms):
        result += x**n / factorial(n)
    return result
    
def sin(x, terms=10):
    x = x % (2 * 3.141592653589793)  # réduction de l'angle à une période
    result = 0
    for n in range(terms):
        numerator = ((-1) ** n) * (x ** (2 * n + 1))
        denominator = factorial(2 * n + 1)
        result += numerator / denominator
    return result
    
def cos(x, terms=10):
    x = x % (2 * 3.141592653589793)  # réduction de l'angle à une période
    result = 0
    for n in range(terms):
        numerator = ((-1) ** n) * (x ** (2 * n))
        denominator = factorial(2 * n)
        result += numerator / denominator
    return result
    
def degrees_to_radians(degrees):
    pi = 3.141592653589793
    radians = degrees * (pi / 180)
    return radians
    
def atan(x, terms=10):
    result = 0
    for n in range(terms):
        result += ((-1) ** n) * (x ** (2 * n + 1)) / (2 * n + 1)
    return result

def atan2(y, x, terms=10):
    if x > 0:
        return atan(y / x, terms)
    elif x < 0 and y >= 0:
        return atan(y / x, terms) + 3.141592653589793
    elif x < 0 and y < 0:
        return atan(y / x, terms) - 3.141592653589793
    elif x == 0 and y > 0:
        return 3.141592653589793 / 2
    elif x == 0 and y < 0:
        return -3.141592653589793 / 2
    else:
        return 0  # (0, 0) case
	
def log(x, iterations=1000):
    """
    Approximates the natural logarithm (log base e) of x using Newton's method.
    
    :param x: The value to compute the natural logarithm for.
    :param iterations: The number of iterations to improve the approximation.
    :return: Approximated natural logarithm of x.
    """
    if x <= 0:
        raise ValueError("Math domain error. Input must be greater than 0.")
    
    # Initial guess
    guess = x if x < 2 else x / 2
    
    # Newton's method to approximate log(x)
    for _ in range(iterations):
        guess -= (guess - x / (2.718281828459045 ** guess)) / (1 + x / (2.718281828459045 ** guess))
    
    return guess
    


    
def rank(data):
    """
    Spearman
    Calcule les rangs des valeurs dans la liste donnée.
    
    :param data: Liste des valeurs à classer.
    :return: Liste des rangs correspondant aux valeurs.
    """
    sorted_indices = sorted(range(len(data)), key=lambda i: data[i])
    ranks = [0] * len(data)
    rank_sum = 0
    last_value = None
    
    for index in sorted_indices:
        if last_value is None or data[index] != last_value:
            rank_sum = index + 1
        else:
            rank_sum += index + 1
        
        ranks[index] = rank_sum / (sorted_indices.index(index) + 1)
        last_value = data[index]
    
    return ranks

def spearman_correlation(x, y):
    """
    Spearman
    Calcule le coefficient de corrélation de Spearman entre deux listes de données.
    
    :param x: Liste des valeurs de la première variable.
    :param y: Liste des valeurs de la seconde variable.
    :return: Coefficient de corrélation de Spearman entre x et y.
    """
    if len(x) != len(y):
        raise ValueError("Les listes x et y doivent avoir la même longueur.")
    
    n = len(x)
    
    # Calcul des rangs
    rank_x = rank(x)
    rank_y = rank(y)
    
    # Calcul de la différence des rangs
    d_squared_sum = sum((rank_x[i] - rank_y[i]) ** 2 for i in range(n))
    
    # Calcul du coefficient de corrélation de Spearman
    spearman_corr = 1 - (6 * d_squared_sum) / (n * (n * n - 1))
    
    return spearman_corr
    
##############################

class Scalar:
	pass
	
class Matrix:
    
	def invert_matrix(matrix):
		"""
		Calcule l'inverse d'une matrice carrée.
    
		:param matrix: Matrice carrée à inverser.
		:return: Matrice inverse.
		"""
		from copy import deepcopy
		n = len(matrix)
		A = deepcopy(matrix)
		I = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    
		for i in range(n):
			if A[i][i] == 0:
				for k in range(i + 1, n):
					if A[k][i] != 0:
						A[i], A[k] = A[k], A[i]
						I[i], I[k] = I[k], I[i]
						break
        
				for j in range(n):
					if i != j:
						ratio = A[j][i] / A[i][i]
						for k in range(n):
							A[j][k] -= ratio * A[i][k]
							I[j][k] -= ratio * I[i][k]
    
		for i in range(n):
			divisor = A[i][i]
			for j in range(n):
				I[i][j] /= divisor
		return I
		
	def covariance_matrix(data):
		"""
		Calcule la matrice de covariance pour un ensemble de données.
    
		:param data: Liste de listes, où chaque sous-liste représente une observation.
		:return: Matrice de covariance.
		"""
		n = len(data)
		m = len(data[0])
		mean = [sum(col) / n for col in zip(*data)]
		cov_matrix = [[0] * m for _ in range(m)]
    
		for i in range(m):
			for j in range(m):
				cov_matrix[i][j] = sum((data[k][i] - mean[i]) * (data[k][j] - mean[j]) for k in range(n)) / (n - 1)
    
		return cov_matrix
		
	def eigenvalues_2x2(self, matrix):
		"""
		Compute the eigenvalues of a 2x2 matrix.
        
		Parameters:
		matrix (list of list of float): 2x2 matrix.
        
		Returns:
		list of complex: Eigenvalues of the matrix.
		"""
		coeffs = self.characteristic_polynomial(matrix)
		a, b, c = coeffs
		discriminant = b**2 - 4*a*c
		eigenvalue1 = (-b + discriminant**0.5) / (2*a)
		eigenvalue2 = (-b - discriminant**0.5) / (2*a)
		return [eigenvalue1, eigenvalue2]

	def matrix_subtraction(self, A, B):
		"""
		Subtract matrix B from matrix A element-wise.
        
		Parameters:
		A (list of list of float): First matrix.
		B (list of list of float): Second matrix.
        
		Returns:
		list of list of float: Resultant matrix of A - B.
		"""
		return [[A[i][j] - B[i][j] for j in range(self.num_states)] for i in range(self.num_states)]

	def matrix_trace(self, matrix):
		"""
		Compute the trace of a matrix (sum of diagonal elements).
        
		Parameters:
		matrix (list of list of float): Matrix.
        
		Returns:
		float: Trace of the matrix.
		"""
		return sum(matrix[i][i] for i in range(self.num_states))

	def characteristic_polynomial(self, matrix):
		"""
		Compute the characteristic polynomial of a matrix.
        
		Parameters:
		matrix (list of list of float): Matrix.
        
		Returns:
		list of float: Coefficients of the characteristic polynomial.
		"""
		# For a 2x2 matrix, the characteristic polynomial is given by:
		# det(A - λI) = λ^2 - (trace(A))λ + det(A)
		a = matrix
		if self.num_states == 2:
			trace = self.matrix_trace(a)
			det = a[0][0]*a[1][1] - a[0][1]*a[1][0]
			return [1, -trace, det]
		else:
			raise NotImplementedError("Characteristic polynomial calculation for matrices larger than 2x2 is not implemented.")
            
class Graph:
	def __init__(self, nodes, edges):
		self.nodes = nodes
		self.edges = edges
		self.adjacency_matrix = self.create_adjacency_matrix()
		self.adjacency_list = self.create_adjacency_list()

	def create_adjacency_matrix(self):
		matrix = [[0 for _ in range(len(self.nodes))] for _ in range(len(self.nodes))]
		node_index = {node: i for i, node in enumerate(self.nodes)}
        
		for edge in self.edges:
			i, j = node_index[edge[0]], node_index[edge[1]]
			matrix[i][j] = 1
			matrix[j][i] = 1  # Assuming the graph is undirected

		return matrix

	def create_adjacency_list(self):
		adj_list = {node: [] for node in self.nodes}
		for edge in self.edges:
			u, v = edge
			adj_list[u].append(v)
			adj_list[v].append(u)  # Assuming the graph is undirected
		return adj_list

	def count_motifs(self, motif_size):
		motifs = {}
		for node in self.nodes:
			neighbors = self.adjacency_list[node]
			if len(neighbors) >= motif_size - 1:
				for sub_motif in self._find_sub_motifs(node, neighbors, motif_size - 1):
					sub_motif = tuple(sorted(sub_motif))
					if sub_motif in motifs:
						motifs[sub_motif] += 1
					else:
						motifs[sub_motif] = 1
		return motifs

	def _find_sub_motifs(self, node, neighbors, remaining):
		if remaining == 1:
			return [(node, neighbor) for neighbor in neighbors]
		sub_motifs = []
		for i, neighbor in enumerate(neighbors):
			new_neighbors = neighbors[i + 1:]
			for sub_motif in self._find_sub_motifs(neighbor, new_neighbors, remaining - 1):
				sub_motifs.append((node,) + sub_motif)
		return sub_motifs
        
	def get_nodes(self):
		nodes = set()
		for edge in self.edges:
			nodes.update(edge)
		return list(nodes)
        
	def _get_edges(self, graph):
		"""
		Returns a set of edges from a graph, ensuring each edge is only counted once in an undirected graph.
        
		:param graph: The graph as a dictionary.
		:return: A set of edges.
		"""
		edges = set()
		for node, neighbors in graph.items():
			for neighbor in neighbors:
				if (node, neighbor) not in edges and (neighbor, node) not in edges:
					edges.add((node, neighbor))
		return edges
        
	def dijkstra(self, start_node, end_node):
		"""
		Implémente l'algorithme de Dijkstra pour trouver le plus court chemin entre deux nœuds.
		:param start_node: Le nœud de départ.
		:param end_node: Le nœud d'arrivée.
		:return: La distance du plus court chemin entre start_node et end_node.
		"""
		import heapq

		# Initialisation des distances de tous les nœuds à l'infini, sauf le nœud de départ à 0
		distances = {node: float('inf') for node in self.graph}
		distances[start_node] = 0

		# File de priorité pour gérer les nœuds à explorer
		priority_queue = [(0, start_node)]

		while priority_queue:
			current_distance, current_node = heapq.heappop(priority_queue)

			# Si nous avons atteint le nœud de destination, on peut arrêter
			if current_node == end_node:
				return current_distance

			# Si la distance actuelle est supérieure à la distance déjà trouvée, on saute
			if current_distance > distances[current_node]:
				continue

			# Explorer les voisins du nœud actuel
			for neighbor, weight in self.graph[current_node].items():
				distance = current_distance + weight

			# Si une distance plus courte est trouvée, mettre à jour et ajouter à la queue
			if distance < distances[neighbor]:
				distances[neighbor] = distance
				heapq.heappush(priority_queue, (distance, neighbor))

		# Si le nœud d'arrivée est injoignable, retourner l'infini
		return float('inf')
        
class MarkovChain:
	def stationary_distribution(self, matrix, tolerance=1e-10, max_iterations=1000):
		"""
		Compute the stationary distribution of a Markov chain from its transition matrix.
        
		Parameters:
		matrix (list of list of float): Transition matrix of the Markov chain.
		tolerance (float): Tolerance level for convergence.
		max_iterations (int): Maximum number of iterations for convergence.
        
		Returns:
		list of float: The stationary distribution of the Markov chain.
		"""
		dist = [1.0 / self.num_states] * self.num_states  # Initial uniform distribution
		for _ in range(max_iterations):
			next_dist = [0] * self.num_states
			for i in range(self.num_states):
				for j in range(self.num_states):
					next_dist[i] += dist[j] * matrix[j][i]
				if all(abs(next_dist[i] - dist[i]) < tolerance for i in range(self.num_states)):
					break
				dist = next_dist
		return dist
