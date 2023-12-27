import kotlin.math.max

private fun parseItem(s: String): Pair<String, Int> {
    val (cnt, typ) = s.trim().split(" ")
    return typ to cnt.toInt()
}

private fun parseGame(s: String): List<Map<String, Int>> {
    return s.split(";")
        .map {
            its -> its.split(",")
            .associate {parseItem(it)}
        }
}

fun main() {
    val input = readInput(2, 2023)
    val game_pat = Regex("Game ([0-9]+): (.*)")
    val games = input.trim().split("\n")
        .map {game_pat.matchEntire(it)!!.groups.toList()}
        .map {it[1]!!.value.toInt() to parseGame(it[2]!!.value)}

    val items_have = mapOf(
        "red" to 12,
        "green" to 13,
        "blue" to 14,
    )
    games
        .filter {
            game -> game.second.all {
                it.entries.all {(k, v) -> v <= items_have[k]!!}
            }
        }
        .sumOf {it.first }
        .also {println("Part 1: $it")}

    fun updateBagReq(d: Map<String, Int>, hand: Map<String, Int>): Map<String, Int> {
        val newd = d.toMutableMap()
        for ((k, v) in hand.entries) newd[k] = max(newd.getOrDefault(k, 0), v)
        return newd
    }

    games.map { (idx, bags) ->
        bags.fold(mapOf(), ::updateBagReq)
    }
        .map {
            it.values.reduce {x, y -> x * y}
        }
        .sum()
        .also {println("Part 2: $it")}

}