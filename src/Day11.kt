val itemsRegex = Regex(".*items: (.*)")
val opRegex = Regex("Operation: new = ([a-z0-9]+) ([+-/*]) ([a-z0-9]+)")
val testRegex = Regex(".*divisible by (\\d+)")
val decRegex = Regex(".*throw to monkey (\\d+)")

class Monkey(lines: List<String>) {
    var items: MutableList<Long>
    val operation: (Long) -> Long
    val test: (Long) -> Boolean
    val decision: Pair<Int, Int>
    val mod: Int

    // if the token is 'old', return `it` else the token's integer value
    private fun v(token: String, it: Long) = if (token == "old") it else token.toLong()

    init {
        val r1 = itemsRegex.matchEntire(lines[1].trim())!!
        items = r1.groups[1]!!.value.split(",").map {it.trim().toLong()}.toMutableList()

        val r2 = opRegex.matchEntire(lines[2].trim())!!
        val (x1, op, x2) = r2.groupValues.subList(1, 4)
        operation = when (op) {
            "*" ->  {it -> v(x1, it) * v(x2, it)}
            "+" -> {it -> v(x1, it) + v(x2, it)}
            "-" -> {it -> v(x1, it) - v(x2, it)}
            else -> {it -> v(x1, it) / v(x2, it)}
        }

        val r3 = testRegex.matchEntire(lines[3].trim())!!
        mod = r3.groups[1]!!.value.toInt()
        test = {it % mod == 0L}

        val r4 = decRegex.matchEntire(lines[4].trim())
        val m1 = r4!!.groupValues[1].toInt()
        val r5 = decRegex.matchEntire(lines[5].trim())
        val m2 = r5!!.groupValues[1].toInt()
        decision = m1 to m2
    }
}

fun main() {
    val input = readInput(11).split("\n\n")
        .asSequence()
        .map {it.trim()}
        .map {it.lines()}

    var monkeys = input.map {Monkey(it)}.toList()
    var insp = MutableList(monkeys.size) {0}

    // part1
    repeat(20) {
        for ((i, monkey) in monkeys.withIndex()) {
            for (item in monkey.items) {
                val x = monkey.operation(item) / 3
                if (monkey.test(x)) monkeys[monkey.decision.first].items.add(x)
                else monkeys[monkey.decision.second].items.add(x)
            }
            insp[i] += monkey.items.size
            monkey.items.clear()
        }
    }

    println(insp.sortedDescending().take(2).reduce {
            a, b -> a*b
    })

    // common multiple of the monkeys' modular values (not necessarly LCM)
    val N = monkeys.map {it.mod}.reduce {acc, i -> acc*i}

    // part2
    monkeys = input.map {Monkey(it)}.toList()
    insp = MutableList(monkeys.size) {0}
    repeat(10000) {
        for ((i, monkey) in monkeys.withIndex()) {
            for (item in monkey.items) {
                val x = monkey.operation(item) % N
                if (monkey.test(x)) monkeys[monkey.decision.first].items.add(x)
                else monkeys[monkey.decision.second].items.add(x)
            }
            insp[i] += monkey.items.size
            monkey.items.clear()
        }
    }

    println(insp.sortedDescending().take(2).map{it.toLong()}.reduce { a, b ->
        a * b
    })
}