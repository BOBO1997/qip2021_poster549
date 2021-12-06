import cython
cimport cython

from libcpp.map import map
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.set cimport set

cdef void print_vec2d(vector[vector[int]] vec2d):
    for vec1d in vec2d:
        for elem in vec1d:
            print(elem)
        print()

cdef void print_set_of_string(set[string] s):
    for ss in s:
        print(ss)

def test_extend_keys(key, max_dist):
    # cdef set[string] s = extend_keys(key, max_dist)
    # print_vec2d(vec2d)
    # print_set_of_string(s)
    print_vec1d()
    pass