#include <algorithm>
#include <cassert>
#include <climits>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

#include "aoc_utils/common.hpp"
#include "aoc_utils/functional.hpp"
#include "aoc_utils/io.hpp"
#include "boost/algorithm/string.hpp"
#include "boost/regex.hpp"

using namespace std;
using namespace aoc_utils;
using namespace boost;

namespace aoc202108 {
    const string DIGITS[10] = {
        "abcefg", "cf",     "acdeg", "acdfg",   "bcdf",
        "abdfg",  "abdefg", "acf",   "abcdefg", "abcdfg",
    };

    int lookup_digit(const string& s) {
        for (int i = 0; i < 10; i++)
            if (DIGITS[i] == s)
                return i;
        throw out_of_range("Digit undefined for string: " + s);
    }

    pair<vector<string>, vector<string>> parse_line(const string& line) {
        regex line_pattern("([a-z ]+) \\| ([a-z ]+)");
        // regex line_pattern("(?:([a-z]+) ){10}\\s*\\|.*");
        vector<string> chunk1, chunk2;

        smatch what;
        if (!regex_match(line, what, line_pattern, boost::match_extra)) {
            throw runtime_error("Line did not match regex: '" + line + "'");
        }

        string s_input(what[1].first, what[1].second);
        string s_output(what[2].first, what[2].second);
        boost::trim(s_input);
        boost::trim(s_output);
        boost::split(chunk1, s_input, boost::is_any_of(" "));
        boost::split(chunk2, s_output, boost::is_any_of(" "));

        return {chunk1, chunk2};
    }

    string find_by_charset(const vector<string>& elems, const set<char>& s,
                           bool containing = true) {
        for (const string& e : elems) {
            uint missing = (s - to_set(e)).size();
            if (missing == 0 && containing)
                return e;
            if (missing > 0 && !containing)
                return e;
        }
        throw std::invalid_argument("Cannot found set of chars in elems!");
    }

    // return sorted wire ids for digit i at pos i
    vector<string> solve_mapping(const vector<string>& wirings) {
        assert(wirings.size() == 10);
        map<int, vector<string>> wiring_bysize;
        for (const string& w : wirings)
            wiring_bysize[w.size()].push_back(w);

        assert(wiring_bysize[2].size() == 1); // digit 1
        assert(wiring_bysize[3].size() == 1); // digit 7
        assert(wiring_bysize[4].size() == 1); // digit 4
        assert(wiring_bysize[7].size() == 1); // digit 8

        string digit1 = wiring_bysize[2][0];
        string digit7 = wiring_bysize[3][0];
        string digit4 = wiring_bysize[4][0];
        string digit8 = wiring_bysize[7][0];

        char c_cand = digit1.at(0);
        char f_cand = digit1.at(1);

        // find digit 3
        string digit3 =
            find_by_charset(wiring_bysize[5], set<char>{c_cand, f_cand});

        char b = *(to_set(digit4) - to_set(digit3)).begin();
        char d = *(to_set(digit4) - to_set(digit7) - set<char>{b}).begin();

        string digit0 =
            find_by_charset(wiring_bysize[6], set<char>{b, d}, false);
        string digit9 = find_by_charset(wiring_bysize[6],
                                        set<char>{d, c_cand, f_cand}, true);

        char e = *(to_set(digit8) - to_set(digit9)).begin();
        string digit6 =
            find_by_charset(wiring_bysize[6], set<char>{e, d}, true);

        // digits 2 and 5 at last
        string digit5 = find_by_charset(wiring_bysize[5], set<char>{b}, true);
        string digit2 =
            find_by_charset(wiring_bysize[5], set<char>{d, e}, true);

        vector<string> digits = {
            digit0, digit1, digit2, digit3, digit4,
            digit5, digit6, digit7, digit8, digit9,
        };

        for (string& s : digits) {
            sort(s.begin(), s.end());
        }
        return digits;
    }

    string decode_digits(const vector<string>& wirings,
                         const vector<string>& mapping) {
        string res;
        for (const string& w : wirings) {
            string s = w;
            sort(s.begin(), s.end());
            auto pos = std::find(mapping.begin(), mapping.end(), s);
            int digit = (pos - mapping.begin());
            res.push_back('0' + digit);
        }
        return res;
    }

    int digit_total_occurrences(const vector<string>& v,
                                const set<char> digits) {
        int total = 0;
        for (const string& s : v) {
            for (char ch : s)
                if (digits.find(ch) != digits.end())
                    total++;
        }
        return total;
    }
} // namespace aoc202108

using namespace aoc202108;

void solve_202108() {
    auto input_lines = read_input_lines(find_input_file(2021, 8));
    cout << "Loaded " << input_lines.size() << " lines\n";

    vector<string> outputs;
    int idx = 0;
    for (const string& s : input_lines) {
        auto res = parse_line(s);
        auto mapping = solve_mapping(res.first);
        auto output_str = decode_digits(res.second, mapping);
        outputs.push_back(output_str);
        // cout << idx++ << ": " << output_str << endl;
    }

    // part 1
    long long total_occ =
        digit_total_occurrences(outputs, set<char>{'1', '4', '7', '8'});
    report_output(total_occ);

    // part 2
    long long output_sum = 0;
    for (const string& s : outputs) {
        output_sum += stoi(s);
    }
    report_output(output_sum);
}
