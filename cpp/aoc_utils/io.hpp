#include <iostream>
#include <string>
#include <vector>
std::vector<std::string> read_input_lines(int year, int day);
std::vector<int> read_input_ints(int year, int day);
void report_output(int x);

// Debug print ////////////////////////////////////////////////////////////////

const int DEBUG_INDENT = 2;

template <typename T> static void _print_value(const T& x, int indent = 0) {
    std::cout << std::string(indent, ' ');
    std::cout << x << "\n";
}

template<typename T>
void print_debug(const std::vector<T>& vec, int indent = 0, int limit = 40) {
    std::cout << "vector:[\n";
    int nested_indent = indent + DEBUG_INDENT;
    if (vec.size() <= limit) {
        for (const auto& elem : vec) {
            _print_value(elem, nested_indent);
        }
    } else {
        int half = limit / 2;
        for (uint i = 0; i < half; i++)
            _print_value(vec[i], nested_indent);
        std::cout << std::string(nested_indent, ' ') << "...\n";
        for (uint i = vec.size() - (limit - half); i < vec.size(); i++)
            _print_value(vec[i], nested_indent);
    }
    std::cout << "]\n";
}

template <typename T> void print_debug(const T& x, int indent = 0) {
    _print_value(x, indent);
}

