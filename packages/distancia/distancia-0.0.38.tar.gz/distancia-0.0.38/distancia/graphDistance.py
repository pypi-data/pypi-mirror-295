from .mainClass import Distance
from .distance import Euclidean
#from .tools     import *

class ShortestPath(Distance):
    def __init__(self):
        """
        Initialise la classe avec un graphe représenté sous forme de dictionnaire.
        :param graph: Un dictionnaire représentant le graphe, où les clés sont les nœuds et les valeurs sont des dictionnaires
                      de voisins avec les poids des arêtes.
        """
        super().__init__()


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

    def distance_function(self,graph, start_node, end_node):
        """
        Obtient la distance du plus court chemin entre deux nœuds dans le graphe.
        :param start_node: Le nœud de départ.
        :param end_node: Le nœud d'arrivée.
        :return: La distance du plus court chemin.
        """
        self.graph = graph

        return self.dijkstra(start_node, end_node)


class GraphEditDistance(Distance):
    def __init__(self):
        """
        Initializes the GraphEditDistance class with two graphs.
        
        :param graph1: The first graph as a dictionary where keys are nodes and values are sets of connected nodes.
        :param graph2: The second graph as a dictionary where keys are nodes and values are sets of connected nodes.
        """
        super().__init__()

        

    def distance_function(self, graph1, graph2):
        """
        Computes the Graph Edit Distance (GED) between the two graphs.

        :return: The Graph Edit Distance between the two graphs.
        """
        self.graph1 = graph1
        self.graph2 = graph2
        
        # Compute node differences
        node_diff = self._node_diff(self.graph1, self.graph2)

        # Compute edge differences
        edge_diff = self._edge_diff(self.graph1, self.graph2)

        # Total cost is the sum of node and edge differences
        return node_diff + edge_diff

    def _node_diff(self, g1, g2):
        """
        Computes the difference in nodes between two graphs.
        
        :param g1: The first graph.
        :param g2: The second graph.
        :return: The node difference.
        """
        g1_nodes = set(g1.keys())
        g2_nodes = set(g2.keys())

        # Nodes to delete from g1 or add to g2
        node_deletions = g1_nodes - g2_nodes
        node_additions = g2_nodes - g1_nodes

        # Node difference is the sum of deletions and additions
        return len(node_deletions) + len(node_additions)

    def _edge_diff(self, g1, g2):
        """
        Computes the difference in edges between two graphs.
        
        :param g1: The first graph.
        :param g2: The second graph.
        :return: The edge difference.
        """
        g1_edges = self._get_edges(g1)
        g2_edges = self._get_edges(g2)

        # Edges to delete from g1 or add to g2
        edge_deletions = g1_edges - g2_edges
        edge_additions = g2_edges - g1_edges

        # Edge difference is the sum of deletions and additions
        return len(edge_deletions) + len(edge_additions)

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

#claude
import networkx as nx

class SpectralDistance(Distance):
    """
    A class to compute the spectral distance between two graphs.

    The spectral distance is based on the difference between the eigenvalues
    of the Laplacian matrices of the graphs.

    Attributes:
        k (int): Number of eigenvalues to consider (default is None, which uses all eigenvalues)
        normalized (bool): Whether to use normalized Laplacian (default is False)
    """

    def __init__(self, k=None, normalized=False):
        """
        Initialize the SpectralDistance object.

        Args:
            k (int, optional): Number of eigenvalues to consider. If None, all eigenvalues are used.
            normalized (bool, optional): Whether to use the normalized Laplacian. Defaults to False.
        """
        super().__init__()

        self.k = k
        self.normalized = normalized

    def laplacian_matrix(self, G):
        """
        Compute the Laplacian matrix of the graph.

        Args:
            G (networkx.Graph): Input graph

        Returns:
            list of list: Laplacian matrix
        """
        n = G.number_of_nodes()
        L = [[0 for _ in range(n)] for _ in range(n)]
        
        for i in range(n):
            for j in range(n):
                if i == j:
                    L[i][j] = G.degree(i)
                elif G.has_edge(i, j):
                    L[i][j] = -1
        
        if self.normalized:
            for i in range(n):
                for j in range(n):
                    if G.degree(i) > 0 and G.degree(j) > 0:
                        L[i][j] /= (G.degree(i) * G.degree(j))**0.5
        
        return L

    def eigenvalues(self, matrix):
        """
        Compute eigenvalues using the power iteration method.

        Args:
            matrix (list of list): Input matrix

        Returns:
            list: Approximate eigenvalues
        """
        n = len(matrix)
        eigenvalues = []
        for _ in range(n):
            # Initialize random vector
            v = [1/(n)**0.5 for _ in range(n)]
            for _ in range(100):  # Number of iterations
                # Matrix-vector multiplication
                u = [sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n)]
                # Normalize
                norm = (sum(x*x for x in u))**0.5
                if norm==0:norm=1
                v = [x/norm for x in u]
            # Compute Rayleigh quotient
            lambda_ = sum(v[i] * sum(matrix[i][j] * v[j] for j in range(n)) for i in range(n))
            eigenvalues.append(lambda_)
            # Deflate the matrix
            for i in range(n):
                for j in range(n):
                    matrix[i][j] -= lambda_ * v[i] * v[j]
        return sorted(eigenvalues)

    def distance_function(self, G1, G2):
        """
        Calculate the spectral distance between two graphs.

        Args:
            G1 (networkx.Graph): First graph
            G2 (networkx.Graph): Second graph

        Returns:
            float: Spectral distance between G1 and G2

        Raises:
            ValueError: If the graphs have different numbers of nodes and k is None
        """
        L1 = self.laplacian_matrix(G1)
        L2 = self.laplacian_matrix(G2)
        
        eig1 = self.eigenvalues(L1)
        eig2 = self.eigenvalues(L2)

        if self.k is None:
            if len(eig1) != len(eig2):
                raise ValueError("Graphs must have the same number of nodes when k is None")
            k = len(eig1)
        else:
            k = min(self.k, len(eig1), len(eig2))

        # Pad or truncate eigenvalues to length k
        eig1 = eig1[:k] + [0] * max(0, k - len(eig1))
        eig2 = eig2[:k] + [0] * max(0, k - len(eig2))

        # Compute Euclidean distance between eigenvalues
        #distance = (sum((e1 - e2)**2 for e1, e2 in zip(eig1, eig2)))**0.5
        distance = Euclidean().calculate(eig1, eig2)

        return distance

#claude
import networkx as nx
from collections import Counter

class WeisfeilerLehmanSimilarity(Distance):
    """
    A class to compute the Weisfeiler-Lehman similarity between two graphs.

    The Weisfeiler-Lehman algorithm is used to create a multi-set of labels
    for each graph, which are then compared to compute a similarity score.

    Attributes:
        num_iterations (int): Number of iterations for the WL algorithm
        node_label_attr (str): Attribute name for initial node labels
    """

    def __init__(self, num_iterations=3, node_label_attr=None):
        """
        Initialize the WeisfeilerLehmanSimilarity object.

        Args:
            num_iterations (int): Number of iterations for the WL algorithm. Default is 3.
            node_label_attr (str, optional): Attribute name for initial node labels.
                If None, all nodes are initially labeled with the same value.
        """
        super().__init__()

        self.num_iterations = num_iterations
        self.node_label_attr = node_label_attr

    def wl_labeling(self, G):
        """
        Perform Weisfeiler-Lehman labeling on the graph.

        Args:
            G (networkx.Graph): Input graph

        Returns:
            list: List of label multi-sets for each iteration
        """
        if self.node_label_attr:
            labels = nx.get_node_attributes(G, self.node_label_attr)
        else:
            labels = {node: '1' for node in G.nodes()}

        label_lists = [Counter(labels.values())]

        for _ in range(self.num_iterations):
            new_labels = {}
            for node in G.nodes():
                # Collect labels of neighbors
                neighbor_labels = sorted(labels[nbr] for nbr in G.neighbors(node))
                # Create a new label by combining current label and sorted neighbor labels
                new_labels[node] = f"{labels[node]}({''.join(neighbor_labels)})"
            
            # Update labels and add to label_lists
            labels = new_labels
            label_lists.append(Counter(labels.values()))

        return label_lists

    def distance_function(self, G1, G2):
        """
        Calculate the Weisfeiler-Lehman similarity between two graphs.

        Args:
            G1 (networkx.Graph): First graph
            G2 (networkx.Graph): Second graph

        Returns:
            float: Weisfeiler-Lehman similarity between G1 and G2
        """
        # Get label multi-sets for both graphs
        label_lists1 = self.wl_labeling(G1)
        label_lists2 = self.wl_labeling(G2)

        # Compute similarity for each iteration
        similarities = []
        for labels1, labels2 in zip(label_lists1, label_lists2):
            intersection = sum((labels1 & labels2).values())
            union = sum((labels1 | labels2).values())
            similarities.append(intersection / union if union > 0 else 0)

        # Return the average similarity across all iterations
        return sum(similarities) / len(similarities)

    def is_isomorphic(self, G1, G2, threshold=0.99):
        """
        Check if two graphs are potentially isomorphic using WL similarity.

        Args:
            G1 (networkx.Graph): First graph
            G2 (networkx.Graph): Second graph
            threshold (float): Similarity threshold for isomorphism. Default is 0.99.

        Returns:
            bool: True if the graphs are potentially isomorphic, False otherwise
        """
        if G1.number_of_nodes() != G2.number_of_nodes() or G1.number_of_edges() != G2.number_of_edges():
            return False
        
        similarity = self.calculate(G1, G2)
        return similarity > threshold

import numpy as np
import networkx as nx

class ComparingRandomWalkStationaryDistributions(Distance):
    """
    A class to compare stationary distributions of random walks on graphs.
    """

    def __init__(self, graph1, graph2):
        """
        Initialize the Distance object with two graphs.

        Parameters:
        graph1 (networkx.Graph): The first graph to compare
        graph2 (networkx.Graph): The second graph to compare
        """
        super().__init__()

        self.graph1 = graph1
        self.graph2 = graph2

    def compute_stationary_distribution(self, graph):
        """
        Compute the stationary distribution of a random walk on the given graph.

        Parameters:
        graph (networkx.Graph): The graph to compute the stationary distribution for

        Returns:
        numpy.ndarray: The stationary distribution vector
        """
        # Get the adjacency matrix
        adj_matrix = nx.adjacency_matrix(graph).toarray()

        # Compute the transition matrix
        degree = np.sum(adj_matrix, axis=1)
        transition_matrix = adj_matrix / degree[:, np.newaxis]

        # Compute the eigenvalues and eigenvectors
        eigenvalues, eigenvectors = np.linalg.eig(transition_matrix.T)

        # Find the eigenvector corresponding to eigenvalue 1
        stationary_index = np.argmin(np.abs(eigenvalues - 1))
        stationary_distribution = np.real(eigenvectors[:, stationary_index])

        # Normalize the distribution
        return stationary_distribution / np.sum(stationary_distribution)

    def compare_distributions(self, metric='l1'):
        """
        Compare the stationary distributions of the two graphs.

        Parameters:
        metric (str): The distance metric to use. Options: 'l1', 'l2', 'kl'. Default is 'l1'.

        Returns:
        float: The distance between the two stationary distributions
        """
        dist1 = self.compute_stationary_distribution(self.graph1)
        dist2 = self.compute_stationary_distribution(self.graph2)

        if len(dist1) != len(dist2):
            raise ValueError("The graphs must have the same number of nodes")

        if metric == 'l1':
            return np.sum(np.abs(dist1 - dist2))
        elif metric == 'l2':
            return np.sqrt(np.sum((dist1 - dist2)**2))
        elif metric == 'kl':
            return np.sum(dist1 * np.log(dist1 / dist2))
        else:
            raise ValueError("Invalid metric. Choose 'l1', 'l2', or 'kl'.")

    def random_walk(self, graph, steps, start_node=None):
        """
        Perform a random walk on the given graph.

        Parameters:
        graph (networkx.Graph): The graph to walk on
        steps (int): The number of steps to take
        start_node (int): The starting node for the walk. If None, a random node is chosen.

        Returns:
        list: The sequence of nodes visited during the walk
        """
        if start_node is None:
            start_node = np.random.choice(list(graph.nodes()))

        walk = [start_node]
        current_node = start_node

        for _ in range(steps - 1):
            neighbors = list(graph.neighbors(current_node))
            if not neighbors:
                break
            current_node = np.random.choice(neighbors)
            walk.append(current_node)

        return walk

    def compare_random_walks(self, num_walks, walk_length):
        """
        Compare random walks on both graphs.

        Parameters:
        num_walks (int): The number of random walks to perform on each graph
        walk_length (int): The length of each random walk

        Returns:
        dict: A dictionary containing the average walk length and node visit frequencies for both graphs
        """
        results = {}

        for i, graph in enumerate([self.graph1, self.graph2]):
            total_length = 0
            node_visits = {node: 0 for node in graph.nodes()}

            for _ in range(num_walks):
                walk = self.random_walk(graph, walk_length)
                total_length += len(walk)
                for node in walk:
                    node_visits[node] += 1

            avg_length = total_length / num_walks
            visit_freq = {node: visits / (num_walks * walk_length) for node, visits in node_visits.items()}

            results[f'graph{i+1}'] = {
                'avg_walk_length': avg_length,
                'node_visit_frequencies': visit_freq
            }

        return results

#claude
import networkx as nx
from collections import deque

class DiffusionDistance:
    """
    A class to compare diffusion processes on two graphs.
    """

    def __init__(self, graph1, graph2):
        """
        Initialize the DiffusionDistance object with two graphs.

        Parameters:
        graph1 (networkx.Graph): The first graph to compare
        graph2 (networkx.Graph): The second graph to compare
        """
        self.graph1 = graph1
        self.graph2 = graph2

    def compute_diffusion(self, graph, source_node, steps):
        """
        Compute the diffusion process on the given graph starting from the source node.

        Parameters:
        graph (networkx.Graph): The graph to compute the diffusion process on
        source_node (int): The starting node for the diffusion process
        steps (int): The number of steps to run the diffusion process

        Returns:
        dict: A dictionary where the keys are the nodes and the values are the diffusion values
        """
        diffusion_values = {node: 0 for node in graph.nodes()}
        diffusion_values[source_node] = 1

        queue = deque([(source_node, 0)])

        while queue and queue[0][1] < steps:
            node, step = queue.popleft()
            neighbors = list(graph.neighbors(node))

            for neighbor in neighbors:
                diffusion_values[neighbor] += diffusion_values[node] / len(neighbors)

            for neighbor in neighbors:
                queue.append((neighbor, step + 1))

        return diffusion_values

    def compare_diffusion(self, source_node, steps, metric='l1'):
        """
        Compare the diffusion processes on the two graphs.

        Parameters:
        source_node (int): The starting node for the diffusion process
        steps (int): The number of steps to run the diffusion process
        metric (str): The distance metric to use. Options: 'l1', 'l2'. Default is 'l1'.

        Returns:
        float: The distance between the two diffusion processes
        """
        diff1 = self.compute_diffusion(self.graph1, source_node, steps)
        diff2 = self.compute_diffusion(self.graph2, source_node, steps)

        if metric == 'l1':
            return sum(abs(diff1[node] - diff2[node]) for node in self.graph1.nodes())
        elif metric == 'l2':
            return sum((diff1[node] - diff2[node])**2 for node in self.graph1.nodes())**0.5
        else:
            raise ValueError("Invalid metric. Choose 'l1' or 'l2'.")
    

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
        
#chatgpt
class GraphKernelDistance:
    def __init__(self, graph1, graph2):
        self.graph1 = graph1
        self.graph2 = graph2
    
    def random_walk_kernel(self, depth=3):
        """Compute a simple random walk kernel similarity."""
        kernel_value = 0
        
        for node1 in self.graph1.nodes:
            for node2 in self.graph2.nodes:
                kernel_value += self.random_walk(node1, node2, depth)
        
        return kernel_value
    
    def random_walk(self, node1, node2, depth):
        """Recursive helper function to compute random walk similarity."""
        if depth == 0:
            return 1
        
        similarity = 0
        
        neighbors1 = self.get_neighbors(self.graph1, node1)
        neighbors2 = self.get_neighbors(self.graph2, node2)
        
        for neighbor1 in neighbors1:
            for neighbor2 in neighbors2:
                similarity += self.random_walk(neighbor1, neighbor2, depth - 1)
        
        return similarity

    def get_neighbors(self, graph, node):
        """Get the neighbors of a node in a given graph."""
        neighbors = []
        for edge in graph.edges:
            if node == edge[0]:
                neighbors.append(edge[1])
            elif node == edge[1]:
                neighbors.append(edge[0])
        return neighbors
    
    def compute(self, method="random_walk", **kwargs):
        """Compute the graph kernel distance using the specified method."""
        if method == "random_walk":
            similarity = self.random_walk_kernel(**kwargs)
            return 1 / (1 + similarity)  # Convert similarity to distance
        else:
            raise ValueError(f"Unknown method: {method}")

class FrobeniusDistance:
    def __init__(self, graph1, graph2):
        self.graph1 = graph1
        self.graph2 = graph2

    def compute(self):
        if len(self.graph1.nodes) != len(self.graph2.nodes):
            raise ValueError("Graphs must have the same number of nodes")

        distance = 0
        matrix1 = self.graph1.adjacency_matrix
        matrix2 = self.graph2.adjacency_matrix
        
        for i in range(len(matrix1)):
            for j in range(len(matrix1[i])):
                diff = matrix1[i][j] - matrix2[i][j]
                distance += diff * diff
        
        return distance ** 0.5

class PatternBasedDistance:
    def __init__(self, graph1, graph2, motif_size):
        self.graph1 = graph1
        self.graph2 = graph2
        self.motif_size = motif_size

    def compute(self):
        motifs1 = self.graph1.count_motifs(self.motif_size)
        motifs2 = self.graph2.count_motifs(self.motif_size)
        return self._calculate_distance(motifs1, motifs2)

    def _calculate_distance(self, motifs1, motifs2):
        all_motifs = set(motifs1.keys()).union(set(motifs2.keys()))
        distance = 0
        for motif in all_motifs:
            freq1 = motifs1.get(motif, 0)
            freq2 = motifs2.get(motif, 0)
            distance += abs(freq1 - freq2)
        return distance
        
import zlib

class GraphCompressionDistance:
    def __init__(self, graph1, graph2):
        """
        Initialize the GraphCompressionDistance class with two graphs.
        Each graph is represented as an adjacency matrix, which is a list of lists.

        :param graph1: Adjacency matrix of the first graph
        :param graph2: Adjacency matrix of the second graph
        """
        self.graph1 = graph1
        self.graph2 = graph2

    def compress(self, data):
        """
        Compress the data using zlib compression and return the compressed size.

        :param data: String representation of the graph
        :return: Length of the compressed data
        """
        compressed_data = zlib.compress(data.encode('utf-8'))
        return len(compressed_data)

    def adjacency_to_string(self, matrix):
        """
        Convert the adjacency matrix to a string representation.

        :param matrix: Adjacency matrix of a graph
        :return: String representation of the adjacency matrix
        """
        return ''.join([''.join(map(str, row)) for row in matrix])

    def combined_compression(self):
        """
        Compress the combined adjacency matrices of both graphs.

        :return: Length of the compressed combined adjacency matrix
        """
        combined_matrix = self.adjacency_to_string(self.graph1) + self.adjacency_to_string(self.graph2)
        return self.compress(combined_matrix)

    def compression_distance(self):
        """
        Compute the Graph Compression Distance between the two graphs.

        :return: Compression distance between the two graphs
        """
        graph1_compressed_size = self.compress(self.adjacency_to_string(self.graph1))
        graph2_compressed_size = self.compress(self.adjacency_to_string(self.graph2))
        combined_compressed_size = self.combined_compression()

        distance = combined_compressed_size - min(graph1_compressed_size, graph2_compressed_size)
        return distance
        
class DegreeDistributionDistance:
    def __init__(self, graph1, graph2):
        """
        Initializes the DegreeDistributionDistance class with two graphs.

        :param graph1: First graph, represented as an adjacency list or edge list.
        :param graph2: Second graph, represented as an adjacency list or edge list.
        """
        self.graph1 = graph1
        self.graph2 = graph2

    def compute_degree_distribution(self, graph):
        """
        Computes the degree distribution of a graph.

        :param graph: The graph for which to compute the degree distribution.
        :return: A dictionary where the keys are node degrees and the values are the counts of nodes with that degree.
        """
        degree_distribution = {}
        for node, neighbors in graph.items():
            degree = len(neighbors)
            if degree in degree_distribution:
                degree_distribution[degree] += 1
            else:
                degree_distribution[degree] = 1
        return degree_distribution

    def compare_distributions(self, dist1, dist2):
        """
        Compares two degree distributions using a simple difference metric.

        :param dist1: Degree distribution of the first graph.
        :param dist2: Degree distribution of the second graph.
        :return: A floating-point value representing the difference between the distributions.
        """
        all_degrees = set(dist1.keys()).union(set(dist2.keys()))
        difference = 0.0
        for degree in all_degrees:
            count1 = dist1.get(degree, 0)
            count2 = dist2.get(degree, 0)
            difference += abs(count1 - count2)
        return difference

    def compute_distance(self):
        """
        Computes the degree distribution distance between the two graphs.

        :return: A floating-point value representing the distance between the degree distributions of the two graphs.
        """
        dist1 = self.compute_degree_distribution(self.graph1)
        dist2 = self.compute_degree_distribution(self.graph2)
        return self.compare_distributions(dist1, dist2)


class CommunityStructureDistance:
    def __init__(self, community_detection_algorithm):
        """
        Initialize the CommunityStructureDistance class with a specific community detection algorithm.
        
        :param community_detection_algorithm: A function that takes a graph as input and returns a list of sets, 
                                              where each set represents a community (i.e., nodes that belong together).
        """
        self.community_detection_algorithm = community_detection_algorithm

    def jaccard_index(self, set1, set2):
        """
        Compute the Jaccard Index between two sets.
        
        :param set1: A set of nodes.
        :param set2: Another set of nodes.
        :return: The Jaccard Index, a measure of similarity between two sets.
        """
        intersection = len(set1.intersection(set2))
        union = len(set1.union(set2))
        return intersection / union if union != 0 else 0

    def compare_communities(self, communities1, communities2):
        """
        Compare two sets of communities and return a similarity score based on Jaccard Index.
        
        :param communities1: List of sets, where each set represents a community in the first graph.
        :param communities2: List of sets, where each set represents a community in the second graph.
        :return: The average Jaccard Index over all community pairs.
        """
        total_similarity = 0
        count = 0
        
        for community1 in communities1:
            best_similarity = 0
            for community2 in communities2:
                similarity = self.jaccard_index(community1, community2)
                best_similarity = max(best_similarity, similarity)
            total_similarity += best_similarity
            count += 1
            
        return total_similarity / count if count > 0 else 0

    def distance(self, graph1, graph2):
        """
        Compute the community structure distance between two graphs.
        
        :param graph1: The first graph (networkx.Graph object).
        :param graph2: The second graph (networkx.Graph object).
        :return: The distance between the community structures of the two graphs.
        """
        # Detect communities in both graphs
        communities1 = self.community_detection_algorithm(graph1)
        communities2 = self.community_detection_algorithm(graph2)

        # Compute similarity score
        similarity = self.compare_communities(communities1, communities2)
        
        # Convert similarity to distance (1 - similarity)
        distance = 1 - similarity
        
        return distance
