
fun main() {
    val lines = readInput(25).trim().lines()

    val digitToSnafu = mapOf(-2 to '=', -1 to '-', 0 to '0', 1 to '1', 2 to '2')
    val snafuToDigit = digitToSnafu.entries.associate {it.value to it.key}

    // solution 1: sum the numbers by coordinates, then normalize the answer
    val N = lines.maxOf {it.length} // max number length
    val digits = MutableList(N) {0}
    lines.forEach {
        it.reversed().forEachIndexed {i, ch -> digits[i] += snafuToDigit[ch]!!}
    }
    // normalize each digit to be in the valid [-2, 2] range
    var i = 0
    while (i < digits.size) {
        // if digit > 2, carry is positive; if digit < -2 carry is negative
        val carry = when {
            digits[i] < -2 -> - (2 - digits[i]) / 5
            digits[i] in -2..2 -> 0
            else -> (digits[i] + 2) / 5
        }
        if (carry != 0) {
            digits[i] -= carry * 5
            if (digits.size == i + 1) digits.add(carry)
            else digits[i+1] += carry
        }
        i += 1
    }
    println(digits.reversed().map {digitToSnafu[it]}.joinToString(""))

    // solution 2: convert the numbers to long, then convert their sum back into SNAFU
    // this is easier, but with enough numbers even longs could overflow ...
    fun toLong(snafu: String): Long {
        var (total, pow) = 0L to 1L
        for (i in snafu.indices.reversed()) {
            total += snafuToDigit[snafu[i]]!! * pow
            pow *= 5
        }
        return total
    }

    val remToDigit = listOf(0, 1, 2, -2, -1) // map remainders of [0,4] to [-2,2] so that if we subtract the latter we get a num divisible by 5
    fun toSnafu(num: Long): String {
        val snafu = mutableListOf<Char>()
        var x = num
        while (x > 0) {
            val digit = remToDigit[(x % 5).toInt()]
            snafu.add(digitToSnafu[digit]!!)
            x = (x - digit) / 5
        }
        return snafu.reversed().joinToString("")
    }
    val total = lines.map(::toLong).sum()
    println(toSnafu(total))
}