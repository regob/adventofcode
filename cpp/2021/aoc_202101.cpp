#include <iostream>
#include <numeric>
#include <vector>

#include "aoc_utils/io.hpp"

using namespace std;
using namespace aoc_utils;

namespace aoc202101 {
    int num_increases(const vector<int> &v) {
        int cnt = 0;
        for (uint i = 1; i < v.size(); i++) {
            if (v[i] > v[i-1]) cnt++;
        }
        return cnt;
    }

    vector<int> sliding_sums(const vector<int> &v, int win_size) {
        vector<int> res;
        if (win_size > v.size())
            return res;
        int ptr = win_size;
        int s = accumulate(&v[0], &v[ptr], 0);
        res.push_back(s);

        while (ptr < v.size()) {
            s += v[ptr];
            s -= v[ptr - win_size];
            ptr++;
            res.push_back(s);
        }
        return res;
    }
} // namespace aoc202101

using namespace aoc202101;

void solve_202101() {
    auto ints = read_input_ints(2021, 1);
    int res = num_increases(ints);
    report_output(res);

    auto sums = sliding_sums(ints, 3);
    int res_2 = num_increases(sums);
    report_output(res_2);
}
