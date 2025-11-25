#include <array>
#include <cstdint>
#include <numeric>
#include <stdexcept>
#include <string>
#include <vector>

namespace aoc_utils {

    template <typename T> struct matrix {
        uint32_t nrow;
        uint32_t ncol;
        std::vector<std::vector<T>> dat;

        matrix(const std::vector<std::vector<T>>& vec) {
            nrow = vec.size();
            if (nrow == 0)
                throw std::invalid_argument("Matrix cannot have 0 rows!");

            ncol = vec[0].size();
            dat.resize(nrow);
            for (uint i = 0; i < nrow; i++) {
                if (vec[i].size() != ncol)
                    throw std::invalid_argument(
                        "Matrix should have " + std::to_string(ncol) +
                        " columns, found: " + std::to_string(vec[i].size()));
                dat[i] = vec[i];
            }
        }

        matrix(uint32_t nrow, uint32_t ncol, T init_val)
            : nrow(nrow), ncol(ncol) {
            dat.resize(nrow);
            for (uint i = 0; i < nrow; i++) {
                dat[i].resize(ncol, init_val);
            }
        }

        const std::vector<T> & operator[](size_t n) const {
            check_bounds(n);
            return dat[n];
        }

        std::vector<T> & operator[](size_t n) {
            check_bounds(n);
            return dat[n];
        }

        const T& at(size_t r, size_t c) const {
            check_bounds(r, c);
            return dat[r][c];
        }

        long long row_sum(size_t r) const {
            check_bounds(r);
            long long total = 0;
            for (uint i = 0; i < ncol; i++) {
                total += (long long)dat[r][i];
            }
            return total;
        }

        long long col_sum(size_t c) const {
            check_bounds(0, c);
            long long total = 0;
            for (uint i = 0; i < nrow; i++) {
                total += dat[i][c];
            }
            return total;
        }

        long long sum() const {
            long long total = 0;
            for (uint i = 0; i < nrow; i++)
                total += row_sum(i);
            return total;
        }

        matrix<T> operator*(const matrix<T>& mask) const {
            matrix<T> res(nrow, ncol, 0);
            for (uint i = 0; i < nrow; i++) {
                for (uint j = 0; j < ncol; j++) res[i][j] = dat[i][j] * mask.at(i, j);
            }
            return matrix(res);
        }

        matrix<T> operator!() const {
            matrix<T> res(nrow, ncol, 0);
            for (uint i = 0; i < nrow; i++) {
                for (uint j = 0; j < ncol; j++) res[i][j] = !dat[i][j];
            }
            return res;
        }

        matrix<bool> operator>=(const T &x) const {
            matrix<bool> res(nrow, ncol, false);
            for (uint i = 0; i < nrow; i++) {
                for (uint j = 0; j < ncol; j++) res[i][j] = dat[i][j] >= x;
            }
            return res;
        }

      private:
        void check_bounds(size_t r, size_t c = 0) const {
            if (r >= nrow)
                throw std::out_of_range("Matrix row index out of bounds " +
                                        std::to_string(r));
            if (c >= ncol)
                throw std::out_of_range("Matrix column index out of bounds " +
                                        std::to_string(c));
        }
    };
} // namespace aoc_utils
