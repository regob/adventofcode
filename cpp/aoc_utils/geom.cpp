#include <cstdint>
#include <string>

#include "aoc_utils/geom.hpp"

using namespace std;

v2::v2(int64_t x, int64_t y) : x(x), y(y) {}
v2::v2(int32_t x, int32_t y) : x(x), y(y) {}
v2 v2::operator+(const v2& right) { return v2(x + right.x, y + right.y); }
v2 v2::operator-(const v2& right) { return v2(x - right.x, y - right.y); }
v2 v2::operator*(const v2& right) { return v2(x * right.x, y * right.y); }
v2 v2::operator/(const v2& right) { return v2(x / right.x, y / right.y); }
int64_t v2::dot(const v2 &right) {return (x * right.x + y * right.y);}

std::string to_string(const v2& v) {
    return "(" + to_string(v.x) + ", " + to_string(v.y) + ")";
}
