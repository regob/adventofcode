import kotlin.math.*

private typealias Shape = List<Pair<Int, Int>>
private val Width = 7

fun main() {
    val d = readInput(17).trim().map {if (it == '<') -1 else 1}
    val b = mutableListOf<Array<Int>>()
    var ptr = -1

    fun next(s: Shape): Shape {
        ptr += 1
        // left-right movement
        var s1 = s.map {it.first to it.second + d[ptr % d.size]}
        if (s1.any {it.second < 0 || it.second >= Width || b[it.first][it.second] != 0}) s1 = s
        // downwards movement
        val s2 = s1.map {it.first - 1 to it.second}
        if (s2.any {it.first < 0 || b[it.first][it.second] != 0}) return s1
        return s2
    }

    fun simulate(s: Shape): Shape {
        var (prev, nxt) = s to next(s)
        // while the shape goes down, we simulate it
        while (prev[0].first != nxt[0].first) {
            prev = nxt.also {nxt = next(nxt)}
        }
        return nxt
    }

    fun height() = b.indexOfLast {it.any {x -> x != 0}} + 1
    fun itemAt(idx: Long, y: Int): Shape = when (idx % 5) {
        0L -> (2..5).map {y to it}
        1L -> listOf(y to 3, y+1 to 2, y+1 to 3, y+1 to 4, y+2 to 3)
        2L -> listOf(y to 2, y to 3, y to 4, y+1 to 4, y+2 to 4)
        3L -> listOf(y to 2, y+1 to 2, y+2 to 2, y+3 to 2)
        4L -> listOf(y to 2, y to 3, y+1 to 2, y+1 to 3)
        else -> throw IllegalArgumentException("This is impossible, but the compiler does not know :(")
    }

    // part1
    for (i in 0 until 2022) {
        val h = height()
        val item = itemAt(i.toLong(), h + 3)
        // add new empty rows at the top, if needed
        repeat(max(0, item.maxOf {it.first} + 1 - h)) {
            b.add(Array(Width) {0})
        }
        val xitem = simulate(item)
        for (pt in xitem) {
            b[pt.first][pt.second] = 1
        }
    }
    println(height())

    // part2
    ptr = -1
    b.clear()
    data class State(val iMod: Int, val ptr: Int, val history: List<Int>)
    //
    val states = mutableMapOf<State, Pair<Long, Int>>()

    var (i, add) = 0L to 0L
    var history = listOf<Int>()
    val M = 1000000000000L
    while (i < M) {
        val h = height()
        val item = itemAt(i, h + 3)
        // add new empty rows at the top, if needed
        repeat(max(0, item.maxOf {it.first} + 1 - h)) {
            b.add(Array(Width) {0})
        }
        val xitem = simulate(item)
        val (dy, dx) = xitem[0].first - item[0].first to xitem[0].second - xitem[0].second

        if (history.size < 10) {
            history = history + listOf(dy, dx)
        } else if (add == 0L) {
            history = history.drop(2) + listOf(dy, dx)
            val state = State((i % 5).toInt(), ptr % d.size, history)

            // assume that if this state happened before, the events between will repeat periodically
            if (state in states) {
                val (iPrev, hPrev) = states[state]!!
                val period = i - iPrev
                add = (M - i) / period * (h - hPrev)
                i += period * ((M - i) / period)
            } else states[state] = i to h
        }

        for (pt in xitem) {
            b[pt.first][pt.second] = 1
        }
        i += 1
    }
    println(height() + add)
}