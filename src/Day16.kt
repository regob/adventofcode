import kotlin.math.max

private val r = Regex("Valve (..) has flow rate=([0-9]+); .* valves? (.*)")
private typealias EdgeList = List<Pair<Int, String>>

fun main() {
    val rates = mutableMapOf<String, Int>()
    val neighs = mutableMapOf<String, List<String>>()
    readInput(16).trim().lines()
        .forEach {s ->
            val groups = r.matchEntire(s)!!.groupValues
            val node = groups[1]
            val rate = groups[2].toInt()
            val neigh = groups[3].split(", ")
            rates[node] = rate
            neighs[node] = neigh
        }

    // compress the graph: all nodes with rate=0 and only two edges are transient:
    // e.g: 5 --- 0 ---- 0 ---- 9
    // transformed to: 5 --- 9 with an edge length of 3
    // most nodes are actually transient in the input
    val e = mutableMapOf<String, EdgeList>()
    val transientNodes = rates.filter {it.value == 0 && neighs[it.key]!!.size <= 2}.map {it.key}
    for ((node, neigh) in neighs) {
        if (node in transientNodes) continue
        val dist = mutableMapOf<String, Int>()
        for (n in neigh) {
            var (xnode, length) = n to 1
            var prev = node
            while (xnode in transientNodes) {
                val next = neighs[xnode]!!.first {it != prev}
                prev = xnode
                xnode = next
                length += 1
            }
            dist[xnode] = length
        }
        e[node] = dist.map {it.value to it.key}
    }

    val idx = e.keys.withIndex().associate { it.value to it.index }

    // memoize the search function
    data class CacheEntry(val node: String, val t: Int, val valves: Int, val rep: Int)
    val cache = mutableMapOf<CacheEntry, Int>()
    fun returnStore(entry: CacheEntry, ret: Int): Int {
        cache[entry] = ret
        return ret
    }

    var (initNode, initTime) = "AA" to 30

    fun search(node: String, t: Int, valves: Int, rep: Int=0): Int {
        val cacheEntry = CacheEntry(node, t, valves, rep-1)
        if (t <= 1) {
            if (rep > 0) returnStore(cacheEntry, search(node, t, valves, rep-1))
            return 0
        }
        if (cacheEntry in cache) return cache[cacheEntry]!!

        val g = e[node]!!
        val (rate, i) = rates[node]!! to idx[node]!!
        var best = 0

        if (rate > 0 && (valves and (1 shl i) == 0)) {
            val valv = valves or (1 shl i)
            val plus = (t-1) * rate

            // check other nodes `n` reached by an edge of length `w`
            for ((w, n) in g) {
                if (w >= t - 2) continue // no time for opening the valve after moving
                best = max(best, search(n, t - w - 1, valv, rep) + plus)
            }
            // no other moves, just open valve here, and stop
            best = max(best, plus)
        }

        // check moves to other nodes without opening the valve here
        for ((w, n) in g) {
            if (w >= t - 1) continue
            best = max(best, search(n, t - w, valves, rep))
        }
        // if absolutely no other moves can be made, and we have repetitions left, check the next rep
        if (g.all {it.first >= t - 1} && rep > 0)
            return returnStore(cacheEntry,
                best + search(initNode, initTime, valves, rep-1))

        return returnStore(cacheEntry, best)
    }

    // part1
    println(search(initNode, initTime, 0, 0))

    // part2
    initTime = 26
    println(search(initNode, initTime, 0, 1))
}