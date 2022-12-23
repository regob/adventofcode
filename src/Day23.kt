fun main() {
    data class P(val x: Int, val y: Int)
    val init = mutableSetOf<P>()
    readInput(23).trim()
        .lines().withIndex().forEach {
            it.value.withIndex().forEach {itc ->
                if (itc.value == '#') init.add(P(itc.index, it.index))
            }
        }
    var e = init.toMutableSet()

    val constraints = mutableListOf(
        listOf(P(-1, -1), P(0, -1), P(1, -1)) to P(0, -1),
        listOf(P(0, 1), P(-1, 1), P(1, 1)) to P(0, 1),
        listOf(P(-1, 0), P(-1, -1), P(-1, 1)) to P(-1, 0),
        listOf(P(1, 0), P(1, -1), P(1, 1)) to P(1, 0),
    )
    val neigh = listOf(P(-1, -1), P(0, -1), P(1, -1), P(-1, 0), P(1, 0), P(-1, 1), P(0, 1), P(1, 1))
    fun stepConstraints() = constraints.add(constraints.removeFirst())
    fun next(p: P): P {
        if (neigh.all {P(p.x + it.x, p.y + it.y) !in e}) return p
        val diff = constraints.firstOrNull {it.first.all {ap -> P(ap.x + p.x, ap.y + p.y) !in e}}?.second
        if (diff != null) return P(p.x + diff.x, p.y + diff.y)
        return p
    }

    fun simulate(n: Int, part2: Boolean): Int {
        for (rep in 1..n) {
            val d = mutableMapOf<P, MutableList<P>>()
            for (p in e) {
                d.getOrPut(next(p)) { mutableListOf() }.add(p)
            }
            val ne = mutableSetOf<P>()
            var moved = false
            for ((p, pts) in d.entries) {
                if (pts.size == 1) {
                    ne.add(p)
                    if (p != pts.first()) moved = true
                }
                else for (pt in pts) ne.add(pt)
            }
            e = ne
            stepConstraints()
            if (part2 && !moved) return rep
        }
        return n
    }

    // part1
    simulate(10, part2 = false)
    val (xmin, xmax) = e.minOf {p -> p.x} to e.maxOf {p -> p.x}
    val (ymin, ymax) = e.minOf {p -> p.y} to e.maxOf {p -> p.y}
    println((xmax - xmin + 1) * (ymax - ymin + 1) - e.size)

    // part2
    e = init
    while (constraints.first().second != P(0, -1)) stepConstraints()
    println(simulate(Int.MAX_VALUE, part2 = true))
}