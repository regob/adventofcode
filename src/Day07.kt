
data class Node(val parent: Node?, val children: MutableMap<String, Node> = mutableMapOf(), var size: Int = 0)

fun calcTotalSize(node: Node, acc: MutableList<Int>): Int {
    var total = node.children.values.sumOf {
        calcTotalSize(it, acc)
    }
    total += node.size
    acc.add(total)
    return total
}

fun main() {
    val input = readInput(7).trim()
    val cmds = input.split("$").asSequence()
        .filter {it.isNotBlank()}
        .map {
            it.lines()
                .map(String::trim)
                .filter {x -> x.isNotBlank() }
        }


    val root = Node(null)
    var cur = root
    for (cmdLines in cmds) {
        val cmd = cmdLines[0]
        when (cmd) {
            "ls" ->  cmdLines.subList(1, cmdLines.size).forEach {
                val (x, y) = it.split(" ")
                if (x == "dir") cur.children[y] = Node(cur)
                else cur.size += x.toInt()
            }
            else -> when(val tar = cmd.split(" ")[1]) {
                "/" -> cur = root
                ".." -> cur = cur.parent!!
                else -> cur = cur.children[tar]!!
            }
        }
    }

    val totals = mutableListOf<Int>()
    val total = calcTotalSize(root, totals)

    // part1
    println(totals.filter {it <= 100000}.sum())

    // part2
    val minSize = 30000000 - (70000000 - total)
    val res = totals.asSequence()
        .filter {it >= minSize}
        .min()
    println(res)
}