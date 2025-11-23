#include <charconv>
#include <iostream>
#include <system_error>
#include <vector>

#include <boost/algorithm/string.hpp>

#include "aoc_utils/io.hpp"

using namespace std;
using namespace aoc_utils;

namespace aoc202103 {
    vector<int> parse_ints_base2(const vector<string>& v) {
        vector<int> vi;
        int res = -1;
        for (string s : v) {
            auto [ptr, ec] = from_chars(s.data(), s.data() + s.size(), res, 2);
            if (ec == errc()) {
                vi.push_back(res);
            } else {
                throw invalid_argument("Cannot parse to int: " + string("'") + s + "'");
            }
        }
        return vi;
    }

    int bit_present_count(const vector<int>& vi, int bit) {
        int total = 0;
        for (int x : vi) {
            if (x & (1 << bit)) total++;
        }
        return total;
    }

    int power_consumption(const vector<int>& vi, int bit_width) {
        int gamma = 0;
        int elems = vi.size();
        for (uint i = 0; i < bit_width; i++) {
            int present = bit_present_count(vi, i);
            if (present > elems / 2) gamma += 1 << i;
        }
        int epsilon = (~gamma) & ((1 << bit_width) - 1);
        return epsilon * gamma;
    }

    vector<int> filter_on_bit(const vector<int>& vi, int bit, bool keep_one) {
        vector<int> v_filt;
        for (int x : vi) {
            bool has_bit = (1 << bit) & x;
            if (has_bit == keep_one) v_filt.push_back(x);
        }
        return v_filt;
    }

    int find_rating(const vector<int>& vi, int bit_width, bool most_common, bool keep_ones_on_tie) {
        vector<int> cands = vi;
        int bit = bit_width - 1;
        while (cands.size() > 1 && bit >= 0) {
            int sz = cands.size();

            int bit_cnt = bit_present_count(cands, bit);
            int keep_one = true;
            if (2 * bit_cnt == sz) {
                keep_one = keep_ones_on_tie;
            } else {
                bool ones_more_common = 2 * bit_cnt > sz;
                keep_one = ones_more_common == most_common;
            }
            cands = filter_on_bit(cands, bit, keep_one);
            bit--;
        }
        assert(cands.size() == 1);
        return cands[0];
    }

} // namespace aoc202103

using namespace aoc202103;

void solve_202103() {
    auto lines = read_input_lines(2021, 3);
    int bit_width = lines[0].size();
    auto ints = parse_ints_base2(lines);
    int res = power_consumption(ints, bit_width);
    report_output(res);

    int oxygen = find_rating(ints, bit_width, true, true);
    cout << "Oxygen: " << oxygen << endl;
    int co2 = find_rating(ints, bit_width, false, false);
    cout << "CO2: " << co2 << endl;

    int res2 = oxygen * co2;
    report_output(res2);
}
