private val opRegex = Regex("move (\\d+) from (\\d+) to (\\d+)")

fun main() {
    val input = readInput(5).trim().lines()
    val sepIdx = input.indexOfFirst {it.isBlank()}
    val N = input[sepIdx-1].trim().replace(" ", "").length

    val cols = List(N) { mutableListOf<Char>() }
    for (line in input.subList(0, sepIdx - 1)) {
        for ((i, pos) in (1 until line.length step 4).withIndex()) {
            if (line[pos] != ' ') {
                cols[i].add(line[pos])
            }
        }
    }
    val ops = input.subList(sepIdx + 1, input.size)
        .map {opRegex.matchEntire(it)!!.groupValues.drop(1).map {x -> x.toInt()}}

    // part1
    var c = cols.map {it.reversed().toMutableList()}
    for (op in ops) {
        repeat(op[0]) {
            val x = c[op[1] - 1].removeLast()
            c[op[2] - 1].add(x)
        }
    }
    println(c.map {it.last()}.joinToString(""))

    // part2
    c = cols.map {it.reversed().toMutableList()}
    for (op in ops) {
        val take = c[op[1] - 1].takeLast(op[0])
        repeat(op[0]) {c[op[1] - 1].removeLast()}
        c[op[2] - 1].addAll(take)
    }
    println(c.map {it.last()}.joinToString(""))

}