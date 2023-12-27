fun main() {
    val input = readInput(20).trim().lines()
        .map {it.toInt()}
    val N = input.size
    val idxes = listOf(1000, 2000, 3000)

    fun solve(x: MutableList<Pair<Long, Int>>, rep: Int = 1): Long {
        repeat(rep) {
            for (i in 0 until N) {
                // find where's the item originally at index `i`
                var j = 0
                while (x[j].second != i) j++
                // N-1 rotations don't do anything in either direction
                val rot = x[j].first % (N - 1)
                var nj = j + rot
                // if rotation happens at the end, jumping one more pos (as in the examples) ...
                if (nj < 0 || (nj == 0L && j != 0)) nj -= 1
                else if (nj >= N) nj += 1
                val jj = ((nj + N) % N).toInt()

                val curr = x[j]
                if (jj > j) {
                    for (k in j until jj) x[k] = x[k+1]
                } else {
                    for (k in j downTo jj + 1) x[k] = x[k-1]
                }
                x[jj] = curr
            }
        }
        val zero = x.indexOfFirst {it.first == 0L}
        return idxes.sumOf { x[(zero + it) % N].first }
    }

    // part1
    val x1 = input.withIndex().map {it.value.toLong() to it.index}.toMutableList()
    println(solve(x1))

    // part2
    val x2 = input.withIndex().map {it.value.toLong() * 811589153 to it.index}.toMutableList()
    println(solve(x2, 10))
}