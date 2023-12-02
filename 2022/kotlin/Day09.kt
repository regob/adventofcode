import kotlin.math.abs
import kotlin.math.max

private fun sign(a: Int, b: Int) = if (b > a) 1 else -1

private fun newPos(head: Pair<Int, Int>, tail: Pair<Int, Int>): Pair<Int, Int> {
    val (tx, ty) = tail
    val (xDiff, yDiff) = abs(head.first - tx) to abs(head.second - ty)
    if (max(xDiff, yDiff) <= 1) return tail
    if (xDiff == 0) return tx to ty + sign(ty, head.second)
    if (yDiff == 0) return tx + sign(tx, head.first) to ty
    return tx + sign(tx, head.first) to ty + sign(ty, head.second)
}

private fun direction(ch: Char) = when (ch) {
    'U' -> 0 to -1
    'D' -> 0 to 1
    'L' -> -1 to 0
    'R' -> 1 to 0
    else -> throw IllegalArgumentException()
}

fun main() {
    val input = readInput(9).trim().lines()
    val inputPairs = input.map {
        val p = it.split(" ")
        p[0][0] to p[1].toInt()
    }

    // part1
    var h = 0 to 0
    var t = 0 to 0
    val fields = mutableSetOf(t)
    for ((ch, cnt) in inputPairs) {
        val diff = direction(ch)
        repeat(cnt) {
            h = h.first + diff.first to h.second + diff.second
            t = newPos(h, t)
            fields.add(t)
        }
    }
    println(fields.size)

    // part2
    val xs = MutableList(10) {0 to 0}
    fields.clear()
    for ((ch, cnt) in inputPairs) {
        val diff = direction(ch)
        repeat(cnt) {
            xs[0] = xs[0].first + diff.first to xs[0].second + diff.second
            var prev = xs[0]
            for (i in 1 until xs.size) {
                xs[i] = newPos(prev, xs[i])
                prev = xs[i]
            }
            fields.add(xs.last())
        }
    }
    println(fields.size)
}