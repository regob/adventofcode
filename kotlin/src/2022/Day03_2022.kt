
private fun prio(chr: Char) =
    if (chr in 'a'..'z') chr - 'a' + 1
    else chr - 'A' + 27

fun main() {
    val input = readInput(3).trim().lines()

    // part1
    val total = input.asSequence().map { s ->
        s.substring(0 until s.length / 2) to s.substring(s.length / 2 until s.length)
    }.map {
        it.first.toSet().intersect(it.second.toSet()).first()
    }.map(::prio).sum()
    println(total)

    // part2
    var total2 = 0
    for (i in input.indices step 3) {
        val sets = input.subList(i, i + 3).map {it.toSet()}
        val c = sets.reduce {s1, s2 ->
            s1.intersect(s2)
        }.first()
        total2 += prio(c)
    }
    println(total2)
}