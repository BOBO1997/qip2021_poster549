#include <iostream>
#include <map>
#include <set>
#include <vector>
#include <string>

#include "combinations.hpp"

namespace libs_qrem {

string change_bit_at_poses(string key, vector<int> poses) {

    for (const auto& pos: poses) {
        if (key[pos] == '0') {
            key[pos] = '1';
        }
        else {
            key[pos] = '0';
        }
    }
    return key
}

set<string> extend_keys(set<string> original_keys, int max_dist) {
    set<string> extended_key_set;
    for (const auto& key: original_keys) {
        extended_key_set.insert(key)
        int n = key.size()
        for (int d = 0; d < max_dist; d++) {
            vector<vector<int>> combs = combinations(n, d + 1)
            for (const auto& comb: combs) {
                new_key = change_bit_at_poses(key, comb)
                extended_key_set.insert(new_key)
            }
        }
    }
    return extended_key_set
}

vector<double> extended_vectors(map<string, double> y, map<string, int> keys_to_indices) {
    vector<double> exteded_y(keys_to_indices.size(), 0);
    for (const auto& item: y) {
        extended_y[keys_to_indices[item.first]] = item.second
    }
    return extended_y;
}

}

