#include <filesystem>
#include <vector>
#include <string>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>

#include "aoc_utils/io.hpp"

using namespace std;
namespace fs = std::filesystem;

fs::path find_input_dir() {
    fs::path cwd = fs::current_path();
    while (cwd.parent_path() != cwd) {
        if (fs::exists(cwd / "input") && fs::is_directory(cwd / "input"))
            return cwd / "input";
        cwd = cwd.parent_path();
    }
    throw runtime_error("Input directory cannot be found!");
}

ifstream open_input_file(int year, int day) {
    ifstream fp;
    fs::path input_dir = find_input_dir();
    stringstream fname_ss;
    fname_ss << year << "_";
    fname_ss << setw(2) << setfill('0') << day << ".txt";

    fs::path input_file = input_dir / fname_ss.str();
    if (!fs::exists(input_file)) {
        throw runtime_error("File cannot be found: " + input_file.string());
    }
    fp.open(input_file);
    cout << "Opened input file: " << input_file << "\n";
    return fp;
}

vector<string> read_input_lines(int year, int day) {
    ifstream ifs = open_input_file(year, day);

    vector<string> lines;
    string line;
    while (std::getline(ifs, line)) {
      lines.push_back(line);
    }
    return lines;
}

vector<int> read_input_ints(int year, int day) {
    ifstream ifs = open_input_file(year, day);

    vector<int> v;
    int x;
    while (ifs >> x) {
      v.push_back(x);
    }
    return v;
}


// Output /////////////////////////////////////////////////////////////////////

std::string to_str(const int &x) {return std::to_string(x);}
std::string to_str(const long &x) {return std::to_string(x);}
std::string to_str(const long long &x) {return std::to_string(x);}


// void report_output(int x) {
//     std::cout << "Output: " << std::to_string(x) << "\n";
// }
