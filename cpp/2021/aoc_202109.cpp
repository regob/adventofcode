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
#include "aoc_utils/matrix.hpp"
#include "aoc_utils/geom.hpp"

using namespace std;
using namespace aoc_utils;

namespace aoc202109 {
    matrix<int> parse_grid(const vector<string> &v) {
        matrix<int> m(v.size(), v[0].size(), 0);
        for (uint i = 0; i < m.nrow; i++) {
            for (uint j = 0; j < m.ncol; j++)
                m[i][j] = (v[i][j] - '0');
        }
        return m;
    }

    vector<v2> find_low_points(const matrix<int>& m) {
        vector<v2> pts;
        for (int i = 0; i < m.nrow; i++) {
            for (int j = 0; j < m.ncol; j++) {
                auto neigh = m.neighbors(i, j);
                if (sum(neigh > m[i][j]) == neigh.size()) {
                    pts.emplace_back(i, j);
                }
            }
        }
        return pts;
    }

    using basin = set<v2>;
    vector<basin> find_basins(const matrix<int>& m, const vector<v2>& low_pts) {
        vector<basin> comps;
        for (const v2& low_pt : low_pts) {
            // simple "flood fill"
            set<v2> was {low_pt};
            vector<v2> backlog{low_pt};
            while (backlog.size()) {
                v2 nxt = backlog.back();
                backlog.pop_back();
                for (auto neigh : m.neighbor_coords(nxt.x, nxt.y)) {
                    if (was.find(neigh) != was.end())
                        continue;
                    if (m[neigh.x][neigh.y] == 9) continue;
                    was.insert(neigh);
                    backlog.push_back(neigh);
                }
            }
            comps.push_back(was);
        }
        return comps;
    }
}
using namespace aoc202109;

void solve_202109() {
    auto input_lines = read_input_lines(find_input_file(2021, 9));
    cout << "Loaded " << input_lines.size() << " lines\n";

    matrix<int> g = parse_grid(input_lines);
    auto pts = find_low_points(g);
    cout << "Grid size: " << g.nrow << " x " << g.ncol << endl;
    cout << "Found low points: " << pts.size() << endl;

    int total_risk = 0;
    for (auto p : pts) {
        total_risk += g[p.x][p.y] + 1;
    }
    report_output(total_risk);

    auto basins = find_basins(g, pts);
    auto basin_comp = [](const basin& left, const basin& right) {
        return left.size() < right.size();
    };
    sort(basins.begin(), basins.end(), basin_comp);
    auto top_3 = tail(basins, 3);
    long long res = 1;
    for (const basin& b : top_3)
        res *= b.size();
    report_output(res);
}
