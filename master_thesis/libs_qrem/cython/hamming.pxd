import cython
cimport cython

from libcpp.map import map
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.set cimport set

cdef extern from "../libcpp/hamming.hpp" namespace "libs_qrem":
    cdef set[string] extend_keys(set[string] original_keys, int max_dist)