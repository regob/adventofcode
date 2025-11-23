#include <algorithm>
#include <charconv>
#include <cstdlib>
#include <iostream>
#include <numeric>
#include <system_error>
#include <vector>
#include <sstream>
#include <optional>

#include <boost/algorithm/string.hpp>

#include "aoc_utils/io.hpp"
#include "aoc_utils/matrix.hpp"
#include "aoc_utils/geom.hpp"

using namespace std;
using namespace aoc_utils;

namespace aoc202104  {
    vector<int> parse_nums(const string& line, char sep) {
        string token;
        istringstream is(line);
        vector<int> nums;

        while (getline(is, token, sep)) {
            if (token.size())
                nums.push_back(stoi(token));
        }
        return nums;
    }

    matrix<int> parse_matrix(const vector<string> &lines, char sep) {
        vector<vector<int>> m;
        m.resize(lines.size());
        uint i = 0;
        for (string line : lines) {
            m[i++] = parse_nums(line, sep);
        }
        return matrix(m);
    }

    optional<v2> find_in_bingo(const matrix<int>& bingo, int num) {
        for (int row = 0; row < bingo.nrow; row++)
            for (int col = 0; col < bingo.ncol; col++)
                if (bingo.at(row, col) == num)
                    return v2(row, col);
        return nullopt;
    }

    // returns {num_rounds, score}
    optional<pair<int, int>> solve_bingo(const matrix<int>& bingo, const vector<int>& nums) {
        matrix<int> was(bingo.nrow, bingo.ncol, 0);
        for (uint i = 0; i < nums.size(); ++i) {
            auto pos = find_in_bingo(bingo, nums[i]);
            if (pos.has_value()) {
                const auto [x, y] = pos.value();
                was[x][y] = 1;
            }

            bool done = false;
            for (uint row = 0; row < was.nrow; row++)
                if (was.row_sum(row) == was.ncol)
                    done = true;
            for (uint col = 0; col < was.ncol; col++)
                if (was.col_sum(col) == was.nrow)
                    done = true;

            if (done) {
                int board_sum = (bingo * (!was)).sum();
                return pair(i + 1, board_sum * nums[i]);
            }
        }
        return nullopt;
    }
} // namespace aoc202104

using namespace aoc202104;

void solve_202104() {
    auto lines = read_input_lines(2021, 4);
    auto bingo_nums = parse_nums(lines[0], ',');
    assert(lines[1] == "");
    vector<matrix<int>> bingos;

    int start = 2;
    while (true) {
        while (start < lines.size() && lines[start] == "")
            start++;
        if (start >= lines.size()) break;
        int end = start + 1;
        while (end < lines.size() && lines[end] != "")
            end++;
        vector<string> bingo_lines(lines.begin() + start, lines.begin() + end);
        matrix<int> bingo = parse_matrix(bingo_lines, ' ');
        bingos.push_back(bingo);
        start = end;
    }
    uint n_bingos = bingos.size();

    vector<optional<pair<int, int>>> solutions;
    for (uint i = 0; i < n_bingos; ++i) {
        auto res = solve_bingo(bingos[i], bingo_nums);
        if (!res.has_value()) {
            cout << "No solution for puzzle " << i << "\n";
        }
        solutions.push_back(res);
    }

    int best_val = -1;
    int best_score = -1;
    for (auto res : solutions) {
        if (!res.has_value())
            continue;
        auto [rounds, score] = res.value();
        if (best_val < 0 || rounds < best_val) {
            best_val = rounds;
            best_score = score;
        }
    }
    report_output(best_score);

    // part 2
    int worst_res = 0;
    int worst_score = 0;
    for (auto res : solutions) {
        if (res.value().first > worst_res) {
            worst_score = res.value().second;
            worst_res = res.value().first;
        }
    }
    report_output(worst_score);
}
