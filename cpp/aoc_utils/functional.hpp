#pragma once
#include <vector>

#include "aoc_utils/common.hpp"

template <typename T> long long sum(const std::vector<T>& v) {
    long long res = 0;
    for (const T& t : v)
        res += t;
    return res;
}

template <typename T> std::vector<long long> upcast(const std::vector<T>& v) {
    std::vector<long long> vll(v.size(), 0);
    for (uint i = 0; i < v.size(); i++)
        vll[i] = v[i];
    return vll;
}
