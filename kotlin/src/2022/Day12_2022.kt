import java.util.ArrayDeque

private fun height(chr: Char) = when (chr) {
    'S' -> 0
    'E' -> 25
    else -> chr - 'a'
}

private fun neighbors(y: Int, x: Int, yMax: Int, xMax: Int): List<Pair<Int, Int>> =
    listOf(y to x - 1, y to x + 1, y - 1 to x, y + 1 to x)
        .filter {it.first >= 0 && it.second >= 0 && it.first < yMax && it.second < xMax}


private fun findDist(start: List<Pair<Int, Int>>, M: List<List<Int>>, target: Pair<Int, Int>): Int {
    val q = ArrayDeque(start)
    val D = Array(M.size) {Array(M[0].size) {-1} }
    for (p in start) D[p.first][p.second] = 0
    while (q.isNotEmpty()) {
        val p = q.removeLast()
        for (tar in neighbors(p.first, p.second, M.size, M[0].size)) {
            if (M[tar.first][tar.second] > M[p.first][p.second] + 1) continue
            if (D[tar.first][tar.second] >= 0) continue
            q.addFirst(tar)
            D[tar.first][tar.second] = D[p.first][p.second] + 1
        }
    }
    return D[target.first][target.second]
}

fun main() {
    val input = readInput(12).trim().lines()
    val M = input.map {
            it.toList().map(::height)
        }

    fun posOf(chr: Char): Pair<Int, Int> {
        for (y in M.indices)
            for (x in M[0].indices)
                if (input[y][x] == chr) return y to x
        return -1 to -1
    }

    // part1
    val start1 = listOf(posOf('S'))
    val target = posOf('E')
    println(findDist(start1, M, target))

    // part2
    val start2 = mutableListOf<Pair<Int, Int>>()
    for (y in M.indices)
        for (x in M[0].indices)
            if (M[y][x] == 0) start2.add(y to x)
    println(findDist(start2, M, target))
}