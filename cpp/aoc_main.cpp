#include <cstdlib>
#include <iostream>
#include <stdlib.h>

#include "2021/aoc_2021.h"

int main(int argc, char* argv[]) {
    if (argc != 3) {
        std::cout << "Usage: " << argv[0] << " YEAR DAY" << std::endl;
        exit(1);
    }

    int day = std::atoi(argv[2]);
    int year = std::atoi(argv[1]);
    int dt = year * 100 + day;
    switch (dt) {
    case 202101:
        solve_202101();
        break;
    case 202102:
        solve_202102();
        break;
    case 202103:
        solve_202103();
        break;
    case 202104:
        solve_202104();
        break;
    case 202105:
        solve_202105();
        break;
    case 202106:
        solve_202106();
        break;
    case 202107:
        solve_202107();
        break;
    case 202108:
        // solve_202108();
        break;
    case 202109:
        // solve_202109();
        break;
    case 202110:
        // solve_202110();
        break;
    default:
        std::cout << "Invalid day provided (or not implemented yet): " << day
                  << "\n";
        exit(1);
    }
}
