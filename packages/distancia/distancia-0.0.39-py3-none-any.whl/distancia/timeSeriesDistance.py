from .mainClass import Distance
from .distance  import Euclidean
#from .tools     import *

class DynamicTimeWarping(Distance):
    def __init__(self):
        """
        Compute the Dynamic Time Warping (DTW) distance between two time series.
    
        DTW is a measure of similarity between two temporal sequences that may vary in speed.
        This class allows the computation of the DTW distance and the optimal alignment path between the sequences.
    
        Attributes:
        series_a (list or array): First time series.
        series_b (list or array): Second time series.
        distance_matrix (2D list): The accumulated cost matrix used to compute the DTW distance.
        dtw_distance (float): The computed DTW distance between series_a and series_b.
        """
        super().__init__()


    def distance_function(self, series_a, series_b):
        """
        Compute the DTW distance between the two time series.
        
        Returns:
            float: The DTW distance.
        """
        self.series_a = series_a
        self.series_b = series_b
        self.distance_matrix = None
        self.dtw_distance = None
        
        n = len(self.series_a)
        m = len(self.series_b)
        self.distance_matrix = [[float('inf')] * m for _ in range(n)]
        self.distance_matrix[0][0] = 0
        
        for i in range(1, n):
            for j in range(1, m):
                cost = abs(self.series_a[i] - self.series_b[j])
                self.distance_matrix[i][j] = cost + min(self.distance_matrix[i-1][j],    # Insertion
                                                        self.distance_matrix[i][j-1],    # Deletion
                                                        self.distance_matrix[i-1][j-1])  # Match

        self.dtw_distance = self.distance_matrix[-1][-1]
        return self.dtw_distance

    def get_optimal_path(self):
        """
        Retrieve the optimal path that aligns the two time series with the minimum cost.
        
        Returns:
            list of tuples: The optimal path as a list of index pairs (i, j).
        """
        i, j = len(self.series_a) - 1, len(self.series_b) - 1
        path = [(i, j)]
        
        while i > 0 and j > 0:
            if i == 0:
                j -= 1
            elif j == 0:
                i -= 1
            else:
                step = min(self.distance_matrix[i-1][j], self.distance_matrix[i][j-1], self.distance_matrix[i-1][j-1])
                
                if step == self.distance_matrix[i-1][j-1]:
                    i -= 1
                    j -= 1
                elif step == self.distance_matrix[i-1][j]:
                    i -= 1
                else:
                    j -= 1
            
            path.append((i, j))
        
        path.reverse()
        return path

class LongestCommonSubsequence(Distance):
	
    def __init__(self):
        """
        Initialize the LongestCommonSubsequence class with two sequences.

        :param sequence_a: The first sequence (e.g., list, string, etc.)
        :param sequence_b: The second sequence
        """
        super().__init__()

    def distance_function(self, sequence_a, sequence_b):
        """
        Compute the LCSS distance between the two sequences.

        :return: The length of the Longest Common Subsequence
        """
        self.sequence_a = sequence_a
        self.sequence_b = sequence_b
        self.lcs_matrix = None
	
        len_a = len(self.sequence_a)
        len_b = len(self.sequence_b)
        self.lcs_matrix = [[0] * (len_b + 1) for _ in range(len_a + 1)]

        for i in range(1, len_a + 1):
            for j in range(1, len_b + 1):
                if self.sequence_a[i - 1] == self.sequence_b[j - 1]:
                    self.lcs_matrix[i][j] = self.lcs_matrix[i - 1][j - 1] + 1
                else:
                    self.lcs_matrix[i][j] = max(self.lcs_matrix[i - 1][j], self.lcs_matrix[i][j - 1])

        return self.lcs_matrix[len_a][len_b]

    def get_lcs(self):
        """
        Retrieve the Longest Common Subsequence.

        :return: A sequence representing the LCS
        """
        if self.lcs_matrix is None:
            self.compute()

        lcs = []
        i, j = len(self.sequence_a), len(self.sequence_b)

        while i > 0 and j > 0:
            if self.sequence_a[i - 1] == self.sequence_b[j - 1]:
                lcs.append(self.sequence_a[i - 1])
                i -= 1
                j -= 1
            elif self.lcs_matrix[i - 1][j] >= self.lcs_matrix[i][j - 1]:
                i -= 1
            else:
                j -= 1

        return ''.join(reversed(lcs)) if isinstance(self.sequence_a, str) else list(reversed(lcs))

    def lcss_distance(self):
        """
        Compute the LCSS distance, which is the difference between the length of the sequences and the LCS length.

        :return: The LCSS distance
        """
        lcs_length = self.compute()
        return max(len(self.sequence_a), len(self.sequence_b)) - lcs_length

class Frechet(Distance):

    def __init__(self):
        """
        Initialize the FrechetDistance with two curves.

        :param curve_a: First curve, a list of tuples representing points (e.g., [(x1, y1), (x2, y2), ...])
        :param curve_b: Second curve, a list of tuples representing points (e.g., [(x1, y1), (x2, y2), ...])
        """
        super().__init__()

    def _c(self, i, j):
        """
        Internal method to compute the discrete Fréchet distance using dynamic programming.

        :param i: Index in curve_a
        :param j: Index in curve_b
        :return: Fréchet distance between curve_a[0..i] and curve_b[0..j]
        """
        if self.ca[i][j] > -1:
            return self.ca[i][j]
        elif i == 0 and j == 0:
            self.ca[i][j] = Euclidean().calculate(self.curve_a[0], self.curve_b[0])
        elif i > 0 and j == 0:
            self.ca[i][j] = max(self._c(i - 1, 0), Euclidean().calculate(self.curve_a[i], self.curve_b[0]))
        elif i == 0 and j > 0:
            self.ca[i][j] = max(self._c(0, j - 1), Euclidean().calculate(self.curve_a[0], self.curve_b[j]))
        elif i > 0 and j > 0:
            self.ca[i][j] = max(
                min(self._c(i - 1, j), self._c(i - 1, j - 1), self._c(i, j - 1)),
                Euclidean().calculate(self.curve_a[i], self.curve_b[j])
            )
        else:
            self.ca[i][j] = float('inf')
        return self.ca[i][j]

    def distance_function(self, curve_a, curve_b):
        """
        Compute the Fréchet distance between the two curves.

        :return: The Fréchet distance between curve_a and curve_b
        """
        self.curve_a = curve_a
        self.curve_b = curve_b
        self.ca = [[-1 for _ in range(len(curve_b))] for _ in range(len(curve_a))]
        
        return self._c(len(self.curve_a) - 1, len(self.curve_b) - 1)


