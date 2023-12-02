import kotlin.math.abs

private fun part1(input: List<String>): Int {
    var total = 0
    var (bound, boundMx) = 20 to 220
    var (x, cycle) = 1 to 0
    for (s in input) {
        val y = if (s == "noop") {
            cycle += 1
            0
        } else {
            cycle += 2
            s.split(" ")[1].toInt()
        }

        if (cycle >= bound) {
            total += bound * x
            bound += 40
        }
        x += y
        if (bound > boundMx) break
    }
    return total
}

private fun outputAt(i: Int, sprite: Int) : String {
    val r = (i - 1) % 40
    val ch = if (abs(sprite - r) <= 1) "#" else "."
    if (r == 39) return ch + "\n"
    return ch
}

private fun part2(input: List<String>){
    val output = mutableListOf<String>()
    var (x, cycle) = 1 to 0
    for (s in input) {
        val y = if (s == "noop") {
            cycle += 1
            output.add(outputAt(cycle, x))
            0
        } else {
            cycle += 2
            output.add(outputAt(cycle - 1, x))
            output.add(outputAt(cycle, x))
            s.split(" ")[1].toInt()
        }
        x += y
    }
    println(output.joinToString(""))
}


fun main() {
    val input = readInput(10).trim().lines()
    println(part1(input))
    part2(input)
}