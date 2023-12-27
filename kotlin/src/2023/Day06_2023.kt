
private fun waysToWin(t: Long, record: Long): Int {
    return (1..<t)
        .map {it * (t - it)}
        .count {it > record}
}

fun main() {
    val input = readInput(6, 2023).trim().split("\n")
    val p = "\\s+(\\d+)"
    val pat = Regex("(\\w+):$p$p$p$p")

    val times = pat.matchEntire(input[0])!!.groupValues.drop(2)
    val dists = pat.matchEntire(input[1])!!.groupValues.drop(2)

    times.zip(dists)
        .map {waysToWin(it.first.toLong(), it.second.toLong())}
        .reduce {x, y -> x * y}
        .also {println("Part 1: $it")}

    val time = times.joinToString("").toLong()
    val dist = dists.joinToString("").toLong()
    val res = waysToWin(time, dist)
    println("Part 2: $res")

}