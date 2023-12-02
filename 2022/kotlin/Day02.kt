private fun part1(input: String): Int {
    return input.lines().asSequence()
        .map { (it[0] - 'A') to (it[2] - 'X') }
        // pairs of (player's shape, difference)
        .map { it.second to (it.second - it.first).mod(3) }
        // score = player's shape + 1 + 3*(difference + 1) % 3
        .map {
            it.first + 1 + 3 * (it.second + 1).mod(3)
        }
        .sum()
}

private fun part2(input: String): Int {
    return input.lines().asSequence()
        .map { (it[0] - 'A') to (it[2] - 'X') }
        // (player's symbol, player's base score)
        .map {
            (it.first + it.second - 1).mod(3) to it.second * 3
        }
        .map {it.first + 1 + it.second}
        .sum()
}


fun main() {
    val input = readInput(2).trim()
    println(part1(input))
    println(part2(input))
}