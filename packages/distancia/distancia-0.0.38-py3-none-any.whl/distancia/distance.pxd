cdef class Distance:
    pass

# Declaration for the Levenshtein class in Cython

cdef class Euclidean:

    # Declare the distance_function method with types for inputs and outputs
    cpdef float distance_function(self,list[float] point1, list[float] point2) except *

    # Declare the exemple method (no return value)
    cpdef void exemple(self)
    
# Declaration for the Levenshtein class in Cython

cdef class Levenshtein:

    # Declare the distance_function method with types for inputs and outputs
    cpdef int distance_function(self, str s1, str s2)except *

    # Declare the exemple method (no return value)
    cpdef void exemple(self)

cdef class Hamming:

    # Declare the distance_function method with types for inputs and outputs
    cpdef int distance_function(self, str s1, str s2)except *

    # Declare the exemple method (no return value)
    cpdef void exemple(self)
