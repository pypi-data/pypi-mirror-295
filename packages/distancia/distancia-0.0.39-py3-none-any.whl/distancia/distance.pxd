cdef class Distance:
	pass

# Declaration for the Levenshtein class in Cython
cdef class Euclidean:
	# Declare the distance_function method with types for inputs and outputs
	cpdef float compute(self,list[float] point1, list[float] point2) except *
	# Declare the exemple method (no return value)
	cpdef void exemple(self)
    
# Declaration for the Levenshtein class in Cython
cdef class Levenshtein:
	# Declare the distance_function method with types for inputs and outputs
	cpdef int compute(self, str s1, str s2)except *
	# Declare the exemple method (no return value)
	cpdef void exemple(self)

cdef class Hamming:
	# Declare the distance_function method with types for inputs and outputs
	cpdef int compute(self, str s1, str s2)
	# Declare the exemple method (no return value)
	cpdef void exemple(self)

cdef class InverseTanimoto:
	cpdef double compute(self, set set_a, set set_b)

cdef class Manhattan:
	cpdef double compute(self, list[float] point1, list[float] point2)

cdef class Minkowski:
	cpdef double compute(self, list[float] point1, list[float] point2)
	cpdef void exemple(self)

cdef class Mahalanobis:
	cpdef double mean(self, list[list[float]] data)
	cpdef double covariance_matrix(self, list[list[float]] data,float mean)
	cpdef list[list[float]] matrix_inverse(self, list[list[float]] matrix)
	cpdef double compute(self, list[float] point, list[list[float]] data)
	cpdef void exemple(self)

cdef class RussellRao:
	cpdef double compute(self, list[int] vector1, list[int]vector2)
	cpdef void exemple(self)

cdef class Chebyshev:
	cpdef double compute(self, list[float] point1, list[loat]point2)
	cpdef void exemple(self)

cdef class Jaro:
	cpdef double compute(self, str s1, str s2)
	cpdef void exemple(self)

cdef class SorensenDice:
	cpdef double compute(self, str s1, str s2)
	cpdef void exemple(self)

cdef class JaroWinkler:
	cpdef double compute(self, str s1, str s2,float p)
	cpdef void exemple(self)

cdef class Hausdorff:
	cpdef double compute(self, set set_a, set set_b)
	cpdef void exemple(self)

cdef class KendallTau:
	cpdef double compute(self, list[int] permutation1, list[int] permutation1)
	cpdef void exemple(self)

cdef class Haversine:
	cpdef double compute(self, list[float] p1, list[loat]p2)
	cpdef void exemple(self)

cdef class Canberra:
	cpdef double compute(self, list[float] point1, list[loat]point2)
	cpdef void exemple(self)

cdef class BrayCurtis:
	cpdef double compute(self, list[float] point1, list[loat]point2)
	cpdef void exemple(self)

cdef class Matching:
	cpdef int compute(self, str seq1, str seq2)
	cpdef void exemple(self)

cdef class Kulsinski:
	cpdef double compute(self, set set_a, set set_b)
	cpdef void exemple(self)

cdef class DamerauLevenshtein:
	cpdef int compute(self, str s1, str s2)
	cpdef void exemple(self)

cdef class Yule:
	cpdef double compute(self, list[int] binary_vector1, list[int]binary_vector2)
	cpdef void exemple(self)

cdef class Bhattacharyya:
	cpdef double compute(self, list[float] P, list[float]Q)
	cpdef void exemple(self)

cdef class Gower:
	cpdef double compute(self, list vec1, list vec2)
	cpdef void exemple(self)

cdef class Hellinger:
	cpdef double compute(self, list[float] p, list[float]q)
	cpdef void exemple(self)

cdef class CzekanowskiDice:
	cpdef double compute(self, list[float] x, list[float]y)
	cpdef void exemple(self)

cdef class Wasserstein:
	cpdef double compute(self, list[float] distribution1, list[float]distribution2)
	cpdef array double _cumulative_distribution(list[float] distribution)
	cpdef void exemple(self)

cdef class FagerMcGowan:
	cpdef double compute(self, set set_a, set set_b, int N)
	cpdef void exemple(self)


