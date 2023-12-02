import kotlin.math.*

data class State(val resources: List<Int>, val robots: List<Int>, val t: Int)

// ore, clay, obsidian, geode
fun maxGeodes(resources: List<Int>, robots: List<Int>, t: Int, costs: List<List<Int>>): Int {
    val cache = mutableMapOf<State, Int>()
    var allBest = 0 // best solution found yet
    var currentRes = 0 // result on the current path without the current node

    // maximum amount of each robot
    val maxRobot = robots.indices.map {i -> costs.maxOf {it[i]}}

    // maximum geodes that can be produced in the remaining time
    val maxGeodeLeft = (0..t).map {it * (it - 1) / 2}

    fun dfs(res: List<Int>, rob: List<Int>, t: Int, buildSkipped: List<Int> = emptyList()): Int {
        if (t <= 1) return 0
        if (t == 2) return if (res.indices.any {res[it] < costs[3][it]}) 0 else 1
        val state = State(res, rob, t)
        if (state in cache) return cache[state]!!

        // if we cannot improve the best solution, even if we build geode robots all the time, cut this branch
        if (currentRes + maxGeodeLeft[t] <= allBest) return -1
        var branchCut = false

        var best = 0
        val possibleRobots = costs.indices.asSequence()
            .filter {r -> r !in buildSkipped}
            .filter {r -> res.zip(costs[r]).all {it.first >= it.second}}
            .filter {r -> r == 3 || rob[r] < maxRobot[r]}
            .toList()

        for (r in possibleRobots) {
            val new_res = res.indices.map {res[it] + rob[it] - costs[r][it]}
            val new_rob = rob.indices.map {if(it == r) rob[it] + 1 else rob[it]}

            // if new robot is geode robot, it produces t-1 geodes in total
            val curr = if (r == 3) {
                currentRes += t - 1
                (dfs(new_res, new_rob, t-1) + t-1).also {currentRes -= t - 1}
            } else {
                dfs(new_res, new_rob, t-1)
            }
            if (curr < 0) branchCut = true
            else best = max(best, curr)
        }
        // we can also skip building anything
        val new_res = res.indices.map {res[it] + rob[it]}
        dfs(new_res, rob, t-1, possibleRobots).let {
            if (it < 0) branchCut = true
            else best = max(best, it)
        }

        if (!branchCut) cache[state] = best
        allBest = max(allBest, best + currentRes)
        return best
    }
    return dfs(resources, robots, t)
}

fun main() {
    val bps = readInput(19).trim().lines()
        .map {"\\d+".toRegex().findAll(it).map {it.groupValues[0].toInt()}.toList()}
        .map {
            bp -> bp[0] to listOf(listOf(bp[1], 0, 0), listOf(bp[2], 0, 0), listOf(bp[3], bp[4], 0), listOf(bp[5], 0, bp[6]))
        }

    // part1
    println(bps.sumOf {
        it.first * maxGeodes(listOf(0, 0, 0), listOf(1, 0, 0), 24, costs=it.second)
    })

    // part2
    println(bps.take(3).map {
        maxGeodes(listOf(0, 0, 0), listOf(1, 0, 0), 32, costs=it.second)
    }.reduce {x, y -> x * y})
}