fun main() {
    val input = readInput(1)
    val totals = input.trim().split("\n\n")
        .map {
            it.split("\n").map {x -> x.toInt()}
        }
        .map {it.sum()}
        .sortedDescending()
    println(totals.first())
    println(totals.take(3).sum())
}
