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

namespace aoc_utils {
    fs::path find_input_dir() {
        fs::path cwd = fs::current_path();
        while (cwd.parent_path() != cwd) {
            if (fs::exists(cwd / "input") && fs::is_directory(cwd / "input"))
                return cwd / "input";
            cwd = cwd.parent_path();
        }
        throw runtime_error("Input directory cannot be found!");
    }

    fs::path find_input_file(int year, int day, bool test) {
        fs::path input_dir = find_input_dir();
        stringstream fname_ss;
        fname_ss << year << "_";
        fname_ss << setw(2) << setfill('0') << day;
        if (test) {
            fname_ss << "_test";
        }
        fname_ss << ".txt";

        return input_dir / fname_ss.str();
    }

    ifstream open_input_file(fs::path input_file) {
        ifstream fp;
        if (!fs::exists(input_file)) {
            throw runtime_error("File cannot be found: " + input_file.string());
        }
        fp.open(input_file);
        cout << "Opened input file: " << input_file << "\n";
        return fp;
    }

    vector<string> read_input_lines(fs::path input_file) {
        ifstream ifs = open_input_file(input_file);

        vector<string> lines;
        string line;
        while (std::getline(ifs, line)) {
            lines.push_back(line);
        }
        return lines;
    }

    vector<int> read_input_ints(fs::path input_file) {
        ifstream ifs = open_input_file(input_file);

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

}
