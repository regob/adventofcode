import java.io.File
import java.math.BigInteger
import java.security.MessageDigest

/**
 * Reads lines from the given input txt file.
 */
fun readInput(name: String) = File("../input", name).readText()

/**
 * Reads the input for a given day.
 */
fun readInput(day: Int, year: Int = 2022): String {
    return readInput("${year}_${day}.txt")
}

/**
 * Converts string to md5 hash.
 */
fun String.md5() = BigInteger(1, MessageDigest.getInstance("MD5").digest(toByteArray()))
    .toString(16)
    .padStart(32, '0')
