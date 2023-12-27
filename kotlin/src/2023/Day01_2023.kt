private val sdigits = mapOf(
    "one" to 1,
    "two" to 2,
    "three" to 3,
    "four" to 4,
    "five" to 5,
    "six" to 6,
    "seven" to 7,
    "eight" to 8,
    "nine" to 9,
)

private fun digitAtStart(s: String, i: Int): Int? {
    val seq = s.subSequence(i until s.length)
    for ((sdig, dig) in sdigits.entries) {
        if (seq.startsWith(sdig)) return dig
    }
    if (seq[0].isDigit()) return seq[0].digitToInt()
    return null
}

fun main() {
    val input = readInput(1, 2023)
    val lines = input.trim().split("\n")

    val res1 = lines.asSequence()
        .map {
            line -> line.first {it.isDigit()}.toString() + line.last {it.isDigit()}
        }
        .map {it.toInt()}
        .sum()
    println("Part 1: $res1")

    var res2 = 0
    for (line in lines) {
        var (first_dig, last_dig) = -1 to -1
        for (i in line.indices) {
            val dig = digitAtStart(line, i)
            if (dig != null) {
                last_dig = dig
                if (first_dig < 0) first_dig = dig
            }
        }
        res2 += first_dig * 10 + last_dig
    }
    println("Part 2: $res2")



}