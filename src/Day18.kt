import kotlin.math.*
fun main() {
    val pts = readInput(18).trim().lines()
        .map {it.split(",").map {x -> x.toInt()}}.toSet()

    fun neighbors(pt: List<Int>): List<List<Int>> {
        val (x, y, z) = pt
        return listOf(listOf(x-1, y, z), listOf(x+1, y, z), listOf(x, y-1, z), listOf(x, y+1, z), listOf(x, y, z-1), listOf(x, y, z+1))
    }

    // part1
    println(pts.sumOf {
        neighbors(it).count {x -> x !in pts}
    })

    // part2
    val (mi, mx) = mutableListOf(10000, 10000, 10000) to mutableListOf(-10000, -10000, -10000)
    pts.forEach {
        for ((i, q) in it.withIndex()) {
            mi[i] = min(mi[i], q)
            mx[i] = max(mx[i], q)
        }
    }
    fun good(pt: List<Int>) = pt !in pts && pt.withIndex().all {it.value >= mi[it.index] - 1 && it.value <= mx[it.index] + 1}

    val outpts = mutableSetOf(mi.map {x -> x - 1})
    val q = mutableSetOf(mi.map {x -> x - 1})
    while (q.isNotEmpty()) {
        val pt = q.first().also {q.remove(it)}
        neighbors(pt).filter(::good)
            .filter {it !in outpts}
            .forEach {
                outpts.add(it)
                q.add(it)
            }
    }
    println(pts.sumOf {
        neighbors(it).count {x -> x !in pts && x in outpts}
    })
}