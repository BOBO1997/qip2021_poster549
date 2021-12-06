import cython
cimport cython

from libcpp.map import map
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.set cimport set

# OK, O(n)
cdef string change_bit_at_poses(string key, vector[int] poses):
    for pos in poses:
        key = key[:pos] + "1" + key[pos + 1:] if key[pos] == "0" else key[:pos] + "0" + key[pos+1:]
    return key

# OK, O(n * 2^d)
cdef set[string] extend_keys(set[string] original_keys, int max_dist):

    extended_key_set = original_keys

    for key in original_keys:
        n = len(key)
        for d in range(max_dist):
            combs = combinations(range(n), d + 1)
            for comb in combs:
                new_key = change_bit_at_poses(key, comb)
                extended_key_set.add(new_key)
    return extended_key_set

cdef map[string, double] extend_vectors(map[string, double] y, map[string, int] keys_to_indices):
    extended_y = np.zeros(len(list(keys_to_indices)))
    for key, value in y.items():
        extended_y[keys_to_indices[key]] = value
    return extended_y
