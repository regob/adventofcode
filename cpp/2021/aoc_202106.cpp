#include <iostream>
#include <vector>
#include <string>

#include "aoc_utils/io.hpp"
#include "aoc_utils/functional.hpp"

using namespace std;
using namespace aoc_utils;

namespace aoc202106 {
    using ll = long long;
    vector<ll> histogram(const vector<ll>& items, int max_item) {
        vector<ll> hist(max_item + 1, 0);
        for (ll x : items)
            hist[x]++;
        return hist;
    }

    vector<ll> simulate_fish(const vector<ll>& item_hist, int steps,
                              int breed_freq = 6,
                              int breed_wait = 2) {
        vector<ll> state = item_hist;

        for (uint i = 0; i < steps; i++) {
            vector<ll> res(state.size(), 0);

            res[breed_freq] += state[0];
            res[breed_freq + breed_wait] += state[0];
            for (uint j = 1; j < state.size(); j++) {
                res[j - 1] += state[j];
            }
            state = res;
        }
        return state;
    }
} // namespace aoc202106

using namespace aoc202106;

void solve_202106() {
    auto input_ints = upcast(read_input_ints(find_input_file(2021, 6)));
    cout << "Loaded " << input_ints.size() << " integers\n";
    const int MAX_AGE = 10;
    auto hist = histogram(input_ints, MAX_AGE);
    auto res1 = sum(simulate_fish(hist, 80));
    report_output(res1);

    auto res2 = sum(simulate_fish(hist, 256));
    report_output(res2);
}
