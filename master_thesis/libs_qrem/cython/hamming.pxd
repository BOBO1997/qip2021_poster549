import cython
cimport cython

from libcpp.map import map
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.set cimport set

cdef extern from "../libcpp/hamming.hpp" namespace "libs_qrem":
    cdef void print_vec1d()
    cdef set[string] extend_keys(set[string] original_keys, int max_dist)
    cdef vector[double] extended_vectors(map[string, double] y, map[string, int] keys_to_indices)