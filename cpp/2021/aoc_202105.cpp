#include <iostream>
#include <vector>
#include <string>

#include <boost/algorithm/string.hpp>
#include <boost/regex.hpp>

#include "aoc_utils/geom.hpp"
#include "aoc_utils/io.hpp"
#include "aoc_utils/matrix.hpp"

using namespace std;
using namespace aoc_utils;
using namespace boost;

typedef pair<v2, v2> Line;

namespace aoc202105 {
    vector<Line> parse_lines(const vector<string>& lines) {
        vector<Line> res;
        regex line_pattern("([0-9]+),([0-9]+)\\s*->\\s*([0-9]+),([0-9]+)\\s*");

        for (const string& s : lines) {
            smatch what;
            if (!regex_match(s, what, line_pattern)) {
                throw runtime_error("Line did not match regex: '" + s + "'");
            }
            string start_x = string(what[1].first, what[1].second);
            string start_y = string(what[2].first, what[2].second);
            v2 start(stoi(start_x), stoi(start_y));

            string end_x = string(what[3].first, what[3].second);
            string end_y = string(what[4].first, what[4].second);
            v2 end(stoi(end_x), stoi(end_y));
            res.emplace_back(start, end);
        }
        return res;
    }

    vector<Line> normalize_lines(const vector<Line>& lines) {
        vector<Line> norm_lines;
        for (const Line& line : lines) {
            bool diff_lines_rev = line.first.x > line.second.x;
            bool same_line_rev =
                line.first.x == line.second.x && line.first.y > line.second.y;
            if (diff_lines_rev || same_line_rev) {
                norm_lines.emplace_back(line.second, line.first);
                continue;
            }

            norm_lines.emplace_back(line.first, line.second);
        }
        return norm_lines;
    }

    int num_overlaps(const vector<Line>& lines, uint rows, uint cols,
                     bool diagonals = false) {
        matrix<int> cnt(rows, cols, 0);
        for (const Line& line : lines) {
            // diagonal
            if (line.first.x != line.second.x &&
                line.first.y != line.second.y) {
                if (!diagonals)
                    continue;
                int diff = line.second.x - line.first.x;
                assert(diff > 0);

                int mul = 1;
                if (line.second.y - line.first.y < 0) {
                    mul = -1;
                }
                assert(mul * diff == line.second.y - line.first.y);
                for (int i = 0; i <= diff; i++) {
                    cnt[line.first.y + mul * i][line.first.x + i] += 1;
                }

            } else if (line.first.y == line.second.y) {
                // horizontal
                for (uint x = line.first.x; x <= line.second.x; x++)
                    cnt[line.first.y][x] += 1;
            } else {
                // vertical
                assert(line.first.x == line.second.x);
                for (uint y = line.first.y; y <= line.second.y; y++)
                    cnt[y][line.first.x] += 1;
            }
        }

        int total = (cnt >= 2).sum();
        return total;
    }
} // namespace aoc202105

using namespace aoc202105;

void solve_202105() {
    auto input_lines = read_input_lines(find_input_file(2021, 5));
    vector<Line> lines = parse_lines(input_lines);
    cout << "Read " << lines.size() << " input lines\n";

    uint MAXR = 1000;
    uint MAXC = 1000;

    vector<Line> norm_lines = normalize_lines(lines);
    int overlaps_wo_diag = num_overlaps(norm_lines, MAXR, MAXC);
    report_output(overlaps_wo_diag);

    int overlaps_w_diag = num_overlaps(norm_lines, MAXR, MAXC, true);
    report_output(overlaps_w_diag);
}
