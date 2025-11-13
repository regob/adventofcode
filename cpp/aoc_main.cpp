#include <cstdlib>
#include <iostream>
#include <stdlib.h>

void solve_202101();
void solve_202102();

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
    default:
      std::cout << "Invalid day provided (or not implemented yet): " << day
                << "\n";
      exit(1);
    }
}
