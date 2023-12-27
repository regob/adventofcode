
private fun parseItems(s: String): List<Int> {
    return s.trim().replace(Regex("\\s+"), " ").split(" ").map {it.toInt()}
}
fun main() {
    val input = readInput(4, 2023)
    val gamePat = Regex("Card\\s+([0-9]+): (.*) \\| (.*)")

    val games = input.trim().split("\n")
        .map {gamePat.matchEntire(it)!!.groupValues}
        .map {parseItems(it[2]).toSet() to parseItems(it[3]).toSet()}

    games.asSequence()
        .map {it.first.intersect(it.second).size}
        .sumOf {if (it == 0) 0 else 1 shl (it - 1)}
        .also {println("Part 1: $it")}

    val cnt = MutableList(games.size) {1}

    for (i in cnt.indices) {
        val win = games[i].first.intersect(games[i].second).size
        for (j in (i + 1)..(i + win)) {
            cnt[j] += cnt[i]
        }
    }

    println("Part 2: ${cnt.sum()}")


}