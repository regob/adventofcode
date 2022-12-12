import kotlin.math.max
import kotlin.math.min

fun main() {
    val input = readInput(4).trim().lines()
        .map {
            val (a, b) = it.split(",")
            val r1 = a.split("-").map {x -> x.toInt()}
            val r2 = b.split("-").map {x -> x.toInt()}
            listOf(r1[0], r1[1], r2[0], r2[1])
        }

    // part1
    val total1 = input.count {(x1, x2, y1, y2) ->
        (x1 <= y1 && x2 >= y2) || (x1 >= y1 && x2 <= y2)
    }
    println(total1)

    // part2
    // intervals overlap = both start points come before both end points (or equal)
    val total2 = input.count {(x1, x2, y1, y2) ->
        max(x1, y1) <= min(x2, y2)
    }
    println(total2)
}