#pragma once
#include <cstdint>
#include <string>

#include "aoc_utils/common.hpp"

namespace aoc_utils {
    struct v2 {
        int64_t x;
        int64_t y;
        v2(int64_t x, int64_t y);
        v2(int32_t x, int32_t y);
        v2(uint32_t x, uint32_t y);
        v2(uint64_t x, uint64_t y);
        v2 operator+(const v2 &right) const;
        v2 operator-(const v2 &right) const;
        v2 operator*(const v2& right) const;
        v2 operator/(const v2& right) const;
        bool operator<(const v2& right) const;
        int64_t dot(const v2 &right);
    };

    std::string to_str(const v2 &v);
}
