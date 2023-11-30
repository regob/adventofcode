import kotlin.math.sign

private data class Point(val x: Int, val y: Int)

private fun next(p: Point, m: Map<Point, Int>, yMax: Int) : Point? {
    if (p.y + 1 >= yMax) return null
    for (pt in listOf(Point(p.x, p.y + 1), Point(p.x - 1, p.y + 1), Point(p.x + 1, p.y + 1)))
        if (pt !in m) return pt
    return null
}

fun main() {
    val input = readInput(14).trim().lines()

    // 1 -> rock, 2 -> sand, not in map (-1) -> air
    val M = mutableMapOf<Point, Int>()
    input.forEach {
        val pts = it.split(" -> ").map { x ->
            val ps = x.split(",")
            Point(ps[0].toInt(), ps[1].toInt())
        }

        for ((pStart, pEnd) in pts.dropLast(1).zip(pts.drop(1))) {
            val (xstep, ystep) = (pEnd.x - pStart.x).sign to (pEnd.y - pStart.y).sign
            M[pStart] = 1
            var p = pStart
            while (p != pEnd) {
                p = Point(p.x + xstep, p.y + ystep)
                M[p] = 1
            }
        }
    }

    val yMax = M.maxOf {it.key.y} + 2

    // part1
    var m = M.toMutableMap()
    var cnt = 0
    while (true) {
        var p = Point(500, 0)
        var np = next(p, m, yMax)
        while (np != null) {
            p = np
            np = next(p, m, yMax)
        }
        if (p.y == yMax - 1) break
        cnt += 1
        m[p] = 2
    }
    println(cnt)

    // part2
    m = M.toMutableMap()
    cnt = 0
    while (true) {
        var p = Point(500, 0)
        var np = next(p, m, yMax)
        while (np != null) {
            p = np
            np = next(p, m, yMax)
        }
        cnt += 1
        m[p] = 2
        if (p == Point(500, 0)) break
    }
    println(cnt)
}