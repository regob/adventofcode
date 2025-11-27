#include <iostream>
#include <set>
#include <string>


using namespace std;

std::set<char> to_set(const std::string &v) {
    std::set<char> s(v.begin(), v.end());
    return s;
}
