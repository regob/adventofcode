#pragma once
#include <cstdint>
#include <string>

namespace aoc_utils {
    struct v2 {
        int64_t x;
        int64_t y;
        v2(int64_t x, int64_t y);
        v2(int32_t x, int32_t y);
        v2 operator+(const v2 &right);
        v2 operator-(const v2 &right);
        v2 operator*(const v2& right);
        v2 operator/(const v2& right);
        int64_t dot(const v2 &right);
    };

    std::string to_str(const v2 &v);
}
