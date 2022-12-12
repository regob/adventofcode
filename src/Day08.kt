import kotlin.math.max

typealias Mat = List<List<Int>>

fun Mat.transpose(): Mat {
    val res = List<MutableList<Int>>(size) { mutableListOf() }

    for (j in indices)
        for (i in indices)
            res[j].add(this[i][j])
    return res
}

fun Mat.hflip(): Mat = map {it.asReversed()}

////////////////////////////////// part1 ///////////////////////////////
fun Mat.visibleFromLeft(): Mat {
    val res = List<MutableList<Int>>(size) { mutableListOf() }
    for (i in indices) {
        var mx = -1
        for (j in indices) {
            if (this[i][j] <= mx) res[i].add(0)
            else {
                mx = this[i][j]
                res[i].add(1)
            }
        }
    }
    return res
}

private fun part1(m: Mat): Int {
    val sides = listOf(
        m.visibleFromLeft(),
        m.hflip().visibleFromLeft().hflip(),
        m.transpose().visibleFromLeft().transpose(),
        m.transpose().hflip().visibleFromLeft().hflip().transpose(),
    )
    // count (i, j) indices where at least one element is > 0
    var cnt = 0
    for (i in m.indices)
        for (j in m[i].indices)
            for (mat in sides)
                if (mat[i][j] > 0) {
                    cnt += 1
                    break
                }
    return cnt
}

////////////////////////////////// part2 ///////////////////////////////

fun Mat.scoreFromLeft(): Mat {
    val res = List<MutableList<Int>>(size) { mutableListOf() }
    for (i in indices) {
        var highIdx = -1
        for (j in indices) {
            if (highIdx < 0 || this[i][j] > this[i][highIdx]) {
                res[i].add(j)
                highIdx = j
            }
            else res[i].add(j - highIdx)
            if (this[i][j] == this[i][highIdx]) highIdx = j
        }
    }
    return res
}

private fun part2(m: Mat): Int {
    val sides = listOf(
        m.scoreFromLeft(),
        m.hflip().scoreFromLeft().hflip(),
        m.transpose().scoreFromLeft().transpose(),
        m.transpose().hflip().scoreFromLeft().hflip().transpose(),
    )
    // get (i,j) with the highest score multiplied from all sides
    var best = 0
    for (i in m.indices)
        for (j in m[i].indices) {
            val scores = sides.map {it[i][j]}
            val score = scores.reduce {acc, x -> acc * x}
            best = max(best, score)
        }
    return best
}


fun main() {
    val input = readInput(8).trim()
    val m: List<List<Int>> = input.lines()
        .map {
            it.toList().map { it.digitToInt() }
        }
    println(part1(m))
    println(part2(m))
}