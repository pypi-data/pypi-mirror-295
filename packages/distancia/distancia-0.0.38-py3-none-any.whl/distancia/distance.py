
from .mainClass import *
from .tools     import *

def euclid(point1, point2):
	if len(point1) != len(point2):
			raise ValueError("Points must have the same dimensions")
	distance = 0.0
	for p1, p2 in zip(point1, point2):
		distance += (p1 - p2) ** 2
	return distance**0.5

class Levenshtein(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,s1: str, s2: str) -> int:
		
		dp = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]

		for i in range(len(s1) + 1):
			dp[i][0] = i
		for j in range(len(s2) + 1):
			dp[0][j] = j

		for i in range(1, len(s1) + 1):
			for j in range(1, len(s2) + 1):
				if s1[i - 1] == s2[j - 1]:
					cost = 0
				else:
					cost = 1
				dp[i][j] = min(dp[i - 1][j] + 1,        # Suppression
                           dp[i][j - 1] + 1,        # Insertion
                           dp[i - 1][j - 1] + cost) # Substitution

		return dp[len(s1)][len(s2)]
		
	def exemple(self):
		self.obj1_exemple = "kitten"
		self.obj2_exemple = "sitting"
		super().exemple()


class Euclidean(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,point1: list[float], point2: list[float]) -> float:
		# def distance_function(self,point1, point2):
		"""
		Calculate the Euclidean distance between two points.
    
		:param point1: First point as a list of coordinates
		:param point2: Second point as a list of coordinates
		:return: Euclidean distance between point1 and point2
		"""
		distance: float = 0.0
		for p1, p2 in zip(point1, point2):
			distance += (p1 - p2) ** 2
		return distance**0.5
		
class L2(Euclidean):
	def __init__(self):
		super().__init__()

class Hamming(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,s1: str, s2: str) -> int:
		"""
		Calculate the Hamming distance between two strings.
    
		:param str1: First string
		:param str2: Second string
		:return: Hamming distance between str1 and str2
		:raises ValueError: If the strings are not of the same length
		"""
		if len(str1) != len(str2):
			raise ValueError("Strings must be of the same length")
    
		return sum(el1 != el2 for el1, el2 in zip(str1, str2))
		
	def exemple(self):
		self.obj1_exemple = "1011101"
		self.obj2_exemple = "1001001"
		super().exemple()

class InverseTanimoto(Distance):
	
	def __init__(self):
		super().__init__()

	def distance_function(self, set_a, set_b):
		"""
		Calculate the Inverse Tanimoto coefficient between two sets.

		Parameters:
		- set_a: First set of elements.
		- set_b: Second set of elements.

		Returns:
		- Inverse Tanimoto coefficient: A float value representing the dissimilarity between the two sets.
		"""
		if not isinstance(set_a, set) or not isinstance(set_b, set):
			raise ValueError("Inputs must be of type 'set'.")

		# Calculate the intersection and union of the two sets
		intersection = set_a.intersection(set_b)
		union = set_a.union(set_b)

		# Handle the edge case where the union is empty
		if not union:
			return 0.0

		# Calculate the Inverse Tanimoto coefficient
		inverse_tanimoto = (len(union) - len(intersection)) / len(union)

		return inverse_tanimoto


class Manhattan(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,point1, point2):
		"""
		Calculate the Manhattan distance, taxicab or L1 between two points.
    
		:param point1: First point as a list of coordinates
		:param point2: Second point as a list of coordinates
		:return: Manhattan distance between point1 and point2
		:raises ValueError: If the points are not of the same dimension
		"""
		if len(point1) != len(point2):
			raise ValueError("Points must have the same dimensions")
    
		distance = sum(abs(p1 - p2) for p1, p2 in zip(point1, point2))
		return distance
		
class L1(Manhattan):
	def __init__(self):
		super().__init__()

class Minkowski(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,point1, point2, p):
		"""
		Calculate the Minkowski distance between two points.
    
		:param point1: First point as a list of coordinates
		:param point2: Second point as a list of coordinates
		:param p: The order of the Minkowski distance
		:return: Minkowski distance between point1 and point2
		:raises ValueError: If the points are not of the same dimension
		"""
		if len(point1) != len(point2):
			raise ValueError("Points must have the same dimensions")
    
		distance = sum(abs(p1 - p2) ** p for p1, p2 in zip(point1, point2)) ** (1 / p)
		return distance
	def exemple(self,p):
		self.obj3_exemple = p
		super().exemple()


class Mahalanobis(Distance):
	
	def __init__(self):
		super().__init__()
		
	def mean(self,data):
		"""
		Calculate the mean of each dimension in the dataset.
    
		:param data: A dataset as a list of points (list of lists)
		:return: Mean of each dimension as a list
		"""
		n = len(data)
		d = len(data[0])
		mean = [0] * d
    
		for point in data:
			for i in range(d):
				mean[i] += point[i]
    
		mean = [x / n for x in mean]
		return mean

	def covariance_matrix(self,data, mean):
		"""
		Calculate the covariance matrix of the dataset.
    
		:param data: A dataset as a list of points (list of lists)
		:param mean: Mean of each dimension as a list
		:return: Covariance matrix as a list of lists
		"""
		n = len(data)
		d = len(data[0])
		cov_matrix = [[0] * d for _ in range(d)]
    
		for point in data:
			diff = [point[i] - mean[i] for i in range(d)]
			for i in range(d):
				for j in range(d):
					cov_matrix[i][j] += diff[i] * diff[j]
    
		cov_matrix = [[x / (n - 1) for x in row] for row in cov_matrix]
		return cov_matrix

	def matrix_inverse(self,matrix):
		"""
		Calculate the inverse of a matrix using Gauss-Jordan elimination.
    
		:param matrix: A square matrix as a list of lists
		:return: Inverse of the matrix as a list of lists
		"""
		n = len(matrix)
		identity = [[float(i == j) for i in range(n)] for j in range(n)]
		augmented = [row + identity_row for row, identity_row in zip(matrix, identity)]
		for i in range(n):
			pivot = augmented[i][i]
			for j in range(2 * n):
				augmented[i][j] /= pivot
			for k in range(n):
				if k != i:
					factor = augmented[k][i]
					for j in range(2 * n):
						augmented[k][j] -= factor * augmented[i][j]
    
		inverse = [row[n:] for row in augmented]
		return inverse

	def distance_function(self,point, data):
		"""
		Calculate the Mahalanobis distance between a point and a dataset.
    
		:param point: A point as a list of coordinates
		:param data: A dataset as a list of points (list of lists)
		:return: Mahalanobis distance between the point and the dataset
		:raises ValueError: If the point dimensions do not match the dataset dimensions
		! lever une execption si la matrice est singulière
		"""
		if len(data[0]) != len(point):
			raise ValueError("Point dimensions must match dataset dimensions")
    
		mean_data = self.mean(data)
		cov_matrix = self.covariance_matrix(data, mean_data)
		cov_matrix_inv = self.matrix_inverse(cov_matrix)
    
		diff = [point[i] - mean_data[i] for i in range(len(point))]
    
		# Matrix multiplication: diff^T * cov_matrix_inv * diff
		result = 0
		for i in range(len(diff)):
			for j in range(len(diff)):
				result += diff[i] * cov_matrix_inv[i][j] * diff[j]
    
		return result**0.5
	def exemple(self):
		self.obj2_exemple = [
    [2, 1, 0],
    [2, 3, 4],
    [3, 4, 5],
    [4, 5, 6],
]
		super().exemple()

class RussellRao(Distance):
    def __init__(self, ):
        """
        Initialize the Russell-Rao class with two binary vectors.

        :param vector1: First binary vector for comparison.
        :param vector2: Second binary vector for comparison.
        """
        super().__init__()
        
        

    def distance_function(self,vector1, vector2):
        """
        Calculate the Russell-Rao distance between the two binary vectors.

        :return: The Russell-Rao distance as a float.
        """
        if len(vector1) != len(vector2):
            raise ValueError("Vectors must be of the same length")
        # Calculate the number of matching features (both present)
        a = sum(v1 and v2 for v1, v2 in zip(vector1, vector2))

        # Calculate the total number of features
        n = len(vector1)

        # Calculate the Russell-Rao distance
        distance = a / n

        return distance
        
class Chebyshev(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,point1, point2):

		"""
		Calculate the Chebyshev distance between two points.
    
		:param point1: A list of coordinates for the first point
		:param point2: A list of coordinates for the second point
		:return: Chebyshev distance between the two points
		:raises ValueError: If the points do not have the same dimensions
		"""
		if len(point1) != len(point2):
			raise ValueError("Points must have the same dimensions")
    
		return max(abs(a - b) for a, b in zip(point1, point2))


class RatcliffObershelp(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,str1, str2):
		"""
		ou Similarité Gestalt.
		Calculate the Ratcliff/Obershelp distance between two strings.
    
		:param str1: The first string
		:param str2: The second string
		:return: Ratcliff/Obershelp distance between the two strings
		"""
		def find_longest_common_substring(s1, s2):
			"""
			Helper function to find the longest common substring between two strings.
        
			:param s1: The first string
			:param s2: The second string
			:return: The longest common substring
			"""
			matrix = [[0] * (len(s2) + 1) for _ in range(len(s1) + 1)]
			longest_length = 0
			lcs_end = 0

			for i in range(1, len(s1) + 1):
				for j in range(1, len(s2) + 1):
					if s1[i - 1] == s2[j - 1]:
						matrix[i][j] = matrix[i - 1][j - 1] + 1
						if matrix[i][j] > longest_length:
							longest_length = matrix[i][j]
							lcs_end = i

			return s1[lcs_end - longest_length: lcs_end]

		def recursive_match(s1, s2):
			"""
			Helper function to recursively match substrings.
        
			:param s1: The first string
			:param s2: The second string
			:return: The total length of matched substrings
			"""
			lcs = find_longest_common_substring(s1, s2)
			if not lcs:
				return 0

			lcs_length = len(lcs)
			lcs_start1 = s1.find(lcs)
			lcs_start2 = s2.find(lcs)

			return (
				lcs_length +
				recursive_match(s1[:lcs_start1], s2[:lcs_start2]) +
				recursive_match(s1[lcs_start1 + lcs_length:], s2[lcs_start2 + lcs_length:])
			)

		total_length = len(str1) + len(str2)
		if total_length == 0:
			return 0.0

		matched_length = recursive_match(str1, str2)
		similarity = (2 * matched_length) / total_length

		return 1 - similarity
		
	def exemple(self):
		self.obj1_exemple = "kitten"
		self.obj2_exemple = "sitting"
		super().exemple()

'''
class RatcliffObershelp:
    def __init__(self):
        """
        Initialize the Ratcliff/Obershelp class with two strings.

        :param string1: First string for comparison.
        :param string2: Second string for comparison.
        """
        self.string1 = string1
        self.string2 = string2

    def distance_function(self, string1, string2):
        """
        Calculate the Ratcliff/Obershelp distance between the two strings.

        :return: The Ratcliff/Obershelp distance as a float.
        """
        def ratcliff_obershelp(s1, s2):
            if not s1 or not s2:
                return 0.0 if s1 != s2 else 1.0

            def lcs(s1, s2):
                m, n = len(s1), len(s2)
                dp = [[0] * (n + 1) for _ in range(m + 1)]

                for i in range(1, m + 1):
                    for j in range(1, n + 1):
                        if s1[i - 1] == s2[j - 1]:
                            dp[i][j] = dp[i - 1][j - 1] + 1
                        else:
                            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

                return dp[m][n]

            lcs_length = lcs(s1, s2)
            if lcs_length == 0:
                return 0.0

            prefix_length = 0
            while prefix_length < len(s1) and prefix_length < len(s2) and s1[prefix_length] == s2[prefix_length]:
                prefix_length += 1

            similarity = 2 * lcs_length / (len(s1) + len(s2))
            similarity += (2 * prefix_length) / (len(s1) + len(s2))
            return similarity

        similarity = ratcliff_obershelp(self.string1, self.string2)
        return 1 - similarity
'''
class Jaro(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,s1, s2):
		"""
		Calculate the Jaro similarity between two strings.
    
		:param s1: The first string
		:param s2: The second string
		:return: Jaro similarity between the two strings
		"""
		if s1 == s2:
			return 1.0

		len_s1 = len(s1)
		len_s2 = len(s2)

		if len_s1 == 0 or len_s2 == 0:
			return 0.0

		match_distance = max(len_s1, len_s2) // 2 - 1

		s1_matches = [False] * len_s1
		s2_matches = [False] * len_s2

		matches = 0
		transpositions = 0

		for i in range(len_s1):
			start = max(0, i - match_distance)
			end = min(i + match_distance + 1, len_s2)

			for j in range(start, end):
				if s2_matches[j]:
					continue
				if s1[i] != s2[j]:
					continue
				s1_matches[i] = True
				s2_matches[j] = True
				matches += 1
				break

		if matches == 0:
			return 0.0

		k = 0
		for i in range(len_s1):
			if not s1_matches[i]:
				continue
			while not s2_matches[k]:
				k += 1
			if s1[i] != s2[k]:
				transpositions += 1
			k += 1

		return (matches / len_s1 + matches / len_s2 + (matches - transpositions // 2) / matches) / 3.0
		
	def exemple(self):
		self.obj1_exemple = "martha"
		self.obj2_exemple = "marhta"
		super().exemple()

class SorensenDice(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,str1, str2):
		# Convert strings to sets of bigrams
		bigrams1 = {str1[i:i+2] for i in range(len(str1) - 1)}
		bigrams2 = {str2[i:i+2] for i in range(len(str2) - 1)}
    
		# Calculate the intersection and the sizes of the sets
		intersection = len(bigrams1 & bigrams2)
		size1 = len(bigrams1)
		size2 = len(bigrams2)
    
		# Calculate the Sørensen-Dice coefficient
		sorensen_dice_coeff = 2 * intersection / (size1 + size2)
    
		# The distance is 1 minus the coefficient
		distance = 1 - sorensen_dice_coeff
    
		return distance
		
	def exemple(self):
		self.obj1_exemple = "night"
		self.obj2_exemple = "nacht"

		super().exemple()
		
class JaroWinkler(Distance):
	
	def __init__(self):
		super().__init__()

	def distance_function(self,s1, s2, p=0.1):
		"""
		Calculate the Jaro-Winkler distance between two strings.
    
		:param s1: The first string
		:param s2: The second string
		:param p: The scaling factor, usually 0.1
		:return: Jaro-Winkler distance between the two strings
		"""
		jaro_sim = Jaro().calculate(s1, s2)

		prefix_length = 0
		max_prefix_length = 4

		for i in range(min(len(s1), len(s2))):
			if s1[i] == s2[i]:
				prefix_length += 1
			else:
				break
			if prefix_length == max_prefix_length:
				break

		jaro_winkler_sim = jaro_sim + (prefix_length * p * (1 - jaro_sim))
		return jaro_winkler_sim
		
	def exemple(self):
		self.obj1_exemple = "martha"
		self.obj2_exemple = "marhta"
		super().exemple()

class Hausdorff(Distance):
	
	def __init__(self):
		super().__init__()

	def distance_function(self,set1, set2):
		"""
		Calculate the Hausdorff distance between two sets of points.
    
		:param set1: The first set of points, each point represented as a tuple (x, y)
		:param set2: The second set of points, each point represented as a tuple (x, y)
		:return: Hausdorff distance between the two sets of points
		"""
		def max_min_distance(set_a, set_b):
			"""
			Helper function to find the maximum of the minimum distances from each point in set_a to the closest point in set_b.
        
			:param set_a: The first set of points
			:param set_b: The second set of points
			:return: Maximum of the minimum distances
			"""
			max_min_dist = 0
			for point_a in set_a:
				min_dist = float('inf')
				for point_b in set_b:
					dist = Euclidean().calculate(point_a, point_b)
					if dist < min_dist:
						min_dist = dist
				if min_dist > max_min_dist:
					max_min_dist = min_dist
			return max_min_dist

		return max(max_min_distance(set1, set2), max_min_distance(set2, set1))
		
	def exemple(self):
		self.obj1_exemple = [(0, 0), (0, 1), (1, 0), (1, 1)]
		self.obj2_exemple = [(2, 2), (2, 3), (3, 2), (3, 3)]
		super().exemple()


class KendallTau(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,permutation1, permutation2):
		"""
		Calculate the Kendall Tau distance between two permutations.
    
		:param permutation1: The first permutation (a list of integers)
		:param permutation2: The second permutation (a list of integers)
		:return: Kendall Tau distance between the two permutations
		"""
		assert len(permutation1) == len(permutation2), "Permutations must be of the same length"
    
		n = len(permutation1)
		pairs = [(permutation1[i], permutation2[i]) for i in range(n)]
    
		def count_inversions(pairs):
			"""
			Helper function to count inversions in a list of pairs.
        
			:param pairs: List of pairs
			:return: Number of inversions
			"""
			inversions = 0
			for i in range(len(pairs)):
				for j in range(i + 1, len(pairs)):
					if (pairs[i][0] > pairs[j][0] and pairs[i][1] < pairs[j][1]) or (pairs[i][0] < pairs[j][0] and pairs[i][1] > pairs[j][1]):
						inversions += 1
			return inversions

		return count_inversions(pairs)
		
	def exemple(self):
		self.obj1_exemple = [1, 2, 3, 4]
		self.obj2_exemple = [4, 3, 2, 1]
		super().exemple()



class Haversine(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,p1,p2 ):
		"""
		Calculate the Haversine distance between two points on the Earth's surface.
    
		:param lat1: Latitude of the first point in decimal degrees
		:param lon1: Longitude of the first point in decimal degrees
		:param lat2: Latitude of the second point in decimal degrees
		:param lon2: Longitude of the second point in decimal degrees
		:return: Haversine distance between the two points in kilometers
		"""
		lat1, lon1=p1[0],p1[1]
		lat2, lon2=p2[0],p2[1]
		# Radius of the Earth in kilometers
		R = 6371.0
    
		# Convert latitude and longitude from degrees to radians
		lat1_rad = degrees_to_radians(lat1)
		lon1_rad = degrees_to_radians(lon1)
		lat2_rad = degrees_to_radians(lat2)
		lon2_rad = degrees_to_radians(lon2)
    
		# Differences in coordinates
		dlat = lat2_rad - lat1_rad
		dlon = lon2_rad - lon1_rad
    
		# Haversine formula
		a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
		c = 2 * atan2(a**0.5, (1 - a)**0.5)
    
		# Distance in kilometers
		distance = R * c
    
		return distance
		
	def exemple(self):
		self.obj1_exemple = (48.8566, 2.3522)# Paris coordinates
		self.obj2_exemple = (51.5074, -0.1278)# London coordinates
		super().exemple()

class Canberra(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,point1, point2):
		"""
		Calculate the Canberra distance between two points.
    
		:param point1: The first point (a list of numerical values)
		:param point2: The second point (a list of numerical values)
		:return: Canberra distance between the two points
		"""
		assert len(point1) == len(point2), "Points must be of the same dimension"
    
		distance = 0
		for x1, x2 in zip(point1, point2):
			numerator = abs(x1 - x2)
			denominator = abs(x1) + abs(x2)
			if denominator != 0:
				distance += numerator / denominator
    
		return distance

class BrayCurtis(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,point1, point2):
		"""
		Calculate the Bray-Curtis distance between two points.
    
		:param point1: The first point (a list of numerical values)
		:param point2: The second point (a list of numerical values)
		:return: Bray-Curtis distance between the two points
		"""
		assert len(point1) == len(point2), "Points must be of the same dimension"
    
		sum_diff = 0
		sum_sum = 0
    
		for x1, x2 in zip(point1, point2):
			sum_diff += abs(x1 - x2)
			sum_sum += abs(x1 + x2)
    
		if sum_sum == 0:
			return 0  # To handle the case when both points are zeros
    
		distance = sum_diff / sum_sum
		return distance


class Matching(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,seq1, seq2):
		"""
		Calculate the Matching (Hamming) distance between two sequences.
    
		:param seq1: The first sequence (a list or string of characters or binary values)
		:param seq2: The second sequence (a list or string of characters or binary values)
		:return: Matching distance between the two sequences
		"""
		assert len(seq1) == len(seq2), "Sequences must be of the same length"
    
		distance = sum(el1 != el2 for el1, el2 in zip(seq1, seq2))
    
		return distance
		
	def exemple(self):
		self.obj1_exemple = [1, 0, 1, 1, 0]
		self.obj2_exemple = [0, 1, 1, 0, 0]

		super().exemple()



class Kulsinski(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,set1, set2):
		"""
		Calculate the Kulsinski distance between two sets or binary vectors.
    
		:param set1: The first set (a set of elements or a list of binary values)
		:param set2: The second set (a set of elements or a list of binary values)
		:return: Kulsinski distance between the two sets or binary vectors
		"""
		if isinstance(set1, set) and isinstance(set2, set):
			# Calculate for sets
			intersection = len(set1.intersection(set2))
			union = len(set1.union(set2))
			a = intersection
			b = len(set1) - intersection
			c = len(set2) - intersection
			d = union - a - b - c
		elif isinstance(set1, list) and isinstance(set2, list) and len(set1) == len(set2):
			# Calculate for binary vectors
			a = sum(1 for x, y in zip(set1, set2) if x == 1 and y == 1)
			b = sum(1 for x, y in zip(set1, set2) if x == 1 and y == 0)
			c = sum(1 for x, y in zip(set1, set2) if x == 0 and y == 1)
			d = sum(1 for x, y in zip(set1, set2) if x == 0 and y == 0)
		else:
			raise ValueError("Input must be two sets or two binary vectors of the same length")

		n = a + b + c + d
    
		return (b + c - a + n) / (b + c + n)
		
	def exemple(self):
		self.obj1_exemple = {"a", "b", "c", "d"}
		self.obj2_exemple = {"b", "c", "e", "f"}

		super().exemple()

class DamerauLevenshtein(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,s1, s2):
		d = {}
		lenstr1 = len(s1)
		lenstr2 = len(s2)

		for i in range(-1, lenstr1 + 1):
			d[(i, -1)] = i + 1
		for j in range(-1, lenstr2 + 1):
			d[(-1, j)] = j + 1

		for i in range(lenstr1):
			for j in range(lenstr2):
				cost = 0 if s1[i] == s2[j] else 1
				d[(i, j)] = min(
					d[(i - 1, j)] + 1,  # suppresion
					d[(i, j - 1)] + 1,  # insertion
					d[(i - 1, j - 1)] + cost,  # substitution
				)
				if i > 0 and j > 0 and s1[i] == s2[j - 1] and s1[i - 1] == s2[j]:
					d[(i, j)] = min(d[(i, j)], d[(i - 2, j - 2)] + cost)  # transposition

		return d[lenstr1 - 1, lenstr2 - 1]
		
	def exemple(self):
		self.obj1_exemple = "ca"
		self.obj2_exemple = "abc"

		super().exemple()


class Yule(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,binary_vector1, binary_vector2):
		"""
		Calcule la distance de Yule entre deux vecteurs binaires.
    
		:param binary_vector1: Premier vecteur binaire (liste de 0 et 1)
		:param binary_vector2: Deuxième vecteur binaire (liste de 0 et 1)
		:return: Distance de Yule
		"""
		if len(binary_vector1) != len(binary_vector2):
			raise ValueError("Les vecteurs binaires doivent avoir la même longueur.")
    
		# Calcul des variables a, b, c, d
		a = b = c = d = 0
    
		for bit1, bit2 in zip(binary_vector1, binary_vector2):
			if bit1 == 1 and bit2 == 1:
				a += 1
			elif bit1 == 1 and bit2 == 0:
				b += 1
			elif bit1 == 0 and bit2 == 1:
				c += 1
			elif bit1 == 0 and bit2 == 0:
				d += 1
    
		# Calcul de l'indice de dissimilarité de Yule Q
		if (a * d + b * c) == 0:
			return 0.0  # Si le dénominateur est 0, la dissimilarité est 0 (vecteurs identiques)
    
		Q = 2 * b * c / (a * d + b * c)
        
		return Q / (Q + 2 * a * d)
		
	def exemple(self):
		self.obj1_exemple =  [1, 0, 1, 1, 0, 1, 0, 0, 1, 1]
		self.obj2_exemple = [0, 1, 1, 0, 0, 1, 0, 1, 1, 0]
		super().exemple()



class Bhattacharyya(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,P, Q):
		"""
		Calcule la distance de Bhattacharyya entre deux distributions de probabilité discrètes.
    
		:param P: Première distribution de probabilité (liste de probabilités)
		:param Q: Deuxième distribution de probabilité (liste de probabilités)
		:return: Distance de Bhattacharyya
		"""
		if len(P) != len(Q):
			raise ValueError("Les distributions doivent avoir la même longueur.")
    
		# Calcul du coefficient de Bhattacharyya
		bc = 0.0
		for p, q in zip(P, Q):
			bc += (p * q)**0.5
    
		# Calcul de la distance de Bhattacharyya
		distance = -log(bc)
    
		return distance
		
	def exemple(self):
		self.obj1_exemple =  [0.1, 0.2, 0.4, 0.3]
		self.obj2_exemple = [0.2, 0.3, 0.1, 0.4]
		super().exemple()


class Gower(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self, vec1, vec2, ranges):
		"""
		Calculate the Gower similarity between two vectors.

		Parameters:
		- vec1: List of values for the first entity (can include both numerical and categorical).
		- vec2: List of values for the second entity (can include both numerical and categorical).
		- ranges: List of ranges for numerical variables. Use `None` for categorical variables.

		Returns:
		- Similarity: Gower similarity between vec1 and vec2.
		"""
		if len(vec1) != len(vec2) or len(vec1) != len(ranges):
			raise ValueError("Vectors and ranges must have the same length.")

		total_similarity = 0
		num_variables = len(vec1)

		for i in range(num_variables):
			if ranges[i] is None:
				# Categorical variable
				if vec1[i] == vec2[i]:
					similarity = 1
				else:
				    similarity = 0
			else:
				# Numerical variable
				if vec1[i] == vec2[i]:
					similarity = 1
				else:
					range_value = ranges[i]
					if range_value == 0:
						similarity = 0
					else:
						similarity = 1 - abs(vec1[i] - vec2[i]) / range_value

			total_similarity += similarity

		# Normalize by the number of variables
		return total_similarity / num_variables
		
	def exemple(self):
		test_cases = [
			(["Red", 3.2, 5], ["Blue", 4.1, 3], [None, 5.0, 10]),
			([5.5, "M", 200], [6.1, "F", 180], [10, None, 50]),
			([0, "High", 10], [1, "Low", 10], [1, None, 10]),
			([100, "Yes", 3.5], [150, "No", 2.8], [50, None, 5]),
			([1.5, "Green", 2], [1.5, "Green", 2], [None, None, None])
		]

		# Compute and print the Gower similarity for each pair
		for vec1, vec2, ranges in test_cases:
			similarity = gower.calculate(vec1, vec2, ranges)
			print(f"Gower similarity between {vec1} and {vec2}: {similarity:.4f}")

class Hellinger(Distance):
	
	def __init__(self):
		super().__init__()

	def distance_function(self,p, q):
		"""
		Calcule la distance de Hellinger entre deux distributions de probabilités.
    
		:param p: Première distribution de probabilités (sous forme de liste ou d'array).
		:param q: Deuxième distribution de probabilités (sous forme de liste ou d'array).
		:return: Distance de Hellinger entre p et q.
		"""
		if len(p) != len(q):
			raise ValueError("Les distributions doivent avoir la même longueur.")
    
		# Calculer la distance de Hellinger
		sum_of_squares = sum(((p_i)**0.5 - (q_i)**0.5 ) ** 2 for p_i, q_i in zip(p, q))
    
		return (1 / 2**0.5 ) * sum_of_squares**0.5
		
	def exemple(self):
		self.obj1_exemple = [0.1, 0.4, 0.5]
		self.obj2_exemple = [0.2, 0.3, 0.5]
		super().exemple()

class CzekanowskiDice(Distance):
	
	def __init__(self):
		super().__init__()
		
	def distance_function(self,x, y):
		"""
		Calcule la distance Czekanowski-Dice entre deux vecteurs.
    
		:param x: Premier vecteur (sous forme de liste ou d'array).
		:param y: Deuxième vecteur (sous forme de liste ou d'array).
		:return: Distance Czekanowski-Dice entre x et y.
		"""
		if len(x) != len(y):
			raise ValueError("Les vecteurs doivent avoir la même longueur.")
    
		min_sum = sum(min(x_i, y_i) for x_i, y_i in zip(x, y))
		sum_x = sum(x)
		sum_y = sum(y)
    
		if sum_x + sum_y == 0:
			return 0.0  # Pour éviter la division par zéro
    
		dice_similarity = (2 * min_sum) / (sum_x + sum_y)
    
		return 1 - dice_similarity
		
	def exemple(self):
		self.obj1_exemple = [1, 2, 3, 4]
		self.obj2_exemple = [2, 2, 3, 5]
		super().exemple()

class Wasserstein(Distance):
	
    def __init__(self):
        """
        Initialize the Wasserstein class with two probability distributions.

        :param distribution1: First probability distribution (list of floats).
        :param distribution2: Second probability distribution (list of floats).
        """
        super().__init__()


    def distance_function(self, distribution1, distribution2):
        """
        Calculate the Wasserstein distance between the two distributions.

        :return: The Wasserstein distance as a float.
        """
        if len(distribution1) != len(distribution2):
            raise ValueError("Distributions must have the same length.")
        
    
        # Cumulative distribution functions (CDF) of both distributions
        cdf1 = self._cumulative_distribution(distribution1)
        cdf2 = self._cumulative_distribution(distribution2)

        # Wasserstein distance is the area between the CDFs
        distance = sum(abs(c1 - c2) for c1, c2 in zip(cdf1, cdf2))

        return distance

    def _cumulative_distribution(self, distribution):
        """
        Calculate the cumulative distribution for a given distribution.

        :param distribution: A probability distribution (list of floats).
        :return: The cumulative distribution (list of floats).
        """
        cdf = []
        cumulative_sum = 0.0
        for prob in distribution:
            cumulative_sum += prob
            cdf.append(cumulative_sum)
        return cdf

class FagerMcGowan(Distance):
	
    def __init__(self):
        super().__init__()
    """
    FagerMcGowan similarity coefficient calculator.

    The FagerMcGowan similarity coefficient is used to measure the similarity 
    between two sets, particularly in ecological studies. It adjusts for the 
    expected overlap due to random chance, providing a more accurate reflection 
    of true similarity.

    Methods:
    --------
    calculate(set1, set2, N):
        Calculates the FagerMcGowan similarity coefficient between two sets.
    """

    def distance_function(self, set1, set2, N):
        """
        Calculate the Fager-McGowan similarity coefficient between two sets.

        Parameters:
        -----------
        set1 : set
            The first set of elements (e.g., species in a habitat).
        set2 : set
            The second set of elements.
        N : int
            The total number of unique elements in the universal set.

        Returns:
        --------
        float
            The Fager-McGowan similarity coefficient.
        """
        intersection_size = len(set1 & set2)  # Number of elements common to both sets
        set1_size = len(set1)  # Size of the first set
        set2_size = len(set2)  # Size of the second set

        # Calculate the Fager-McGowan similarity coefficient
        numerator = intersection_size - (set1_size * set2_size / N)
        denominator = min(set1_size, set2_size)

        if denominator == 0:
            return 0.0

        similarity = numerator / denominator
        return similarity

