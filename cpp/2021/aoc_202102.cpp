#include <cstdlib>
#include <iostream>
#include <numeric>
#include <vector>

#include <boost/algorithm/string.hpp>

#include "aoc_utils/io.hpp"
#include "aoc_utils/geom.hpp"

using namespace std;

namespace aoc202102 {
    struct Command {
        string cmd;
        int value;
        Command(string cmd, int value) : cmd(cmd), value(value) {}
    };

    vector<Command> parse_commands(const vector<string> &v) {
        vector<Command> commands;
        vector<string> parts;
        for (string s : v) {
            boost::split(parts, s, boost::is_any_of(" "));
            if (parts.size() < 2) {
                throw runtime_error("Cannot parse command: " + s);
            }
            commands.emplace_back(parts[0], atoi(parts[1].c_str()));
            parts.clear();
        }
        return commands;
    }


    v2 apply_commands(const v2 &pos, const vector<Command> &cmds) {
        v2 p = pos;
        for (Command cmd : cmds) {
            if (cmd.cmd == "forward")
                p = p + v2(cmd.value, 0);
            else if (cmd.cmd == "up")
                p = p - v2(0, cmd.value);
            else if (cmd.cmd == "down")
                p = p + v2(0, cmd.value);
            else
                throw logic_error("Not supported cmd: " + cmd.cmd);
        }
        return p;
    }

    v2 apply_commands_aim(const v2& pos, const vector<Command>& cmds) {
        v2 p = pos;
        int aim = 0;
        for (Command cmd : cmds) {
            if (cmd.cmd == "forward")
                p = p + v2(cmd.value, aim * cmd.value);
            else if (cmd.cmd == "up")
                aim -= cmd.value;
            else if (cmd.cmd == "down")
                aim += cmd.value;
            else
                throw logic_error("Not supported cmd: " + cmd.cmd);
        }
        return p;
    }

} // namespace aoc202102

using namespace aoc202102;

void solve_202102() {
    auto lines = read_input_lines(2021, 2);
    auto cmds = parse_commands(lines);
    cout << "Cmd size " << cmds.size() << "\n";
    v2 pos = apply_commands({0, 0}, cmds);
    int res = pos.x * pos.y;
    report_output(res);

    // part 2
    pos = apply_commands_aim({0, 0}, cmds);
    res = pos.x * pos.y;
    report_output(res);
}
