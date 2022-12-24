
fun main() {
    val chMap = listOf('<', '^', '>', 'v').withIndex().associate {it.value to (1 shl it.index)}
    val input = readInput(24).trim().lines()
    val mStart = input.map {
        it.map {ch -> chMap.getOrDefault(ch, 0)}
    }
    val (N, M) = mStart.size to mStart[0].size

    // directions for each type of blizzard
    val dirs = listOf(0 to -1, -1 to 0, 0 to 1, 1 to 0).withIndex().associate {(1 shl it.index) to it.value}

    fun nextMap(m: List<List<Int>>) = run {
        val nm = List(N) { MutableList(M) { 0 } }
        for (i in m.indices)
            for (j in m[0].indices)
                for ((k, dir) in dirs.entries) {
                    // blizzard of direction `k` is not present at pos (i, j)
                    if (m[i][j] and k == 0) continue
                    var (y, x) = i + dir.first to j + dir.second
                    // if the blizzard reached a wall, it wraps at the other end (first and last coords are walls)
                    if (y == 0) y = N - 2
                    else if (y == N - 1) y = 1
                    if (x == 0) x = M - 2
                    else if (x == M - 1) x = 1
                    nm[y][x] = nm[y][x] or k
                }
        nm
    }

    val start = 0 to input[0].indexOf('.')
    val target = N - 1 to input[N-1].indexOf('.')

    fun neighbors(i: Int, j: Int) = listOf(i + 1 to j, i - 1 to j, i to j - 1, i to j + 1)
        .filter {p ->
            p == start || p == target || (p.first > 0 && p.second > 0 && p.first < N - 1 && p.second < M - 1)
        }


    // part 1
    var fields = setOf(start)
    var m = mStart
    for (t in 1..Int.MAX_VALUE) {
        m = nextMap(m)
        val s = mutableSetOf<Pair<Int, Int>>()
        for ((i, j) in fields) {
            if (m[i][j] == 0) s.add(i to j)
            // try moving in each direction
            for ((y, x) in neighbors(i, j))
                if (m[y][x] == 0) s.add(y to x)
        }

        if (target in s) {
            println(t)
            break
        }
        fields = s
    }

    // part 2
    fields = setOf(start)
    m = mStart
    // phase0: start -> target, phase1: target -> start, phase2: start -> target
    var phase = 0
    for (t in 1..Int.MAX_VALUE) {
        m = nextMap(m)
        var s = mutableSetOf<Pair<Int, Int>>()
        for ((i, j) in fields) {
            if (m[i][j] == 0) s.add(i to j)
            for ((y, x) in neighbors(i, j))
                if (m[y][x] == 0) s.add(y to x)
        }

        if (phase % 2 == 0 && target in s) {
            s = mutableSetOf(target)
            phase += 1
        } else if (phase % 2 == 1 && start in s) {
            s = mutableSetOf(start)
            phase += 1
        }
        if (phase > 2) {
            println(t)
            break
        }

        fields = s
    }
}