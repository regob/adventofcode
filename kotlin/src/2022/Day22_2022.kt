private data class P(val x: Int, val y: Int)

fun main() {
    val input = readInput(22).lines()
    val board = mutableMapOf<P, Int>() // wall = 2, empty field = 1, nothing = not in map
    val N = input.indexOfFirst {it.isBlank()}
    val M = input.take(N).maxOf {it.length}
    input.take(N).withIndex().forEach {
        it.value.withIndex().forEach {x ->
            if (x.value != ' ') board[P(x.index + 1, it.index + 1)] = if (x.value == '#') 2 else 1
        }
    }
    val moves = "(\\d+)([A-Z])?".toRegex().findAll(input[N + 1])
        .flatMap {
            it.groupValues.drop(1).filter {x -> x.isNotBlank()}
        }.toList()

    //////////////////// part1 ////////////////////
    fun next(p: P, dx: Int, dy: Int, jump: (P, Int, Int) -> P?): P? {
        val np = jump(p, dx, dy) ?: P(p.x + dx, p.y + dy)
        return if (board[np] == 2) null else np
    }

    val faces = listOf('R', 'D', 'L', 'U')
    val diff = mapOf('R' to P(1, 0), 'L' to P(-1, 0), 'U' to P(0, -1), 'D' to P(0, 1))

    var p = P((1..M).first {P(it, 1) in board}, 1)
    var face = 'R'

    for (move in moves) {
        if (move.first().isLetter()) {
            face = faces[((faces.indexOf(face) + if (move.first() == 'R') 1 else -1) + 4) % 4]
            continue
        }
        for (u in 0 until move.toInt()) {
            val (dx, dy) = diff[face]!!

            val np = next(p, dx, dy) { p, dx, dy ->
                // if edge of the board, jump else, don't
                if (P(p.x + dx, p.y + dy) in board) null
                else {
                    var npp = P(
                        if (dx == 0) p.x else (if (dx > 0) 0 else M),
                        if (dy == 0) p.y else (if (dy > 0) 0 else N)
                    )
                    while (npp !in board) npp = P(npp.x + dx, npp.y + dy)
                    npp
                }
            } ?: break
            p = np
        }
    }
    println(p.y * 1000 + p.x * 4 + faces.indexOf(face))

    //////////////////// part2 ////////////////////
    p = P((1..M).first {P(it, 1) in board}, 1)
    face = 'R'

    // | AB|
    // | C |
    // |DE |
    // |F  |
    fun jump(x: Int, y: Int, dx: Int, dy: Int): Pair<P, Char>? {
        // A
        if (x == 51 && y in 1..50 && dx < 0) return P(1, 151 - y) to 'R'
        if (x in 51..100 && y == 1 && dy < 0) return P(1, 150+x-50) to 'R'
        // B
        if (x == 150 && y in 1..50 && dx > 0) return P(100, 100+(51-y)) to 'L'
        if (x in 101..150 && y == 1 && dy < 0) return P(x - 100, 200) to 'U'
        if (x in 101..150 && y == 50 && dy > 0) return P(100, 50+x-100) to 'L'
        // C
        if (x == 100 && y in 51..100 && dx > 0) return P(100 + y - 50, 50) to 'U'
        if (x == 51 && y in 51..100 && dx < 0) return P(y - 50, 101) to 'D'
        // D
        if (y == 101 && x in 1..50 && dy < 0) return P(51, 50+x) to 'R'
        if (y in 101..150 && x == 1 && dx < 0) return P(51, 151-y) to 'R'
        // E
        if (x == 100 && y in 101..150 && dx > 0) return P(150, 151-y) to 'L'
        if (x in 51..100 && y == 150 && dy > 0) return P(50, 150+x-50) to 'L'
        // F
        if (x == 1 && y in 151..200 && dx < 0) return P(50 + y - 150, 1) to 'D'
        if (x in 1..50 && y == 200 && dy > 0) return P(100 + x, 1) to 'D'
        if (x == 50 && y in 151..200 && dx > 0) return P(50 + y - 150, 150) to 'U'
        return null
    }

    for (move in moves) {
        if (move.first().isLetter()) {
            face = faces[((faces.indexOf(face) + if (move.first() == 'R') 1 else -1) + 4) % 4]
            continue
        }
        for (u in 0 until move.toInt()) {
            val (dx, dy) = diff[face]!!
            var newface: Char? = face
            val np = next(p, dx, dy) { p, dx, dy ->
                val q = jump(p.x, p.y, dx, dy)
                if (q != null) newface = q.second
                q?.first
            } ?: break
            face = newface!!
            p = np
        }
    }
    println(p.y * 1000 + p.x * 4 + faces.indexOf(face))
    
}