#pragma once
#include <algorithm>
#include <cmath>
#include <vector>

#include "aoc_utils/common.hpp"

template <typename T> long long sum(const std::vector<T>& v) {
    long long res = 0;
    for (const T& t : v)
        res += t;
    return res;
}

template <typename T> T max(const std::vector<T>& v) {
    return *std::max_element(v.begin(), v.end());
}

template <typename T> T min(const std::vector<T>& v) {
    return *std::min_element(v.begin(), v.end());
}

template <typename T> std::vector<T> abs(const std::vector<T>& v) {
    std::vector<T> res(v.size(), 0);
    for (uint i = 0; i < res.size(); i++)
        res[i] = std::abs(v[i]);
    return res;
}

template <typename T> std::vector<long long> pow(const std::vector<T>& v, int k) {
    std::vector<long long> res(v.size(), 0);
    for (uint i = 0; i < res.size(); i++)
        res[i] = pow(v[i], k);
    return res;
}

template <typename T> std::vector<T> operator-(const std::vector<T>& v, const T& x) {
    std::vector<T> res = v;
    for (uint i = 0; i < res.size(); i++)
        res[i] -= x;
    return res;
}

template <typename T> std::vector<T> operator+(const std::vector<T>& v, const T& x) {
    std::vector<T> res = v;
    for (uint i = 0; i < res.size(); i++)
        res[i] += x;
    return res;
}

template <typename T> std::vector<T> operator*(const std::vector<T>& v, const T& x) {
    std::vector<T> res = v;
    for (uint i = 0; i < res.size(); i++)
        res[i] *= x;
    return res;
}

template <typename T> std::vector<T> operator/(const std::vector<T>& v, const T& x) {
    std::vector<T> res = v;
    for (uint i = 0; i < res.size(); i++)
        res[i] /= x;
    return res;
}


template <typename T> T lower_median(const std::vector<T>& v) {
    std::vector<T> cpy = v;
    int n = v.size() / 2;
    std::nth_element(cpy.begin(), cpy.begin() + n - 1, cpy.end());
    return cpy[n - 1];
}

template <typename T> std::vector<long long> upcast(const std::vector<T>& v) {
    std::vector<long long> vll(v.size(), 0);
    for (uint i = 0; i < v.size(); i++)
        vll[i] = v[i];
    return vll;
}
