fun main() {
    val ops = mapOf<Char, (Long, Long) -> Long>(
        '/' to {x, y -> x / y},
        '*' to {x, y -> x * y},
        '-' to {x, y -> x - y},
        '+' to {x, y -> x + y}
    )
    abstract class Node {
        abstract fun value(): Long?
    }
    data class Value(val x: Long?) :Node() {
        override fun value() = x
    }
    data class Op(val l: Node, val r: Node, val op: Char) :Node() {
        override fun value(): Long? {
            val (lv, rv) = l.value() to r.value()
            return if (lv == null || rv == null) null else ops[op]!!(lv, rv)
        }
    }

    val r = "(\\w+): (\\d+|(\\w+) (.) (\\w+))".toRegex()
    val monkeys = readInput(21).trim().lines()
        .associate {
            val g = r.matchEntire(it)!!.groupValues
            if (g.subList(3, 6).all {s -> s.isBlank()}) g[1] to listOf(g[2]) else g[1] to g.subList(3, 6)
        }

    val nodes = mutableMapOf<String, Node>()
    fun parse(key: String): Node {
        val l = monkeys[key]!!
        if (l.size == 1) return Value(l[0].toLong())
        if (l[0] !in nodes) nodes[l[0]] = parse(l[0])
        if (l[2] !in nodes) nodes[l[2]] = parse(l[2])
        return Op(nodes[l[0]]!!, nodes[l[2]]!!, l[1].first())
    }
    monkeys.keys.forEach {
        if (it !in nodes) nodes[it] = parse(it)
    }

    // part1
    println(nodes["root"]!!.value())

    // part2
    nodes.clear()
    nodes["humn"] = Value(null)
    monkeys.keys.forEach {
        if (it !in nodes) nodes[it] = parse(it)
    }
    val root = nodes["root"]!! as Op

    // go down the tree where the value is null until we reach node 'humn', also store the value neeeded in the current node
    fun findValue(node: Node, curr: Long): Long {
        if (node === nodes["humn"]) return curr
        val n = node as Op
        val (lv, rv) = n.l.value() to n.r.value()
        return when (n.op) {
            '/' -> if (lv == null) findValue(n.l, curr * rv!!) else findValue(n.r, curr / lv)
            '*' -> if (lv == null) findValue(n.l, curr / rv!!) else findValue(n.r, curr / lv)
            '-' -> if (lv == null) findValue(n.l, curr + rv!!) else findValue(n.r, lv - curr)
            '+' -> if (lv == null) findValue(n.l, curr - rv!!) else findValue(n.r, curr - lv)
            else -> throw IllegalStateException()
        }
    }

    val target = (root.l.value()) ?: root.r.value()
    val node = if (root.l.value() == null) root.l else root.r
    println(findValue(node, target!!))
}