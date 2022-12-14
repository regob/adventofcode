private typealias Item = Any

private fun parse(s: String): Item {
    val path = mutableListOf<MutableList<Item>>()
    var acc = mutableListOf<Char>()

    fun closeAcc() {
        if (acc.isNotEmpty())
            path.last().add(acc.joinToString("").toInt())
        acc = mutableListOf()
    }

    for (c in s) {
        when (c) {
            in '0'..'9' -> {
                acc.add(c)
            }
            '[' -> {
                path.add(mutableListOf())
            }
            ']' -> {
                closeAcc()
                if (path.size == 1) return path.last()
                val l = path.removeLast()
                path.last().add(l)
            }
            ',' -> closeAcc()
            ' ' -> closeAcc()
            else -> throw IllegalStateException("Got char: $c")
        }
    }
    throw IllegalStateException("List not closed.")
}


private fun Item.compare(y: Item): Int {
     if (this is Int && y is Int) return this.compareTo(y)
     if (this is Int) return listOf(this).compare(y)
     if (y is Int) return this.compare(listOf(y))
     val (l1, l2) = this as List<Item> to y as List<Item>
     for ((a, b) in l1.zip(l2)) {
         val comp = a.compare(b)
         if (comp != 0) return comp
     }
     return l1.size.compareTo(l2.size)
}

fun main() {
    val input = readInput(13).trim().split("\n\n")
        .map {it.trim().split("\n")}

    // part1
    val total = input
        .map {
            parse(it[0]) to parse(it[1])
        }
        .withIndex()
        .map {e ->
            if (e.value.first.compare(e.value.second) < 0) e.index + 1 else 0
        }.sum()
    println(total)

    // part2
    val barriers = listOf(parse("[[2]]"), parse("[[6]]"))
    val sorted = (input.flatten().map(::parse) + barriers)
        .sortedWith { p0, p1 -> p0.compare(p1)}

    val (i1, i2) = barriers.map {sorted.indexOf(it)}
    println((i1 + 1) * (i2 + 1))
}