import kotlin.math.abs
import kotlin.math.max
import kotlin.math.min

private fun part1(entries: List<List<Int>>, Y: Int = 2000000) {
    val beaconsAt = mutableSetOf<Int>()
    val s = mutableSetOf<Int>()
    for (e in entries) {
        val dist = abs(e[0] - e[2]) + abs(e[1] - e[3])
        if (abs(Y - e[1]) > dist) continue
        if (e[3] == Y) beaconsAt.add(e[2])
        val xMin = e[0] - (dist - abs(Y - e[1]))
        val xMax = e[0] + (dist - abs(Y - e[1]))
        for (x in xMin..xMax) s.add(x)
    }
    println(s.size - beaconsAt.size)
}

private fun part2(entries: List<List<Int>>, N: Int = 4000000) {
    val ys = List(N + 1) { mutableListOf<Long>() }
    for (e in entries) {
        val dist = abs(e[0] - e[2]) + abs(e[1] - e[3])
        val yMin = max(0, e[1] - dist)
        val yMax = min(e[1] + dist, N)

        // for each y, add the range of x to ys, so that the distance of
        // point (x, y) from the current entry is at most `dist`
        // ranges are stored as xMin * (N+1) + xMax instead of Pair(xMin, yMin) for smaller memory footstep
        for (y in yMin..yMax) {
            val xMin = max(0, e[0] - (dist - abs(y - e[1])))
            val xMax = min(e[0] + (dist - abs(y - e[1])), N)
            ys[y].add(xMin.toLong() * (N + 1) + xMax)
        }
    }
    for (y in 0..N) {
        if (y % 100000 == 0) println("----- $y -----")
        var x = 0L
        for (xr in ys[y].sorted()) {
            val (xMin, xMax) = xr / (N + 1) to xr % (N + 1)
            if (x < xMin) break
            x = max(x, xMax + 1)
        }
        if (x <= N) {
            println(x * N + y.toLong())
            break
        }
    }
}

fun main() {
    val regex = Regex("Sensor at x=([-0-9]+), y=([-0-9]+): closest beacon is at x=([-0-9]+), y=([-0-9]+)")
    val entries = readInput(15).trim().lines()
        .map {
            val gr = regex.matchEntire(it)!!.groupValues.drop(1)
            gr.map {x -> x.toInt()}
        }

    // separate
    part1(entries)
    part2(entries)

}