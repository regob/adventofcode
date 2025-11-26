#include <algorithm>
#include <climits>
#include <cassert>
#include <iostream>
#include <vector>
#include <string>

#include "aoc_utils/io.hpp"
#include "aoc_utils/common.hpp"
#include "aoc_utils/functional.hpp"

using namespace std;
using namespace aoc_utils;

namespace aoc202107 {
    long long fuel_needed(const vector<int> &items, int pos) {
        long long total = 0;
        for (int x : items) {
            int diff = abs(x - pos);
            total += diff * (diff + 1) / 2;
        }
        return total;
    }

    long long min_fuel_needed_brute(const vector<int> &items) {
        long long best = LONG_LONG_MAX;
        int min_item = min(items);
        int max_item = max(items);
        for (int i = min_item; i <= max_item; i++) {
            best = min(best, fuel_needed(items, i));
        }
        return best;
    }

    // ternary search for convex function, should have only one minimum
    // each time the interval is halved, but the fun is evaled at most 5 times
    // so complexity should be around O(5 * log2 n)
    long long min_fuel_needed_opt(const vector<int>& items) {
        long long l = min(items);
        long long r = max(items);
        long long mid = (r + l) / 2;

        while (r - l >= 2) {
            long long vl = fuel_needed(items, l);
            long long vr = fuel_needed(items, r);
            long long vmid = fuel_needed(items, mid);

            if (vl >= vmid && vmid >= vr) {
                l = mid;
            } else if (vl <= vmid && vmid <= vr) {
                r = mid;
            } else {
                // mid is smallest, we have other three options
                assert(vl >= vmid && vmid <= vr);

                // unless we only have mid left ...
                if (r - l == 2)
                    return vmid;

                long long l2 = (l + mid) / 2;
                long long r2 = (r + mid) / 2;
                long long vl2 = fuel_needed(items, l2);
                long long vr2 = fuel_needed(items, r2);

                if (vl2 < vmid) {
                    l = l2;
                    r = mid;
                } else if (vr2 < vmid) {
                    l = mid;
                    r = r2;
                } else {
                    l = l2;
                    r = r2;
                }
            }
            mid = (r + l) / 2;
        }
        return min(fuel_needed(items, l), fuel_needed(items, r));
    }
} // namespace aoc202107

using namespace aoc202107;

void solve_202107() {
    auto input_ints = read_input_ints(find_input_file(2021, 7));
    cout << "Loaded " << input_ints.size() << " integers\n";

    int med = lower_median(input_ints);
    cout << "Lower median: " << med << endl;

    vector<int> diffs = input_ints - med;
    long long res = sum(abs(diffs));
    report_output(res);

    // part 2
    // res = min_fuel_needed_brute(input_ints);
    res = min_fuel_needed_opt(input_ints);
    report_output(res);
}
