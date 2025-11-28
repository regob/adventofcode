#pragma once
#include <algorithm>
#include <cmath>
#include <set>
#include <stdexcept>
#include <string>
#include <unordered_set>
#include <vector>

#include "aoc_utils/common.hpp"

// Basic vector reductions/operations /////////////////////////////////////////
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

template <typename T> std::vector<T> tail(const std::vector<T>& v, int n) {
    if (n > v.size())
        throw std::out_of_range("tail: n > v.size()");

    std::vector<T> res;
    for (uint i = v.size() - n; i < v.size(); i++)
        res.push_back(v[i]);
    return res;
}

template <typename T> std::vector<T> head(const std::vector<T>& v, int n) {
    if (n > v.size())
        throw std::out_of_range("head: n > v.size()");

    std::vector<T> res;
    for (uint i = 0; i < n; i++)
        res.push_back(v[i]);
    return res;
}


// Boolean ops ////////////////////////////////////////////////////////////////

template <typename T> std::vector<int> operator!(const std::vector<T>& v_bool) {
    std::vector<int> res(v_bool.size(), 0);
    for (uint i = 0; i < res.size(); i++)
        res[i] = (!v_bool[i]);
    return res;
}

template <typename T> std::vector<int> operator<(const std::vector<T>& v, const T& x) {
    std::vector<int> res(v.size(), 0);
    for (uint i = 0; i < res.size(); i++)
        res[i] = (v[i] < x);
    return res;
}

template <typename T> std::vector<int> operator>(const std::vector<T>& v, const T& x) {
    std::vector<int> res(v.size(), 0);
    for (uint i = 0; i < res.size(); i++)
        res[i] = (v[i] > x);
    return res;
}




// Casting ////////////////////////////////////////////////////////////////////

template <typename T> std::vector<long long> upcast(const std::vector<T>& v) {
    std::vector<long long> vll(v.size(), 0);
    for (uint i = 0; i < v.size(); i++)
        vll[i] = v[i];
    return vll;
}

template <typename T> std::set<T> to_set(const std::vector<T>& v) {
    std::set<T> s(v.begin(), v.end());
    return s;
}

std::set<char> to_set(const std::string& v);

template <typename T> std::unordered_set<T> to_uset(const std::vector<T>& v) {
    std::unordered_set<T> s(v.begin(), v.end());
    return s;
}

// Set operations /////////////////////////////////////////////////////////////

template <typename T>
std::set<T> operator-(const std::set<T>& s1, const std::set<T>& s2) {
    std::set<T> s = s1;
    for (const T &t : s2) s.erase(t);
    return s;
}
