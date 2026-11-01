import math
from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QPlainTextEdit,
    QLineEdit,
)
from PySide6.QtGui import QFont, QColor, QPainter, QPainterPath, QPen, QBrush, QLinearGradient
from PySide6.QtCore import Qt, Signal, QPointF, QRectF
from theme import DARK_THEME, get_scrollbar_stylesheet, get_code_font, configure_no_ligatures
from highlighter import PythonHighlighter
from icons import TIME_SVG, SPACE_SVG, render_svg_pixmap


# ==========================================================
# Problems Database (All 58 Practice Problems)
# ==========================================================
PROBLEMS_DATA = [
    {
        "id": "max_value",
        "title": "1. max value",
        "raw_title": "max value",
        "category": "Basics",
        "description": (
            "Write a function, max_value, that takes in list of numbers as an argument. "
            "The function should return the largest number in the list.\n\n"
            "Solve this without using any built-in list methods. "
            "You can assume that the list is non-empty."
        ),
        "examples": (
            "max_value([4, 7, 2, 8, 10, 9]) # -> 10\n"
            "max_value([10, 5, 40, 40.3])   # -> 40.3\n"
            "max_value([-5, -2, -1, -11])   # -> -1"
        ),
        "starter_code": "def max_value(nums):\n  pass # todo\n",
        "solution_code": (
            "def max_value(nums):\n"
            "    maximum = nums[0]\n"
            "    for n in nums:\n"
            "        if n > maximum:\n"
            "            maximum = n\n"
            "    return maximum\n\n"
            "# Example test cases:\n"
            "print(max_value([4, 7, 2, 8, 10, 9])) # -> 10\n"
            "print(max_value([10, 5, 40, 40.3]))   # -> 40.3\n"
            "print(max_value([-5, -2, -1, -11]))   # -> -1\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Iterates through the list of n numbers once, maintaining a maximum variable with constant O(1) auxiliary space."
        ),
    },
    {
        "id": "longest_word",
        "title": "2. longest word",
        "raw_title": "longest word",
        "category": "Basics",
        "description": (
            "Write a function, longest_word, that takes in a sentence string as an argument. "
            "The function should return the longest word in the sentence. "
            "If there is a tie, return the word that occurs later in the sentence.\n\n"
            "You can assume that the sentence is non-empty."
        ),
        "examples": (
            'longest_word("the quick brown fox jumps") # -> "jumps"\n'
            'longest_word("where there is a will there is a way") # -> "there"\n'
            'longest_word("hello world") # -> "world"'
        ),
        "starter_code": "def longest_word(sentence):\n  pass # todo\n",
        "solution_code": (
            "def longest_word(sentence):\n"
            '    words = sentence.split(" ")\n'
            '    longest = ""\n'
            "    for word in words:\n"
            "        if len(word) >= len(longest):\n"
            "            longest = word\n"
            "    return longest\n\n"
            "# Example test cases:\n"
            'print(longest_word("the quick brown fox jumps")) # -> "jumps"\n'
            'print(longest_word("where there is a will there is a way")) # -> "there"\n'
            'print(longest_word("hello world")) # -> "world"\n'
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Splits the sentence into words in linear time O(n) and loops once through all words to find the longest."
        ),
    },
    {
        "id": "all_even",
        "title": "3. all even",
        "raw_title": "all even",
        "category": "Basics",
        "description": (
            "Write a function, all_even, that takes in a list of numbers as an argument. "
            "The function should return a boolean indicating whether or not every element of the list is an even number.\n\n"
            "You can assume that the list is non-empty."
        ),
        "examples": (
            "all_even([2, 4, 6, 8]) # -> True\n"
            "all_even([2, 3, 4, 6]) # -> False\n"
            "all_even([12])         # -> True"
        ),
        "starter_code": "def all_even(nums):\n  pass # todo\n",
        "solution_code": (
            "def all_even(nums):\n"
            "    for num in nums:\n"
            "        if num % 2 != 0:\n"
            "            return False\n"
            "    return True\n\n"
            "# Example test cases:\n"
            "print(all_even([2, 4, 6, 8])) # -> True\n"
            "print(all_even([2, 3, 4, 6])) # -> False\n"
            "print(all_even([12]))         # -> True\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Iterates through the list of n numbers once, returning False immediately if any odd number is found."
        ),
    },
    {
        "id": "is_prime",
        "title": "4. is prime",
        "raw_title": "is prime",
        "category": "Basics",
        "description": (
            "Write a function, is_prime, that takes in a number as an argument. "
            "The function should return a boolean indicating whether or not the given number is prime.\n\n"
            "A prime number is a number that is only divisible by two distinct numbers: 1 and itself.\n\n"
            "For example, 7 is a prime because it is only divisible by 1 and 7. "
            "For example, 6 is not a prime because it is divisible by 1, 2, 3, and 6.\n\n"
            "You can assume that the input number is a positive integer."
        ),
        "examples": (
            "is_prime(2)  # -> True\n"
            "is_prime(7)  # -> True\n"
            "is_prime(4)  # -> False\n"
            "is_prime(1)  # -> False\n"
            "is_prime(25) # -> False"
        ),
        "starter_code": "def is_prime(n):\n  pass # todo\n",
        "solution_code": (
            "from math import sqrt, floor\n\n"
            "def is_prime(n):\n"
            "    if n < 2:\n"
            "        return False\n"
            "    for i in range(2, floor(sqrt(n)) + 1):\n"
            "        if n % i == 0:\n"
            "            return False\n"
            "    return True\n\n"
            "# Example test cases:\n"
            "print(is_prime(2))  # -> True\n"
            "print(is_prime(7))  # -> True\n"
            "print(is_prime(4))  # -> False\n"
            "print(is_prime(1))  # -> False\n"
            "print(is_prime(25)) # -> False\n"
        ),
        "time_complexity": "O(√n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(sqrt(n))",
        "complexity_explanation": (
            "Tests factors up to floor(sqrt(n)) because if a number n has a factor larger than sqrt(n), its pair factor must be smaller than sqrt(n)."
        ),
    },
    {
        "id": "fizz_buzz",
        "title": "5. fizz buzz",
        "raw_title": "fizz buzz",
        "category": "Basics",
        "description": (
            "Write a function, fizz_buzz, that takes in a number n as an argument. "
            "The function should return a list containing numbers from 1 to n, replacing certain numbers according to the following rules:\n\n"
            "• if the number is divisible by 3, make the element \"fizz\"\n"
            "• if the number is divisible by 5, make the element \"buzz\"\n"
            "• if the number is divisible by 3 and 5, make the element \"fizzbuzz\""
        ),
        "examples": (
            "fizz_buzz(11)\n"
            "# -> [1, 2, 'fizz', 4, 'buzz', 'fizz', 7, 8, 'fizz', 'buzz', 11]\n\n"
            "fizz_buzz(16)\n"
            "# -> [1, 2, 'fizz', 4, 'buzz', 'fizz', 7, 8, 'fizz', 'buzz', 11, 'fizz', 13, 14, 'fizzbuzz', 16]"
        ),
        "starter_code": "def fizz_buzz(n):\n  pass # todo\n",
        "solution_code": (
            "def fizz_buzz(n):\n"
            "    result = []\n"
            "    for i in range(1, n + 1):\n"
            "        if i % 3 == 0 and i % 5 == 0:\n"
            "            result.append(\"fizzbuzz\")\n"
            "        elif i % 3 == 0:\n"
            "            result.append(\"fizz\")\n"
            "        elif i % 5 == 0:\n"
            "            result.append(\"buzz\")\n"
            "        else:\n"
            "            result.append(i)\n"
            "    return result\n\n"
            "# Example test cases:\n"
            "print(fizz_buzz(11))\n"
            "print(fizz_buzz(16))\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Loops from 1 to n with constant-time modulo checks and appends each element to the result list."
        ),
    },
    {
        "id": "pairs",
        "title": "6. pairs",
        "raw_title": "pairs",
        "category": "Basics",
        "description": (
            "Write a function, pairs, that takes in a list as an argument. "
            "The function should return a list containing all unique pairs of elements.\n\n"
            "You may return the pairs in any order and the order of elements within a single pair does not matter.\n\n"
            "You can assume that the input list contains unique elements."
        ),
        "examples": (
            "pairs([\"a\", \"b\", \"c\"])\n"
            "# -> [['a', 'b'], ['a', 'c'], ['b', 'c']]\n\n"
            "pairs([\"red\", \"silver\", \"green\", \"blue\"])\n"
            "# -> [['red', 'silver'], ['red', 'green'], ['red', 'blue'], ['silver', 'green'], ['silver', 'blue'], ['green', 'blue']]"
        ),
        "starter_code": "def pairs(elements):\n  pass # todo\n",
        "solution_code": (
            "def pairs(elements):\n"
            "    result = []\n"
            "    for i in range(0, len(elements)):\n"
            "        for j in range(i + 1, len(elements)):\n"
            "            pair = [elements[i], elements[j]]\n"
            "            result.append(pair)\n"
            "    return result\n\n"
            "# Example test cases:\n"
            "print(pairs([\"a\", \"b\", \"c\"]))\n"
            "print(pairs([\"red\", \"silver\", \"green\", \"blue\"]))\n"
        ),
        "time_complexity": "O(n²)",
        "space_complexity": "O(n²)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Nested loop iterates over all pairs, resulting in n(n - 1)/2 iterations and quadratic storage space."
        ),
    },
    {
        "id": "anagrams",
        "title": "7. anagrams",
        "raw_title": "anagrams",
        "category": "Hash Map",
        "description": (
            "Write a function, anagrams, that takes in two strings as arguments. "
            "The function should return a boolean indicating whether or not the strings are anagrams. "
            "Anagrams are strings that contain the same characters, but in any order."
        ),
        "examples": (
            "anagrams('restful', 'fluster') # -> True\n"
            "anagrams('cats', 'tocs')       # -> False\n"
            "anagrams('monkeyswrite', 'newyorktimes') # -> True\n"
            "anagrams('paper', 'reapa')     # -> False"
        ),
        "starter_code": "def anagrams(s1, s2):\n  pass # todo\n",
        "solution_code": (
            "def anagrams(s1, s2):\n"
            "    return char_count(s1) == char_count(s2)\n\n"
            "def char_count(s):\n"
            "    count = {}\n"
            "    for char in s:\n"
            "        if char not in count:\n"
            "            count[char] = 0\n"
            "        count[char] += 1\n"
            "    return count\n\n"
            "# Alternative using Counter:\n"
            "# from collections import Counter\n"
            "# def anagrams(s1, s2):\n"
            "#     return Counter(s1) == Counter(s2)\n\n"
            "# Example test cases:\n"
            "print(anagrams('restful', 'fluster'))           # -> True\n"
            "print(anagrams('cats', 'tocs'))                 # -> False\n"
            "print(anagrams('monkeyswrite', 'newyorktimes')) # -> True\n"
            "print(anagrams('paper', 'reapa'))               # -> False\n"
        ),
        "time_complexity": "O(n + m)",
        "space_complexity": "O(n + m)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Counts character occurrences in both strings of lengths n and m, requiring linear time and space proportional to the distinct characters."
        ),
    },
    {
        "id": "most_frequent_char",
        "title": "8. most frequent char",
        "raw_title": "most frequent char",
        "category": "Hash Map",
        "description": (
            "Write a function, most_frequent_char, that takes in a string as an argument. "
            "The function should return the most frequent character of the string. "
            "If there are ties, return the character that appears earlier in the string.\n\n"
            "You can assume that the input string is non-empty."
        ),
        "examples": (
            "most_frequent_char('bookeeper')   # -> 'e'\n"
            "most_frequent_char('david')       # -> 'd'\n"
            "most_frequent_char('abby')        # -> 'b'\n"
            "most_frequent_char('mississippi') # -> 'i'"
        ),
        "starter_code": "def most_frequent_char(s):\n  pass # todo\n",
        "solution_code": (
            "def most_frequent_char(s):\n"
            "    count = {}\n"
            "    for char in s:\n"
            "        if char not in count:\n"
            "            count[char] = 0\n"
            "        count[char] += 1\n\n"
            "    best = None\n"
            "    for char in s:\n"
            "        if best is None or count[char] > count[best]:\n"
            "            best = char\n"
            "    return best\n\n"
            "# Alternative using Counter:\n"
            "# from collections import Counter\n"
            "# def most_frequent_char(s):\n"
            "#     count = Counter(s)\n"
            "#     best = None\n"
            "#     for char in s:\n"
            "#         if best is None or count[char] > count[best]:\n"
            "#             best = char\n"
            "#     return best\n\n"
            "# Example test cases:\n"
            "print(most_frequent_char('bookeeper'))   # -> 'e'\n"
            "print(most_frequent_char('david'))       # -> 'd'\n"
            "print(most_frequent_char('abby'))        # -> 'b'\n"
            "print(most_frequent_char('mississippi')) # -> 'i'\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Constructs a frequency map in O(n) time, then iterates through the string once more to find the earliest most-frequent character."
        ),
    },
    {
        "id": "pair_sum",
        "title": "9. pair sum",
        "raw_title": "pair sum",
        "category": "Hash Map",
        "description": (
            "Write a function, pair_sum, that takes in a list and a target sum as arguments. "
            "The function should return a tuple containing a pair of indices whose elements sum to the given target. "
            "The indices returned must be unique.\n\n"
            "Be sure to return the indices, not the elements themselves.\n\n"
            "There is guaranteed to be one such pair that sums to the target."
        ),
        "examples": (
            "pair_sum([3, 2, 5, 4, 1], 8)    # -> (0, 2) or (2, 0)\n"
            "pair_sum([4, 7, 9, 2, 5, 1], 5)  # -> (0, 5) or (5, 0)\n"
            "pair_sum([4, 7, 9, 2, 5, 1], 3)  # -> (3, 5) or (5, 3)\n"
            "pair_sum([1, 6, 7, 2], 13)       # -> (1, 2) or (2, 1)"
        ),
        "starter_code": "def pair_sum(numbers, target_sum):\n  pass # todo\n",
        "solution_code": (
            "def pair_sum(numbers, target_sum):\n"
            "    previous_numbers = {}\n\n"
            "    for index, num in enumerate(numbers):\n"
            "        complement = target_sum - num\n\n"
            "        if complement in previous_numbers:\n"
            "            return (index, previous_numbers[complement])\n\n"
            "        previous_numbers[num] = index\n\n"
            "# Example test cases:\n"
            "print(pair_sum([3, 2, 5, 4, 1], 8))    # -> (0, 2) or (2, 0)\n"
            "print(pair_sum([4, 7, 9, 2, 5, 1], 5))  # -> (0, 5) or (5, 0)\n"
            "print(pair_sum([4, 7, 9, 2, 5, 1], 3))  # -> (3, 5) or (5, 3)\n"
            "print(pair_sum([1, 6, 7, 2], 13))       # -> (1, 2) or (2, 1)\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Single pass through the list using a hash map to achieve instant O(1) average lookup for the required complement."
        ),
    },
    {
        "id": "pair_product",
        "title": "10. pair product",
        "raw_title": "pair product",
        "category": "Hash Map",
        "description": (
            "Write a function, pair_product, that takes in a list and a target product as arguments. "
            "The function should return a tuple containing a pair of indices whose elements multiply to the given target. "
            "The indices returned must be unique.\n\n"
            "Be sure to return the indices, not the elements themselves.\n\n"
            "There is guaranteed to be one such pair whose product is the target."
        ),
        "examples": (
            "pair_product([3, 2, 5, 4, 1], 8)     # -> (1, 3) or (3, 1)\n"
            "pair_product([3, 2, 5, 4, 1], 10)    # -> (1, 2) or (2, 1)\n"
            "pair_product([4, 7, 9, 2, 5, 1], 35) # -> (1, 4) or (4, 1)\n"
            "pair_product([4, 6, 8, 2], 16)       # -> (2, 3) or (3, 2)"
        ),
        "starter_code": "def pair_product(numbers, target_product):\n  pass # todo\n",
        "solution_code": (
            "def pair_product(numbers, target_product):\n"
            "    previous_nums = {}\n\n"
            "    for index, num in enumerate(numbers):\n"
            "        complement = target_product / num\n\n"
            "        if complement in previous_nums:\n"
            "            return (index, previous_nums[complement])\n\n"
            "        previous_nums[num] = index\n\n"
            "# Example test cases:\n"
            "print(pair_product([3, 2, 5, 4, 1], 8))     # -> (1, 3) or (3, 1)\n"
            "print(pair_product([3, 2, 5, 4, 1], 10))    # -> (1, 2) or (2, 1)\n"
            "print(pair_product([4, 7, 9, 2, 5, 1], 35)) # -> (1, 4) or (4, 1)\n"
            "print(pair_product([4, 6, 8, 2], 16))       # -> (2, 3) or (3, 2)\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Single pass through the list using a hash map to achieve O(1) lookup for the target quotient complement."
        ),
    },
    {
        "id": "intersection",
        "title": "11. intersection",
        "raw_title": "intersection",
        "category": "Hash Map",
        "description": (
            "Write a function, intersection, that takes in two lists, a, b, as arguments. "
            "The function should return a new list containing elements that are in both of the two lists.\n\n"
            "You may assume that each input list does not contain duplicate elements."
        ),
        "examples": (
            "intersection([4, 2, 1, 6], [3, 6, 9, 2, 10]) # -> [6, 2]\n"
            "intersection([2, 4, 6], [4, 2])               # -> [4, 2]\n"
            "intersection([4, 2, 1], [1, 2, 4, 6])         # -> [1, 2, 4]\n"
            "intersection([0, 1, 2], [10, 11])             # -> []"
        ),
        "starter_code": "def intersection(a, b):\n  pass # todo\n",
        "solution_code": (
            "def intersection(a, b):\n"
            "    set_a = set(a)\n"
            "    return [item for item in b if item in set_a]\n\n"
            "# Brute force alternative O(n * m):\n"
            "# def intersection(a, b):\n"
            "#     result = []\n"
            "#     for item in b:\n"
            "#         if item in a:\n"
            "#             result.append(item)\n"
            "#     return result\n\n"
            "# Example test cases:\n"
            "print(intersection([4, 2, 1, 6], [3, 6, 9, 2, 10])) # -> [6, 2]\n"
            "print(intersection([2, 4, 6], [4, 2]))               # -> [4, 2]\n"
            "print(intersection([4, 2, 1], [1, 2, 4, 6]))         # -> [1, 2, 4]\n"
            "print(intersection([0, 1, 2], [10, 11]))             # -> []\n"
        ),
        "time_complexity": "O(n + m)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Converting list a into a set takes O(n) time and O(n) space; iterating through list b with O(1) set lookups takes O(m) time."
        ),
    },
    {
        "id": "exclusive_items",
        "title": "12. exclusive items",
        "raw_title": "exclusive items",
        "category": "Hash Map",
        "description": (
            "Write a function, exclusive_items, that takes in two lists, a, b, as arguments. "
            "The function should return a new list containing elements that are in either list but not both lists.\n\n"
            "You may assume that each input list does not contain duplicate elements."
        ),
        "examples": (
            "exclusive_items([4, 2, 1, 6], [3, 6, 9, 2, 10]) # -> [4, 1, 3, 9, 10]\n"
            "exclusive_items([2, 4, 6], [4, 2])               # -> [6]\n"
            "exclusive_items([1, 2, 3], [1, 2, 3])            # -> []\n"
            "exclusive_items([1, 2], [3, 4])                  # -> [1, 2, 3, 4]"
        ),
        "starter_code": "def exclusive_items(a, b):\n  pass # todo\n",
        "solution_code": (
            "def exclusive_items(a, b):\n"
            "    difference = []\n"
            "    set_a = set(a)\n"
            "    set_b = set(b)\n\n"
            "    for item in a:\n"
            "        if item not in set_b:\n"
            "            difference.append(item)\n\n"
            "    for item in b:\n"
            "        if item not in set_a:\n"
            "            difference.append(item)\n\n"
            "    return difference\n\n"
            "# Example test cases:\n"
            "print(exclusive_items([4, 2, 1, 6], [3, 6, 9, 2, 10])) # -> [4, 1, 3, 9, 10]\n"
            "print(exclusive_items([2, 4, 6], [4, 2]))               # -> [6]\n"
            "print(exclusive_items([1, 2, 3], [1, 2, 3]))            # -> []\n"
            "print(exclusive_items([1, 2], [3, 4]))                  # -> [1, 2, 3, 4]\n"
        ),
        "time_complexity": "O(n + m)",
        "space_complexity": "O(n + m)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Converting both lists into sets enables linear-time symmetric difference checking with constant-time set lookups."
        ),
    },
    {
        "id": "all_unique",
        "title": "13. all unique",
        "raw_title": "all unique",
        "category": "Hash Map",
        "description": (
            "Write a function, all_unique, that takes in a list. "
            "The function should return a boolean indicating whether or not the list contains unique items."
        ),
        "examples": (
            "all_unique([\"q\", \"r\", \"s\", \"a\"]) # -> True\n"
            "all_unique([\"q\", \"r\", \"s\", \"q\"]) # -> False\n"
            "all_unique([1, 2, 3, 4, 5])      # -> True\n"
            "all_unique([])                   # -> True"
        ),
        "starter_code": "def all_unique(items):\n  pass # todo\n",
        "solution_code": (
            "def all_unique(items):\n"
            "    unique_items = set(items)\n"
            "    return len(unique_items) == len(items)\n\n"
            "# Example test cases:\n"
            "print(all_unique([\"q\", \"r\", \"s\", \"a\"])) # -> True\n"
            "print(all_unique([\"q\", \"r\", \"s\", \"q\"])) # -> False\n"
            "print(all_unique([1, 2, 3, 4, 5]))      # -> True\n"
            "print(all_unique([]))                   # -> True\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Building a set from list of length n takes O(n) average time and space; comparing set length to list length is O(1)."
        ),
    },
    {
        "id": "intersection_with_dupes",
        "title": "14. intersection with dupes",
        "raw_title": "intersection with dupes",
        "category": "Hash Map",
        "description": (
            "Write a function, intersection_with_dupes, that takes in two lists, a, b, as arguments. "
            "The function should return a new list containing elements that are common to both input lists. "
            "The elements in the result should appear as many times as they occur in both input lists.\n\n"
            "You can return the result in any order."
        ),
        "examples": (
            "intersection_with_dupes([1, 2, 2, 1], [2, 2])         # -> [2, 2]\n"
            "intersection_with_dupes([4, 9, 5], [9, 4, 9, 8, 4])   # -> [4, 9] (any order)\n"
            "intersection_with_dupes(['a', 'b', 'c'], ['x', 'y']) # -> []"
        ),
        "starter_code": "def intersection_with_dupes(a, b):\n  pass # todo\n",
        "solution_code": (
            "from collections import Counter\n\n"
            "def intersection_with_dupes(a, b):\n"
            "    count_a = Counter(a)\n"
            "    count_b = Counter(b)\n"
            "    result = []\n\n"
            "    for ele in count_a:\n"
            "        for i in range(0, min(count_a[ele], count_b[ele])):\n"
            "            result.append(ele)\n\n"
            "    return result\n\n"
            "# Example test cases:\n"
            "print(intersection_with_dupes([1, 2, 2, 1], [2, 2]))         # -> [2, 2]\n"
            "print(intersection_with_dupes([4, 9, 5], [9, 4, 9, 8, 4]))   # -> [4, 9]\n"
            "print(intersection_with_dupes(['a', 'b', 'c'], ['x', 'y'])) # -> []\n"
        ),
        "time_complexity": "O(n + m)",
        "space_complexity": "O(n + m)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Counting frequencies with Counter takes O(n + m) time; finding minimum occurrences and building the result takes linear time."
        ),
    },
    {
        "id": "sum_numbers_recursive",
        "title": "15. sum numbers recursive",
        "raw_title": "sum numbers recursive",
        "category": "Recursion",
        "description": (
            "Watch the Approach video first!\n\n"
            "Write a function sum_numbers_recursive that takes in an array of numbers and returns the sum of all the numbers in the array. "
            "All elements will be integers. Solve this recursively."
        ),
        "examples": (
            "sum_numbers_recursive([5, 2, 9, 10])     # -> 26\n"
            "sum_numbers_recursive([1, -1, 1, -1, 1]) # -> 1\n"
            "sum_numbers_recursive([])                # -> 0\n"
            "sum_numbers_recursive([1000, 50])        # -> 1050"
        ),
        "starter_code": "def sum_numbers_recursive(numbers):\n  pass # todo\n",
        "solution_code": (
            "def sum_numbers_recursive(numbers):\n"
            "    if len(numbers) == 0:\n"
            "        return 0\n"
            "    return numbers[0] + sum_numbers_recursive(numbers[1:])\n\n"
            "# Example test cases:\n"
            "print(sum_numbers_recursive([5, 2, 9, 10]))     # -> 26\n"
            "print(sum_numbers_recursive([1, -1, 1, -1, 1])) # -> 1\n"
            "print(sum_numbers_recursive([]))                # -> 0\n"
            "print(sum_numbers_recursive([1000, 50]))        # -> 1050\n"
        ),
        "time_complexity": "O(n²)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Each recursive call creates an O(n) slice of the remaining list numbers[1:], resulting in O(n²) total time and O(n) recursive call stack frames."
        ),
    },
    {
        "id": "factorial",
        "title": "16. factorial",
        "raw_title": "factorial",
        "category": "Recursion",
        "description": (
            "Write a function, factorial, that takes in a number n and returns the factorial of that number. "
            "The factorial of n is the product of all the positive numbers less than or equal to n. "
            "You must solve this recursively. You can assume that n is a non-negative integer. "
            "Note that the factorial of 0 is defined to be 1."
        ),
        "examples": (
            "factorial(3)  # -> 6\n"
            "factorial(6)  # -> 720\n"
            "factorial(18) # -> 6402373705728000\n"
            "factorial(1)  # -> 1\n"
            "factorial(0)  # -> 1"
        ),
        "starter_code": "def factorial(n):\n  pass # todo\n",
        "solution_code": (
            "def factorial(n):\n"
            "    if n == 0:\n"
            "        return 1\n"
            "    return n * factorial(n - 1)\n\n"
            "# Example test cases:\n"
            "print(factorial(3))  # -> 6\n"
            "print(factorial(6))  # -> 720\n"
            "print(factorial(18)) # -> 6402373705728000\n"
            "print(factorial(1))  # -> 1\n"
            "print(factorial(0))  # -> 1\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Recurses n times performing constant-time multiplications, using O(n) space on the recursive call stack."
        ),
    },
    {
        "id": "sum_of_lengths",
        "title": "17. sum of lengths",
        "raw_title": "sum of lengths",
        "category": "Recursion",
        "description": (
            "Write a function sum_of_lengths that takes in a list of strings and returns the total length of the strings.\n\n"
            "You must solve this recursively."
        ),
        "examples": (
            "sum_of_lengths(['goat', 'cat', 'purple'])               # -> 13\n"
            "sum_of_lengths(['bike', 'at', 'pencils', 'phone'])       # -> 19\n"
            "sum_of_lengths([])                                      # -> 0\n"
            "sum_of_lengths(['', ' ', '  ', '   ', '    ', '     ']) # -> 15"
        ),
        "starter_code": "def sum_of_lengths(strings):\n  pass # todo\n",
        "solution_code": (
            "def sum_of_lengths(strings):\n"
            "    if len(strings) == 0:\n"
            "        return 0\n"
            "    return len(strings[0]) + sum_of_lengths(strings[1:])\n\n"
            "# Example test cases:\n"
            "print(sum_of_lengths(['goat', 'cat', 'purple']))               # -> 13\n"
            "print(sum_of_lengths(['bike', 'at', 'pencils', 'phone']))       # -> 19\n"
            "print(sum_of_lengths([]))                                      # -> 0\n"
            "print(sum_of_lengths(['', ' ', '  ', '   ', '    ', '     '])) # -> 15\n"
        ),
        "time_complexity": "O(n²)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Recurses through n strings with list slicing taking O(n) per recursive step, resulting in O(n²) total time and O(n) call stack space."
        ),
    },
    {
        "id": "reverse_string_recursive",
        "title": "18. reverse string recursive",
        "raw_title": "reverse string recursive",
        "category": "Recursion",
        "description": (
            "Write a function, reverse_string, that takes in a string as an argument. "
            "The function should return the string with its characters in reverse order. You must do this recursively."
        ),
        "examples": (
            "reverse_string('hello')    # -> 'olleh'\n"
            "reverse_string('xyz')      # -> 'zyx'\n"
            "reverse_string('bootcamp') # -> 'pmactoob'\n"
            "reverse_string('')         # -> ''"
        ),
        "starter_code": "def reverse_string(s):\n  pass # todo\n",
        "solution_code": (
            "def reverse_string(s):\n"
            "    if len(s) == 0:\n"
            "        return \"\"\n"
            "    return reverse_string(s[1:]) + s[0]\n\n"
            "# Example test cases:\n"
            "print(reverse_string('hello'))    # -> 'olleh'\n"
            "print(reverse_string('xyz'))      # -> 'zyx'\n"
            "print(reverse_string('bootcamp')) # -> 'pmactoob'\n"
            "print(reverse_string(''))         # -> ''\n"
        ),
        "time_complexity": "O(n²)",
        "space_complexity": "O(n²)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Each recursive call slices the string s[1:], taking O(n) time and allocating new string memory across n stack frames."
        ),
    },
    {
        "id": "palindrome_recursive",
        "title": "19. palindrome recursive",
        "raw_title": "palindrome recursive",
        "category": "Recursion",
        "description": (
            "Write a function, palindrome, that takes in a string and returns a boolean indicating whether or not the string is the same forwards and backwards.\n\n"
            "You must solve this recursively."
        ),
        "examples": (
            "palindrome('pop')      # -> True\n"
            "palindrome('kayak')    # -> True\n"
            "palindrome('bootcamp') # -> False\n"
            "palindrome('rotator')  # -> True\n"
            "palindrome('cb')       # -> False\n"
            "palindrome('')         # -> True"
        ),
        "starter_code": "def palindrome(s):\n  pass # todo\n",
        "solution_code": (
            "def palindrome(s):\n"
            "    if len(s) == 0 or len(s) == 1:\n"
            "        return True\n"
            "    if s[0] != s[-1]:\n"
            "        return False\n"
            "    return palindrome(s[1:-1])\n\n"
            "# Example test cases:\n"
            "print(palindrome('pop'))      # -> True\n"
            "print(palindrome('kayak'))    # -> True\n"
            "print(palindrome('bootcamp')) # -> False\n"
            "print(palindrome('rotator'))  # -> True\n"
            "print(palindrome('cb'))       # -> False\n"
            "print(palindrome(''))         # -> True\n"
        ),
        "time_complexity": "O(n²)",
        "space_complexity": "O(n²)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Compares outer characters and creates an O(n) slice s[1:-1] at each recursive step, taking O(n²) time and O(n²) total space."
        ),
    },
    {
        "id": "fibonacci",
        "title": "20. fibonacci",
        "raw_title": "fibonacci",
        "category": "Recursion",
        "description": (
            "Write a function, fibonacci, that takes in a number argument, n, and returns the n-th number of the Fibonacci sequence.\n\n"
            "The 0-th number of the sequence is 0.\n"
            "The 1-st number of the sequence is 1.\n\n"
            "To generate further numbers of the sequence, calculate the sum of previous two numbers.\n\n"
            "You must solve this recursively."
        ),
        "examples": (
            "fibonacci(0) # -> 0\n"
            "fibonacci(1) # -> 1\n"
            "fibonacci(2) # -> 1\n"
            "fibonacci(3) # -> 2\n"
            "fibonacci(4) # -> 3\n"
            "fibonacci(5) # -> 5\n"
            "fibonacci(8) # -> 21"
        ),
        "starter_code": "def fibonacci(n):\n  pass # todo\n",
        "solution_code": (
            "def fibonacci(n):\n"
            "    if n == 0 or n == 1:\n"
            "        return n\n"
            "    return fibonacci(n - 1) + fibonacci(n - 2)\n\n"
            "# Example test cases:\n"
            "print(fibonacci(0)) # -> 0\n"
            "print(fibonacci(1)) # -> 1\n"
            "print(fibonacci(2)) # -> 1\n"
            "print(fibonacci(3)) # -> 2\n"
            "print(fibonacci(4)) # -> 3\n"
            "print(fibonacci(5)) # -> 5\n"
            "print(fibonacci(8)) # -> 21\n"
        ),
        "time_complexity": "O(2ⁿ)",
        "space_complexity": "O(n)",
        "complexity_type": "O(2^n)",
        "complexity_explanation": (
            "Each recursive call branches into two subproblems forming a recursion tree of height n, taking O(2ⁿ) operations with O(n) maximum call stack depth."
        ),
    },
    {
        "id": "linked_list_values",
        "title": "21. linked list values",
        "raw_title": "linked list values",
        "category": "Linked List",
        "description": (
            "Write a function, linked_list_values, that takes in the head of a linked list as an argument. "
            "The function should return a list containing all values of the nodes in the linked list."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n\n"
            "linked_list_values(a) # -> ['a', 'b', 'c', 'd']\n\n"
            "x = Node('x')\n"
            "linked_list_values(x) # -> ['x']\n\n"
            "linked_list_values(None) # -> []"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def linked_list_values(head):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Iterative Approach ===\n"
            "def linked_list_values(head):\n"
            "    values = []\n"
            "    current = head\n"
            "    while current is not None:\n"
            "        values.append(current.val)\n"
            "        current = current.next\n"
            "    return values\n\n\n"
            "# === Recursive Approach ===\n"
            "def linked_list_values(head):\n"
            "    values = []\n"
            "    _linked_list_values(head, values)\n"
            "    return values\n\n"
            "def _linked_list_values(head, values):\n"
            "    if head is None:\n"
            "        return\n"
            "    values.append(head.val)\n"
            "    _linked_list_values(head.next, values)\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n\n"
            "print(linked_list_values(a)) # -> ['a', 'b', 'c', 'd']\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Traverses through all n nodes in the linked list, building an array of n elements in linear time and auxiliary space."
        ),
    },
    {
        "id": "sum_list",
        "title": "22. sum list",
        "raw_title": "sum list",
        "category": "Linked List",
        "description": (
            "Write a function, sum_list, that takes in the head of a linked list containing numbers as an argument. "
            "The function should return the total sum of all values in the linked list."
        ),
        "examples": (
            "a = Node(2)\n"
            "b = Node(8)\n"
            "c = Node(3)\n"
            "d = Node(-1)\n"
            "e = Node(7)\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n"
            "d.next = e\n\n"
            "sum_list(a)    # -> 19\n\n"
            "x = Node(38)\n"
            "sum_list(x)    # -> 38\n\n"
            "sum_list(None) # -> 0"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def sum_list(head):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Iterative Approach ===\n"
            "def sum_list(head):\n"
            "    total_sum = 0\n"
            "    current = head\n"
            "    while current is not None:\n"
            "        total_sum += current.val\n"
            "        current = current.next\n"
            "    return total_sum\n\n\n"
            "# === Recursive Approach ===\n"
            "def sum_list(head):\n"
            "    if head is None:\n"
            "        return 0\n"
            "    return head.val + sum_list(head.next)\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n"
            "a = Node(2)\n"
            "b = Node(8)\n"
            "c = Node(3)\n"
            "d = Node(-1)\n"
            "e = Node(7)\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n"
            "d.next = e\n\n"
            "print(sum_list(a))    # -> 19\n"
            "print(sum_list(None)) # -> 0\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Linear traversal across all n nodes. The iterative approach uses O(1) auxiliary memory; the recursive solution uses O(n) call stack space."
        ),
    },
    {
        "id": "linked_list_find",
        "title": "23. linked list find",
        "raw_title": "linked list find",
        "category": "Linked List",
        "description": (
            "Write a function, linked_list_find, that takes in the head of a linked list and a target value. "
            "The function should return a boolean indicating whether or not the linked list contains the target."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n\n"
            "linked_list_find(a, 'c')    # -> True\n"
            "linked_list_find(a, 'd')    # -> True\n"
            "linked_list_find(a, 'q')    # -> False\n"
            "linked_list_find(None, 'c') # -> False"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def linked_list_find(head, target):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Iterative Approach ===\n"
            "def linked_list_find(head, target):\n"
            "    current = head\n"
            "    while current is not None:\n"
            "        if current.val == target:\n"
            "            return True\n"
            "        current = current.next\n"
            "    return False\n\n\n"
            "# === Recursive Approach ===\n"
            "def linked_list_find(head, target):\n"
            "    if head is None:\n"
            "        return False\n"
            "    if head.val == target:\n"
            "        return True\n"
            "    return linked_list_find(head.next, target)\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n\n"
            "print(linked_list_find(a, 'c'))    # -> True\n"
            "print(linked_list_find(a, 'd'))    # -> True\n"
            "print(linked_list_find(a, 'q'))    # -> False\n"
            "print(linked_list_find(None, 'c')) # -> False\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Traverses at most n nodes looking for the target value, consuming O(1) space iteratively and O(n) call stack frames recursively."
        ),
    },
    {
        "id": "get_node_value",
        "title": "24. get node value",
        "raw_title": "get node value",
        "category": "Linked List",
        "description": (
            "Write a function, get_node_value, that takes in the head of a linked list and an index. "
            "The function should return the value of the linked list at the specified index.\n\n"
            "If there is no node at the given index, then return None."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n\n"
            "get_node_value(a, 2)    # -> 'c'\n"
            "get_node_value(a, 3)    # -> 'd'\n"
            "get_node_value(a, 7)    # -> None\n"
            "get_node_value(None, 0) # -> None"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def get_node_value(head, index):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Iterative Approach ===\n"
            "def get_node_value(head, index):\n"
            "    count = 0\n"
            "    current = head\n"
            "    while current is not None:\n"
            "        if count == index:\n"
            "            return current.val\n"
            "        current = current.next\n"
            "        count += 1\n"
            "    return None\n\n\n"
            "# === Recursive Approach ===\n"
            "def get_node_value(head, index):\n"
            "    if head is None:\n"
            "        return None\n"
            "    if index == 0:\n"
            "        return head.val\n"
            "    return get_node_value(head.next, index - 1)\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n\n"
            "print(get_node_value(a, 2))    # -> 'c'\n"
            "print(get_node_value(a, 3))    # -> 'd'\n"
            "print(get_node_value(a, 7))    # -> None\n"
            "print(get_node_value(None, 0)) # -> None\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Steps sequentially through the linked list up to index (at most n steps), taking O(n) time and O(1) space iteratively (O(n) recursive stack)."
        ),
    },
    {
        "id": "reverse_list",
        "title": "25. reverse list",
        "raw_title": "reverse list",
        "category": "Linked List",
        "description": (
            "Write a function, reverse_list, that takes in the head of a linked list as an argument. "
            "The function should reverse the order of the nodes in the linked list in-place and return the new head of the reversed linked list."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n"
            "d.next = e\n"
            "e.next = f\n\n"
            "reverse_list(a) # -> f -> e -> d -> c -> b -> a"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def reverse_list(head):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Iterative Approach ===\n"
            "def reverse_list(head):\n"
            "    prev = None\n"
            "    current = head\n"
            "    while current is not None:\n"
            "        next_node = current.next\n"
            "        current.next = prev\n"
            "        prev = current\n"
            "        current = next_node\n"
            "    return prev\n\n\n"
            "# === Recursive Approach ===\n"
            "def reverse_list(head, prev=None):\n"
            "    if head is None:\n"
            "        return prev\n"
            "    next_node = head.next\n"
            "    head.next = prev\n"
            "    return reverse_list(next_node, head)\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n"
            "def print_list(head):\n"
            "    vals = []\n"
            "    curr = head\n"
            "    while curr:\n"
            "        vals.append(str(curr.val))\n"
            "        curr = curr.next\n"
            "    return ' -> '.join(vals)\n\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n"
            "d.next = e\n"
            "e.next = f\n\n"
            "print(print_list(reverse_list(a))) # -> f -> e -> d -> c -> b -> a\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Reverses the next pointer of each node in-place in a single pass taking O(1) space iteratively (O(n) recursive stack frames)."
        ),
    },
    {
        "id": "zipper_lists",
        "title": "26. zipper lists",
        "raw_title": "zipper lists",
        "category": "Linked List",
        "description": (
            "Write a function, zipper_lists, that takes in the head of two linked lists as arguments. "
            "The function should zipper the two lists together into single linked list by alternating nodes. "
            "If one of the linked lists is longer than the other, the resulting list should terminate with the remaining nodes. "
            "The function should return the head of the zippered linked list.\n\n"
            "Do this in-place, by mutating the original Nodes.\n\n"
            "You may assume that both input lists are non-empty."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "a.next = b\n"
            "b.next = c\n\n"
            "x = Node('x')\n"
            "y = Node('y')\n"
            "z = Node('z')\n"
            "x.next = y\n"
            "y.next = z\n\n"
            "zipper_lists(a, x) # -> a -> x -> b -> y -> c -> z"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def zipper_lists(head_1, head_2):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Iterative Approach ===\n"
            "def zipper_lists(head_1, head_2):\n"
            "    tail = head_1\n"
            "    current_1 = head_1.next\n"
            "    current_2 = head_2\n"
            "    count = 0\n"
            "    while current_1 is not None and current_2 is not None:\n"
            "        if count % 2 == 0:\n"
            "            tail.next = current_2\n"
            "            current_2 = current_2.next\n"
            "        else:\n"
            "            tail.next = current_1\n"
            "            current_1 = current_1.next\n"
            "        tail = tail.next\n"
            "        count += 1\n\n"
            "    if current_1 is not None:\n"
            "        tail.next = current_1\n"
            "    if current_2 is not None:\n"
            "        tail.next = current_2\n\n"
            "    return head_1\n\n\n"
            "# === Recursive Approach ===\n"
            "def zipper_lists(head_1, head_2):\n"
            "    if head_1 is None and head_2 is None:\n"
            "        return None\n"
            "    if head_1 is None:\n"
            "        return head_2\n"
            "    if head_2 is None:\n"
            "        return head_1\n\n"
            "    next_1 = head_1.next\n"
            "    next_2 = head_2.next\n"
            "    head_1.next = head_2\n"
            "    head_2.next = zipper_lists(next_1, next_2)\n"
            "    return head_1\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n"
            "def print_list(head):\n"
            "    vals = []\n"
            "    curr = head\n"
            "    while curr:\n"
            "        vals.append(str(curr.val))\n"
            "        curr = curr.next\n"
            "    return ' -> '.join(vals)\n\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "a.next = b\n"
            "b.next = c\n\n"
            "x = Node('x')\n"
            "y = Node('y')\n"
            "z = Node('z')\n"
            "x.next = y\n"
            "y.next = z\n\n"
            "print(print_list(zipper_lists(a, x))) # -> a -> x -> b -> y -> c -> z\n"
        ),
        "time_complexity": "O(min(n, m))",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Alternates node references in-place taking linear time proportional to the shorter list in O(1) space iteratively (O(min(n, m)) recursive stack)."
        ),
    },
    {
        "id": "merge_lists",
        "title": "27. merge lists",
        "raw_title": "merge lists",
        "category": "Linked List",
        "description": (
            "Write a function, merge_lists, that takes in the head of two sorted linked lists as arguments. "
            "The function should merge the two lists together into single sorted linked list. "
            "The function should return the head of the merged linked list.\n\n"
            "Do this in-place, by mutating the original Nodes.\n\n"
            "You may assume that both input lists are non-empty and contain increasing sorted numbers."
        ),
        "examples": (
            "a = Node(5)\n"
            "b = Node(7)\n"
            "c = Node(10)\n"
            "a.next = b\n"
            "b.next = c\n\n"
            "q = Node(6)\n"
            "r = Node(8)\n"
            "s = Node(9)\n"
            "q.next = r\n"
            "r.next = s\n\n"
            "merge_lists(a, q) # -> 5 -> 6 -> 7 -> 8 -> 9 -> 10"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def merge_lists(head_1, head_2):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Iterative Approach ===\n"
            "def merge_lists(head_1, head_2):\n"
            "    dummy_head = Node(None)\n"
            "    tail = dummy_head\n"
            "    current_1 = head_1\n"
            "    current_2 = head_2\n\n"
            "    while current_1 is not None and current_2 is not None:\n"
            "        if current_1.val < current_2.val:\n"
            "            tail.next = current_1\n"
            "            current_1 = current_1.next\n"
            "        else:\n"
            "            tail.next = current_2\n"
            "            current_2 = current_2.next\n"
            "        tail = tail.next\n\n"
            "    if current_1 is not None:\n"
            "        tail.next = current_1\n"
            "    if current_2 is not None:\n"
            "        tail.next = current_2\n\n"
            "    return dummy_head.next\n\n\n"
            "# === Recursive Approach ===\n"
            "def merge_lists(head_1, head_2):\n"
            "    if head_1 is None and head_2 is None:\n"
            "        return None\n"
            "    if head_1 is None:\n"
            "        return head_2\n"
            "    if head_2 is None:\n"
            "        return head_1\n\n"
            "    if head_1.val < head_2.val:\n"
            "        head_1.next = merge_lists(head_1.next, head_2)\n"
            "        return head_1\n"
            "    else:\n"
            "        head_2.next = merge_lists(head_1, head_2.next)\n"
            "        return head_2\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n"
            "def print_list(head):\n"
            "    vals = []\n"
            "    curr = head\n"
            "    while curr:\n"
            "        vals.append(str(curr.val))\n"
            "        curr = curr.next\n"
            "    return ' -> '.join(vals)\n\n"
            "a = Node(5)\n"
            "b = Node(7)\n"
            "c = Node(10)\n"
            "a.next = b\n"
            "b.next = c\n\n"
            "q = Node(6)\n"
            "r = Node(8)\n"
            "s = Node(9)\n"
            "q.next = r\n"
            "r.next = s\n\n"
            "print(print_list(merge_lists(a, q))) # -> 5 -> 6 -> 7 -> 8 -> 9 -> 10\n"
        ),
        "time_complexity": "O(min(n, m))",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Compares node values and splices pointers in-place, running in time bounded by the shorter list with O(1) iterative space (O(min(n, m)) recursive stack)."
        ),
    },
    {
        "id": "is_univalue_list",
        "title": "28. is univalue list",
        "raw_title": "is univalue list",
        "category": "Linked List",
        "description": (
            "Write a function, is_univalue_list, that takes in the head of a linked list as an argument. "
            "The function should return a boolean indicating whether or not the linked list contains exactly one unique value.\n\n"
            "You may assume that the input list is non-empty."
        ),
        "examples": (
            "u = Node(7)\n"
            "v = Node(7)\n"
            "w = Node(7)\n"
            "u.next = v\n"
            "v.next = w\n"
            "is_univalue_list(u) # -> True\n\n"
            "a = Node(7)\n"
            "b = Node(4)\n"
            "a.next = b\n"
            "is_univalue_list(a) # -> False"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def is_univalue_list(head):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Iterative Approach ===\n"
            "def is_univalue_list(head):\n"
            "    current = head\n"
            "    while current is not None:\n"
            "        if current.val != head.val:\n"
            "            return False\n"
            "        current = current.next\n"
            "    return True\n\n\n"
            "# === Recursive Approach ===\n"
            "def is_univalue_list(head, prev_val=None):\n"
            "    if head is None:\n"
            "        return True\n"
            "    if prev_val is None or head.val == prev_val:\n"
            "        return is_univalue_list(head.next, head.val)\n"
            "    else:\n"
            "        return False\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n"
            "u = Node(7)\n"
            "v = Node(7)\n"
            "w = Node(7)\n"
            "u.next = v\n"
            "v.next = w\n"
            "print(is_univalue_list(u)) # -> True\n\n"
            "a = Node(7)\n"
            "b = Node(4)\n"
            "a.next = b\n"
            "print(is_univalue_list(a)) # -> False\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Traverses the list until a mismatch is found or all n nodes are verified, using O(1) space iteratively (O(n) recursive stack)."
        ),
    },
    {
        "id": "longest_streak",
        "title": "29. longest streak",
        "raw_title": "longest streak",
        "category": "Linked List",
        "description": (
            "Write a function, longest_streak, that takes in the head of a linked list as an argument. "
            "The function should return the length of the longest consecutive streak of the same value within the list."
        ),
        "examples": (
            "a = Node(5)\n"
            "b = Node(5)\n"
            "c = Node(7)\n"
            "d = Node(7)\n"
            "e = Node(7)\n"
            "f = Node(6)\n\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n"
            "d.next = e\n"
            "e.next = f\n\n"
            "longest_streak(a) # -> 3\n\n"
            "longest_streak(None) # -> 0"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def longest_streak(head):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Iterative Approach ===\n"
            "def longest_streak(head):\n"
            "    max_streak = 0\n"
            "    current_streak = 0\n"
            "    prev_val = None\n\n"
            "    current_node = head\n"
            "    while current_node is not None:\n"
            "        if current_node.val == prev_val:\n"
            "            current_streak += 1\n"
            "        else:\n"
            "            current_streak = 1\n\n"
            "        prev_val = current_node.val\n"
            "        if current_streak > max_streak:\n"
            "            max_streak = current_streak\n\n"
            "        current_node = current_node.next\n\n"
            "    return max_streak\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n"
            "a = Node(5)\n"
            "b = Node(5)\n"
            "c = Node(7)\n"
            "d = Node(7)\n"
            "e = Node(7)\n"
            "f = Node(6)\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n"
            "d.next = e\n"
            "e.next = f\n\n"
            "print(longest_streak(a))    # -> 3\n"
            "print(longest_streak(None)) # -> 0\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Iterates through the n nodes tracking the maximum contiguous run of identical node values, in O(1) auxiliary space."
        ),
    },
    {
        "id": "remove_node",
        "title": "30. remove node",
        "raw_title": "remove node",
        "category": "Linked List",
        "description": (
            "Write a function, remove_node, that takes in the head of a linked list and a target value as arguments. "
            "The function should delete the node containing the target value from the linked list and return the head of the resulting linked list. "
            "If the target appears multiple times in the linked list, only remove the first instance of the target in the list.\n\n"
            "Do this in-place.\n\n"
            "You may assume that the input list is non-empty.\n\n"
            "You may assume that the input list contains the target."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n"
            "d.next = e\n"
            "e.next = f\n\n"
            "remove_node(a, 'c') # -> a -> b -> d -> e -> f"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def remove_node(head, target_val):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Iterative Approach ===\n"
            "def remove_node(head, target_val):\n"
            "    if head.val == target_val:\n"
            "        return head.next\n\n"
            "    current = head\n"
            "    prev = None\n"
            "    while current is not None:\n"
            "        if current.val == target_val:\n"
            "            prev.next = current.next\n"
            "            break\n"
            "        prev = current\n"
            "        current = current.next\n"
            "    return head\n\n\n"
            "# === Recursive Approach ===\n"
            "def remove_node(head, target_val):\n"
            "    if head is None:\n"
            "        return None\n\n"
            "    if head.val == target_val:\n"
            "        return head.next\n\n"
            "    head.next = remove_node(head.next, target_val)\n"
            "    return head\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n"
            "def print_list(head):\n"
            "    vals = []\n"
            "    curr = head\n"
            "    while curr:\n"
            "        vals.append(str(curr.val))\n"
            "        curr = curr.next\n"
            "    return ' -> '.join(vals)\n\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n"
            "d.next = e\n"
            "e.next = f\n\n"
            "print(print_list(remove_node(a, 'c'))) # -> a -> b -> d -> e -> f\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Searches for the target node and rewires the preceding pointer in-place, using O(1) space iteratively (O(n) recursive stack frames)."
        ),
    },
    {
        "id": "insert_node",
        "title": "31. insert node",
        "raw_title": "insert node",
        "category": "Linked List",
        "description": (
            "Write a function, insert_node, that takes in the head of a linked list, a value, and an index. "
            "The function should insert a new node with the value into the list at the specified index. "
            "Consider the head of the linked list as index 0. The function should return the head of the resulting linked list.\n\n"
            "Do this in-place.\n\n"
            "You may assume that the input list is non-empty and the index is not greater than the length of the input list."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n\n"
            "insert_node(a, 'x', 2) # -> a -> b -> x -> c -> d\n"
            "insert_node(a, 'm', 0) # -> m -> a -> b -> c -> d"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def insert_node(head, value, index):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Iterative Approach ===\n"
            "def insert_node(head, value, index):\n"
            "    if index == 0:\n"
            "        new_head = Node(value)\n"
            "        new_head.next = head\n"
            "        return new_head\n\n"
            "    count = 0\n"
            "    current = head\n"
            "    while current is not None:\n"
            "        if count == index - 1:\n"
            "            temp = current.next\n"
            "            current.next = Node(value)\n"
            "            current.next.next = temp\n"
            "            break\n\n"
            "        count += 1\n"
            "        current = current.next\n"
            "    return head\n\n\n"
            "# === Recursive Approach ===\n"
            "def insert_node(head, value, index, count=0):\n"
            "    if index == 0:\n"
            "        new_head = Node(value)\n"
            "        new_head.next = head\n"
            "        return new_head\n\n"
            "    if head is None:\n"
            "        return None\n\n"
            "    if count == index - 1:\n"
            "        temp = head.next\n"
            "        head.next = Node(value)\n"
            "        head.next.next = temp\n"
            "        return head\n\n"
            "    insert_node(head.next, value, index, count + 1)\n"
            "    return head\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n"
            "def print_list(head):\n"
            "    vals = []\n"
            "    curr = head\n"
            "    while curr:\n"
            "        vals.append(str(curr.val))\n"
            "        curr = curr.next\n"
            "    return ' -> '.join(vals)\n\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n\n"
            "print(print_list(insert_node(a, 'x', 2))) # -> a -> b -> x -> c -> d\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Advances up to the target index (at most n steps) to splice in the new Node, running in O(1) space iteratively (O(n) recursive stack)."
        ),
    },
    {
        "id": "depth_first_values",
        "title": "32. depth first values",
        "raw_title": "depth first values",
        "category": "Tree",
        "description": (
            "Write a function, depth_first_values, that takes in the root of a binary tree. "
            "The function should return a list containing all values of the tree in depth-first order."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "#      a\n"
            "#    /   \\\n"
            "#   b     c\n"
            "#  / \\     \\\n"
            "# d   e     f\n\n"
            "depth_first_values(a)\n"
            "#   -> ['a', 'b', 'd', 'e', 'c', 'f']"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def depth_first_values(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Iterative Approach (Stack) ===\n"
            "def depth_first_values(root):\n"
            "    if not root:\n"
            "        return []\n\n"
            "    stack = [root]\n"
            "    values = []\n\n"
            "    while stack:\n"
            "        node = stack.pop()\n"
            "        values.append(node.val)\n"
            "        if node.right:\n"
            "            stack.append(node.right)\n"
            "        if node.left:\n"
            "            stack.append(node.left)\n"
            "    return values\n\n\n"
            "# === Recursive Approach ===\n"
            "def depth_first_values_recursive(root):\n"
            "    if not root:\n"
            "        return []\n\n"
            "    left_values = depth_first_values_recursive(root.left)\n"
            "    right_values = depth_first_values_recursive(root.right)\n"
            "    return [root.val, *left_values, *right_values]\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "print(depth_first_values(a)) # -> ['a', 'b', 'd', 'e', 'c', 'f']\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Visits every node once with O(1) stack operations, accumulating n values into an array in O(n) space."
        ),
    },
    {
        "id": "breadth_first_values",
        "title": "33. breadth first values",
        "raw_title": "breadth first values",
        "category": "Tree",
        "description": (
            "Write a function, breadth_first_values, that takes in the root of a binary tree. "
            "The function should return a list containing all values of the tree in breadth-first order."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "#      a\n"
            "#    /   \\\n"
            "#   b     c\n"
            "#  / \\     \\\n"
            "# d   e     f\n\n"
            "breadth_first_values(a)\n"
            "#    -> ['a', 'b', 'c', 'd', 'e', 'f']"
        ),
        "starter_code": (
            "from collections import deque\n\n"
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def breadth_first_values(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import deque\n\n"
            "def breadth_first_values(root):\n"
            "    if not root:\n"
            "        return []\n\n"
            "    queue = deque([root])\n"
            "    values = []\n\n"
            "    while queue:\n"
            "        node = queue.popleft()\n"
            "        values.append(node.val)\n\n"
            "        if node.left:\n"
            "            queue.append(node.left)\n"
            "        if node.right:\n"
            "            queue.append(node.right)\n\n"
            "    return values\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "print(breadth_first_values(a)) # -> ['a', 'b', 'c', 'd', 'e', 'f']\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Traverses all n nodes level by level using a queue with O(1) push and popleft operations, using O(n) auxiliary memory."
        ),
    },
    {
        "id": "tree_sum",
        "title": "34. tree sum",
        "raw_title": "tree sum",
        "category": "Tree",
        "description": (
            "Write a function, tree_sum, that takes in the root of a binary tree that contains number values. "
            "The function should return the total sum of all values in the tree."
        ),
        "examples": (
            "a = Node(3)\n"
            "b = Node(11)\n"
            "c = Node(4)\n"
            "d = Node(4)\n"
            "e = Node(-2)\n"
            "f = Node(1)\n\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "#       3\n"
            "#    /    \\\n"
            "#   11     4\n"
            "#  / \\      \\\n"
            "# 4  -2      1\n\n"
            "tree_sum(a) # -> 21\n"
            "tree_sum(None) # -> 0"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def tree_sum(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import deque\n\n"
            "# === Depth-First Search (Recursive) ===\n"
            "def tree_sum(root):\n"
            "    if root is None:\n"
            "        return 0\n"
            "    return root.val + tree_sum(root.left) + tree_sum(root.right)\n\n\n"
            "# === Breadth-First Search (Iterative) ===\n"
            "def tree_sum_bfs(root):\n"
            "    if not root:\n"
            "        return 0\n\n"
            "    queue = deque([root])\n"
            "    total_sum = 0\n"
            "    while queue:\n"
            "        node = queue.popleft()\n"
            "        total_sum += node.val\n\n"
            "        if node.left:\n"
            "            queue.append(node.left)\n"
            "        if node.right:\n"
            "            queue.append(node.right)\n\n"
            "    return total_sum\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "a = Node(3)\n"
            "b = Node(11)\n"
            "c = Node(4)\n"
            "d = Node(4)\n"
            "e = Node(-2)\n"
            "f = Node(1)\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "print(tree_sum(a))    # -> 21\n"
            "print(tree_sum(None)) # -> 0\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Visits each of the n nodes once, accumulating the sum with O(n) memory on the call stack or queue."
        ),
    },
    {
        "id": "tree_includes",
        "title": "35. tree includes",
        "raw_title": "tree includes",
        "category": "Tree",
        "description": (
            "Write a function, tree_includes, that takes in the root of a binary tree and a target value. "
            "The function should return a boolean indicating whether or not the value is contained in the tree."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "tree_includes(a, 'e')    # -> True\n"
            "tree_includes(a, 'n')    # -> False\n"
            "tree_includes(None, 'b') # -> False"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def tree_includes(root, target):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import deque\n\n"
            "# === Depth-First Search (Recursive) ===\n"
            "def tree_includes(root, target):\n"
            "    if not root:\n"
            "        return False\n"
            "    if root.val == target:\n"
            "        return True\n"
            "    return tree_includes(root.left, target) or tree_includes(root.right, target)\n\n\n"
            "# === Breadth-First Search (Iterative) ===\n"
            "def tree_includes_bfs(root, target):\n"
            "    if not root:\n"
            "        return False\n\n"
            "    queue = deque([root])\n"
            "    while queue:\n"
            "        node = queue.popleft()\n"
            "        if node.val == target:\n"
            "            return True\n\n"
            "        if node.left:\n"
            "            queue.append(node.left)\n"
            "        if node.right:\n"
            "            queue.append(node.right)\n\n"
            "    return False\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "print(tree_includes(a, 'e'))    # -> True\n"
            "print(tree_includes(a, 'n'))    # -> False\n"
            "print(tree_includes(None, 'b')) # -> False\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Searches up to n nodes until the target is found, utilizing O(n) space in the call stack or queue."
        ),
    },
    {
        "id": "tree_min_value",
        "title": "36. tree min value",
        "raw_title": "tree min value",
        "category": "Tree",
        "description": (
            "Write a function, tree_min_value, that takes in the root of a binary tree that contains number values. "
            "The function should return the minimum value within the tree.\n\n"
            "You may assume that the input tree is non-empty."
        ),
        "examples": (
            "a = Node(3)\n"
            "b = Node(11)\n"
            "c = Node(4)\n"
            "d = Node(4)\n"
            "e = Node(-2)\n"
            "f = Node(1)\n\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "tree_min_value(a) # -> -2"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def tree_min_value(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Depth-First Search (Recursive) ===\n"
            "def tree_min_value(root):\n"
            "    if root is None:\n"
            "        return float('inf')\n"
            "    smallest_left = tree_min_value(root.left)\n"
            "    smallest_right = tree_min_value(root.right)\n"
            "    return min(root.val, smallest_left, smallest_right)\n\n\n"
            "# === Depth-First Search (Iterative with Stack) ===\n"
            "def tree_min_value_iterative(root):\n"
            "    stack = [root]\n"
            "    smallest = float('inf')\n"
            "    while stack:\n"
            "        current = stack.pop()\n"
            "        if current.val < smallest:\n"
            "            smallest = current.val\n\n"
            "        if current.left is not None:\n"
            "            stack.append(current.left)\n"
            "        if current.right is not None:\n"
            "            stack.append(current.right)\n\n"
            "    return smallest\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "a = Node(3)\n"
            "b = Node(11)\n"
            "c = Node(4)\n"
            "d = Node(4)\n"
            "e = Node(-2)\n"
            "f = Node(1)\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "print(tree_min_value(a)) # -> -2\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Traverses all n nodes to evaluate the global minimum, maintaining at most O(n) auxiliary space on the stack."
        ),
    },
    {
        "id": "max_path_sum",
        "title": "37. max root to leaf path sum",
        "raw_title": "max root to leaf path sum",
        "category": "Tree",
        "description": (
            "Write a function, max_path_sum, that takes in the root of a binary tree that contains number values. "
            "The function should return the maximum sum of any root to leaf path within the tree.\n\n"
            "You may assume that the input tree is non-empty."
        ),
        "examples": (
            "a = Node(3)\n"
            "b = Node(11)\n"
            "c = Node(4)\n"
            "d = Node(4)\n"
            "e = Node(-2)\n"
            "f = Node(1)\n\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "#       3\n"
            "#    /    \\\n"
            "#   11     4\n"
            "#  / \\      \\\n"
            "# 4  -2      1\n\n"
            "max_path_sum(a) # -> 18 (3 + 11 + 4)"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def max_path_sum(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Depth-First Search (Recursive) ===\n"
            "def max_path_sum(root):\n"
            "    if root is None:\n"
            "        return float('-inf')\n\n"
            "    if root.left is None and root.right is None:\n"
            "        return root.val\n\n"
            "    return root.val + max(max_path_sum(root.left), max_path_sum(root.right))\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "a = Node(3)\n"
            "b = Node(11)\n"
            "c = Node(4)\n"
            "d = Node(4)\n"
            "e = Node(-2)\n"
            "f = Node(1)\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "print(max_path_sum(a)) # -> 18\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Evaluates all paths from root to leaves in O(n) time, using O(n) space on the recursive call stack."
        ),
    },
    {
        "id": "tree_path_finder",
        "title": "38. tree path finder",
        "raw_title": "tree path finder",
        "category": "Tree",
        "description": (
            "Write a function, path_finder, that takes in the root of a binary tree and a target value. "
            "The function should return an array representing a path to the target value. "
            "If the target value is not found in the tree, then return None.\n\n"
            "You may assume that the tree contains unique values."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "path_finder(a, 'e') # -> ['a', 'b', 'e']\n"
            "path_finder(a, 'p') # -> None"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def path_finder(root, target):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Optimized Depth-First (O(n) with append and reverse) ===\n"
            "def path_finder(root, target):\n"
            "    result = _path_finder(root, target)\n"
            "    if result is None:\n"
            "        return None\n"
            "    return result[::-1]\n\n"
            "def _path_finder(root, target):\n"
            "    if root is None:\n"
            "        return None\n\n"
            "    if root.val == target:\n"
            "        return [root.val]\n\n"
            "    left_path = _path_finder(root.left, target)\n"
            "    if left_path is not None:\n"
            "        left_path.append(root.val)\n"
            "        return left_path\n\n"
            "    right_path = _path_finder(root.right, target)\n"
            "    if right_path is not None:\n"
            "        right_path.append(root.val)\n"
            "        return right_path\n\n"
            "    return None\n\n\n"
            "# === Depth-First Search (Spread operator) ===\n"
            "# Note: creating new lists with * unpack takes O(n) per node, resulting in O(n²) time\n"
            "def path_finder_spread(root, target):\n"
            "    if root is None:\n"
            "        return None\n\n"
            "    if root.val == target:\n"
            "        return [root.val]\n\n"
            "    left_path = path_finder_spread(root.left, target)\n"
            "    if left_path is not None:\n"
            "        return [root.val, *left_path]\n\n"
            "    right_path = path_finder_spread(root.right, target)\n"
            "    if right_path is not None:\n"
            "        return [root.val, *right_path]\n\n"
            "    return None\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "print(path_finder(a, 'e')) # -> ['a', 'b', 'e']\n"
            "print(path_finder(a, 'p')) # -> None\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Searches the tree for target and appends elements to path in O(1) time per level, reversing once at the end for O(n) total time and space."
        ),
    },
    {
        "id": "tree_value_count",
        "title": "39. tree value count",
        "raw_title": "tree value count",
        "category": "Tree",
        "description": (
            "Write a function, tree_value_count, that takes in the root of a binary tree and a target value. "
            "The function should return the number of times that the target occurs in the tree."
        ),
        "examples": (
            "a = Node(12)\n"
            "b = Node(6)\n"
            "c = Node(6)\n"
            "d = Node(4)\n"
            "e = Node(6)\n"
            "f = Node(12)\n\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "tree_value_count(a, 6)  # -> 3\n"
            "tree_value_count(a, 12) # -> 2\n"
            "tree_value_count(a, 99) # -> 0"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def tree_value_count(root, target):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import deque\n\n"
            "# === Depth-First Search (Recursive) ===\n"
            "def tree_value_count(root, target):\n"
            "    if root is None:\n"
            "        return 0\n\n"
            "    match = 1 if root.val == target else 0\n"
            "    return match + tree_value_count(root.left, target) + tree_value_count(root.right, target)\n\n\n"
            "# === Depth-First Search (Iterative Stack) ===\n"
            "def tree_value_count_dfs_iterative(root, target):\n"
            "    if root is None:\n"
            "        return 0\n\n"
            "    count = 0\n"
            "    stack = [root]\n"
            "    while stack:\n"
            "        current = stack.pop()\n"
            "        if current.val == target:\n"
            "            count += 1\n\n"
            "        if current.left is not None:\n"
            "            stack.append(current.left)\n"
            "        if current.right is not None:\n"
            "            stack.append(current.right)\n\n"
            "    return count\n\n\n"
            "# === Breadth-First Search (Queue) ===\n"
            "def tree_value_count_bfs(root, target):\n"
            "    if root is None:\n"
            "        return 0\n\n"
            "    count = 0\n"
            "    queue = deque([root])\n"
            "    while queue:\n"
            "        current = queue.popleft()\n"
            "        if current.val == target:\n"
            "            count += 1\n\n"
            "        if current.left is not None:\n"
            "            queue.append(current.left)\n"
            "        if current.right is not None:\n"
            "            queue.append(current.right)\n\n"
            "    return count\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "a = Node(12)\n"
            "b = Node(6)\n"
            "c = Node(6)\n"
            "d = Node(4)\n"
            "e = Node(6)\n"
            "f = Node(12)\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "print(tree_value_count(a, 6))  # -> 3\n"
            "print(tree_value_count(a, 12)) # -> 2\n"
            "print(tree_value_count(a, 99)) # -> 0\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Traverses all n nodes in the tree, counting matches against target in linear time with O(n) auxiliary queue or stack space."
        ),
    },
    {
        "id": "how_high",
        "title": "40. how high",
        "raw_title": "how high",
        "category": "Tree",
        "description": (
            "Write a function, how_high, that takes in the root of a binary tree. "
            "The function should return a number representing the height of the tree.\n\n"
            "The height of a binary tree is defined as the maximal number of edges from the root node to any leaf node.\n\n"
            "If the tree is empty, return -1."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "how_high(a) # -> 2\n\n"
            "# Single node tree:\n"
            "g = Node('g')\n"
            "how_high(g) # -> 0\n\n"
            "# Empty tree:\n"
            "how_high(None) # -> -1"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def how_high(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import deque\n\n"
            "# === Depth-First Search (Recursive) ===\n"
            "def how_high(root):\n"
            "    if root is None:\n"
            "        return -1\n\n"
            "    left_height = how_high(root.left)\n"
            "    right_height = how_high(root.right)\n"
            "    return 1 + max(left_height, right_height)\n\n\n"
            "# === Breadth-First Search (Iterative Queue) ===\n"
            "def how_high_bfs(root):\n"
            "    queue = deque([])\n"
            "    if root is not None:\n"
            "        queue.append((root, 0))\n\n"
            "    max_depth = -1\n"
            "    while queue:\n"
            "        node, depth = queue.popleft()\n"
            "        max_depth = max(max_depth, depth)\n"
            "        if node.left is not None:\n"
            "            queue.append((node.left, depth + 1))\n"
            "        if node.right is not None:\n"
            "            queue.append((node.right, depth + 1))\n\n"
            "    return max_depth\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "print(how_high(a))         # -> 2\n"
            "print(how_high(Node('g'))) # -> 0\n"
            "print(how_high(None))      # -> -1\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Visits each node once in linear O(n) time, using O(n) auxiliary call stack space in the worst case (for skewed trees)."
        ),
    },
    {
        "id": "bottom_right_value",
        "title": "41. bottom right value",
        "raw_title": "bottom right value",
        "category": "Tree",
        "description": (
            "Write a function, bottom_right_value, that takes in the root of a binary tree. "
            "The function should return the right-most value in the bottom-most level of the tree.\n\n"
            "You may assume that the input tree is non-empty."
        ),
        "examples": (
            "a = Node(3)\n"
            "b = Node(11)\n"
            "c = Node(10)\n"
            "d = Node(4)\n"
            "e = Node(-2)\n"
            "f = Node(1)\n\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "#       3\n"
            "#    /    \\\n"
            "#   11     10\n"
            "#  / \\       \\\n"
            "# 4   -2      1\n\n"
            "bottom_right_value(a) # -> 1"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def bottom_right_value(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import deque\n\n"
            "# === Breadth-First Search (Iterative Queue) ===\n"
            "def bottom_right_value(root):\n"
            "    queue = deque([root])\n"
            "    current = None\n\n"
            "    while queue:\n"
            "        current = queue.popleft()\n\n"
            "        if current.left is not None:\n"
            "            queue.append(current.left)\n"
            "        if current.right is not None:\n"
            "            queue.append(current.right)\n\n"
            "    return current.val\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "a = Node(3)\n"
            "b = Node(11)\n"
            "c = Node(10)\n"
            "d = Node(4)\n"
            "e = Node(-2)\n"
            "f = Node(1)\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "print(bottom_right_value(a)) # -> 1\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Traverses the tree level-by-level in O(n) time using a queue of up to O(n) capacity. The last popped element is guaranteed to be the bottom-rightmost node."
        ),
    },
    {
        "id": "all_tree_paths",
        "title": "42. all tree paths",
        "raw_title": "all tree paths",
        "category": "Tree",
        "description": (
            "Write a function, all_tree_paths, that takes in the root of a binary tree. "
            "The function should return a 2-Dimensional list where each subarray represents a root-to-leaf path in the tree.\n\n"
            "The order within an individual path must start at the root and end at the leaf, "
            "but the relative order among paths in the outer list does not matter.\n\n"
            "You may assume that the input tree is non-empty."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "all_tree_paths(a) # ->\n"
            "# [ \n"
            "#   [ 'a', 'b', 'd' ], \n"
            "#   [ 'a', 'b', 'e' ], \n"
            "#   [ 'a', 'c', 'f' ] \n"
            "# ]"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def all_tree_paths(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Recursive Path Collector (Depth-First) ===\n"
            "def all_tree_paths(root):\n"
            "    paths = _all_tree_paths(root)\n"
            "    for path in paths:\n"
            "        path.reverse()\n"
            "    return paths\n\n"
            "def _all_tree_paths(root):\n"
            "    if root is None:\n"
            "        return []\n\n"
            "    if root.left is None and root.right is None:\n"
            "        return [[root.val]]\n\n"
            "    all_paths = []\n"
            "    left_sub_paths = _all_tree_paths(root.left)\n"
            "    for path in left_sub_paths:\n"
            "        path.append(root.val)\n"
            "        all_paths.append(path)\n\n"
            "    right_sub_paths = _all_tree_paths(root.right)\n"
            "    for path in right_sub_paths:\n"
            "        path.append(root.val)\n"
            "        all_paths.append(path)\n\n"
            "    return all_paths\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "print(all_tree_paths(a))\n"
            "# -> [ ['a', 'b', 'd'], ['a', 'b', 'e'], ['a', 'c', 'f'] ]\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Visits all n nodes recursively, constructing root-to-leaf subarrays with O(n) total path elements and call stack space."
        ),
    },
    {
        "id": "tree_levels",
        "title": "43. tree levels",
        "raw_title": "tree levels",
        "category": "Tree",
        "description": (
            "Write a function, tree_levels, that takes in the root of a binary tree. "
            "The function should return a 2-Dimensional list where each sublist represents a level of the tree."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "#      a\n"
            "#    /   \\\n"
            "#   b     c\n"
            "#  / \\     \\\n"
            "# d   e     f\n\n"
            "tree_levels(a) # ->\n"
            "# [\n"
            "#   ['a'],\n"
            "#   ['b', 'c'],\n"
            "#   ['d', 'e', 'f']\n"
            "# ]"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def tree_levels(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import deque\n\n"
            "# === Breadth-First Search (Iterative Queue) ===\n"
            "def tree_levels(root):\n"
            "    if root is None:\n"
            "        return []\n\n"
            "    levels = []\n"
            "    queue = deque([(root, 0)])\n"
            "    while queue:\n"
            "        current, level_num = queue.popleft()\n\n"
            "        if len(levels) == level_num:\n"
            "            levels.append([current.val])\n"
            "        else:\n"
            "            levels[level_num].append(current.val)\n\n"
            "        if current.left is not None:\n"
            "            queue.append((current.left, level_num + 1))\n"
            "        if current.right is not None:\n"
            "            queue.append((current.right, level_num + 1))\n\n"
            "    return levels\n\n\n"
            "# === Depth-First Search (Recursive) ===\n"
            "def tree_levels_dfs(root):\n"
            "    levels = []\n"
            "    _fill_levels(root, levels, 0)\n"
            "    return levels\n\n"
            "def _fill_levels(root, levels, level_num):\n"
            "    if root is None:\n"
            "        return\n\n"
            "    if len(levels) == level_num:\n"
            "        levels.append([root.val])\n"
            "    else:\n"
            "        levels[level_num].append(root.val)\n\n"
            "    _fill_levels(root.left, levels, level_num + 1)\n"
            "    _fill_levels(root.right, levels, level_num + 1)\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "print(tree_levels(a))\n"
            "# -> [ ['a'], ['b', 'c'], ['d', 'e', 'f'] ]\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Traverses all n nodes once while recording level numbers, organizing nodes into level buckets in O(n) time and O(n) auxiliary space."
        ),
    },
    {
        "id": "level_averages",
        "title": "44. level averages",
        "raw_title": "level averages",
        "category": "Tree",
        "description": (
            "Write a function, level_averages, that takes in the root of a binary tree that contains number values. "
            "The function should return a list containing the average value of each level."
        ),
        "examples": (
            "a = Node(3)\n"
            "b = Node(11)\n"
            "c = Node(4)\n"
            "d = Node(4)\n"
            "e = Node(-2)\n"
            "f = Node(1)\n\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "#       3\n"
            "#    /    \\\n"
            "#   11     4\n"
            "#  / \\      \\\n"
            "# 4   -2     1\n\n"
            "level_averages(a) # -> [ 3.0, 7.5, 1.0 ]"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def level_averages(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from statistics import mean\n"
            "from collections import deque\n\n"
            "# === Depth-First Search (Recursive) ===\n"
            "def level_averages(root):\n"
            "    levels = []\n"
            "    fill_levels(root, levels, 0)\n"
            "    avgs = []\n"
            "    for level in levels:\n"
            "        avgs.append(mean(level))\n"
            "    return avgs\n\n"
            "def fill_levels(root, levels, level_num):\n"
            "    if root is None:\n"
            "        return\n\n"
            "    if level_num == len(levels):\n"
            "        levels.append([root.val])\n"
            "    else:\n"
            "        levels[level_num].append(root.val)\n\n"
            "    fill_levels(root.left, levels, level_num + 1)\n"
            "    fill_levels(root.right, levels, level_num + 1)\n\n\n"
            "# === Breadth-First Search (Iterative Queue) ===\n"
            "def level_averages_bfs(root):\n"
            "    if root is None:\n"
            "        return []\n\n"
            "    levels = []\n"
            "    queue = deque([(root, 0)])\n"
            "    while queue:\n"
            "        current, level_num = queue.popleft()\n"
            "        if len(levels) == level_num:\n"
            "            levels.append([current.val])\n"
            "        else:\n"
            "            levels[level_num].append(current.val)\n\n"
            "        if current.left is not None:\n"
            "            queue.append((current.left, level_num + 1))\n"
            "        if current.right is not None:\n"
            "            queue.append((current.right, level_num + 1))\n\n"
            "    return [mean(lvl) for lvl in levels]\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "a = Node(3)\n"
            "b = Node(11)\n"
            "c = Node(4)\n"
            "d = Node(4)\n"
            "e = Node(-2)\n"
            "f = Node(1)\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "print(level_averages(a))     # -> [3.0, 7.5, 1.0]\n"
            "print(level_averages_bfs(a)) # -> [3.0, 7.5, 1.0]\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Gathers nodes across all levels in linear O(n) time and computes each level mean in O(n) total operations with O(n) space."
        ),
    },
    {
        "id": "leaf_list",
        "title": "45. leaf list",
        "raw_title": "leaf list",
        "category": "Tree",
        "description": (
            "Write a function, leaf_list, that takes in the root of a binary tree and "
            "returns a list containing the values of all leaf nodes in left-to-right order."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "#      a\n"
            "#    /   \\\n"
            "#   b     c\n"
            "#  / \\     \\\n"
            "# d   e     f\n\n"
            "leaf_list(a) # -> [ 'd', 'e', 'f' ]"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def leaf_list(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Depth-First Search (Iterative Stack) ===\n"
            "def leaf_list(root):\n"
            "    if root is None:\n"
            "        return []\n\n"
            "    leaves = []\n"
            "    stack = [root]\n"
            "    while stack:\n"
            "        current = stack.pop()\n"
            "        if current.left is None and current.right is None:\n"
            "            leaves.append(current.val)\n\n"
            "        if current.right is not None:\n"
            "            stack.append(current.right)\n"
            "        if current.left is not None:\n"
            "            stack.append(current.left)\n\n"
            "    return leaves\n\n\n"
            "# === Depth-First Search (Recursive) ===\n"
            "def leaf_list_recursive(root):\n"
            "    leaves = []\n"
            "    _leaf_list(root, leaves)\n"
            "    return leaves\n\n"
            "def _leaf_list(root, leaves):\n"
            "    if root is None:\n"
            "        return\n\n"
            "    if root.left is None and root.right is None:\n"
            "        leaves.append(root.val)\n\n"
            "    _leaf_list(root.left, leaves)\n"
            "    _leaf_list(root.right, leaves)\n\n\n"
            "# === Example Test Cases ===\n"
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n"
            "a.left = b\n"
            "a.right = c\n"
            "b.left = d\n"
            "b.right = e\n"
            "c.right = f\n\n"
            "print(leaf_list(a))           # -> ['d', 'e', 'f']\n"
            "print(leaf_list_recursive(a)) # -> ['d', 'e', 'f']\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Visits all n nodes via depth-first traversal (pushing right child before left child to process left-to-right), gathering leaves in O(n) time and O(n) auxiliary stack space."
        ),
    },
    {
        "id": "has_path",
        "title": "46. has path",
        "raw_title": "has path",
        "category": "Graph",
        "description": (
            "Write a function, has_path, that takes in a dictionary representing the adjacency list "
            "of a directed acyclic graph and two nodes (src, dst). The function should return a boolean "
            "indicating whether or not there exists a directed path between the source and destination nodes."
        ),
        "examples": (
            "graph = {\n"
            "  'f': ['g', 'i'],\n"
            "  'g': ['h'],\n"
            "  'h': [],\n"
            "  'i': ['g', 'k'],\n"
            "  'j': ['i'],\n"
            "  'k': []\n"
            "}\n\n"
            "has_path(graph, 'f', 'k') # -> True\n"
            "has_path(graph, 'f', 'j') # -> False"
        ),
        "starter_code": (
            "def has_path(graph, src, dst):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Depth-First Search (Recursive) ===\n"
            "def has_path(graph, src, dst):\n"
            "    if src == dst:\n"
            "        return True\n\n"
            "    for neighbor in graph[src]:\n"
            "        if has_path(graph, neighbor, dst):\n"
            "            return True\n\n"
            "    return False\n\n\n"
            "# === Breadth-First Search (Queue) ===\n"
            "from collections import deque\n\n"
            "def has_path_bfs(graph, src, dst):\n"
            "    queue = deque([src])\n\n"
            "    while queue:\n"
            "        current = queue.popleft()\n"
            "        if current == dst:\n"
            "            return True\n\n"
            "        for neighbor in graph[current]:\n"
            "            queue.append(neighbor)\n\n"
            "    return False\n\n\n"
            "# === Example Test Cases ===\n"
            "graph = {\n"
            "    'f': ['g', 'i'],\n"
            "    'g': ['h'],\n"
            "    'h': [],\n"
            "    'i': ['g', 'k'],\n"
            "    'j': ['i'],\n"
            "    'k': []\n"
            "}\n\n"
            "print(has_path(graph, 'f', 'k'))     # -> True\n"
            "print(has_path(graph, 'f', 'j'))     # -> False\n"
            "print(has_path_bfs(graph, 'f', 'k')) # -> True\n"
        ),
        "time_complexity": "O(e)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Traverses edges and nodes in the directed acyclic graph in O(e) time (or O(v + e)) with O(v) auxiliary space for the call stack or BFS queue."
        ),
    },
    {
        "id": "undirected_path",
        "title": "47. undirected path",
        "raw_title": "undirected path",
        "category": "Graph",
        "description": (
            "Write a function, undirected_path, that takes in a list of edges for an undirected graph "
            "and two nodes (node_A, node_B). The function should return a boolean indicating whether "
            "or not there exists a path between node_A and node_B.\n\n"
            "You can assume that node_A and node_B both exist in the graph."
        ),
        "examples": (
            "edges = [\n"
            "  ('i', 'j'),\n"
            "  ('k', 'i'),\n"
            "  ('m', 'k'),\n"
            "  ('k', 'l'),\n"
            "  ('o', 'n')\n"
            "]\n\n"
            "undirected_path(edges, 'j', 'm') # -> True\n"
            "undirected_path(edges, 'k', 'o') # -> False"
        ),
        "starter_code": (
            "def undirected_path(edges, node_A, node_B):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Depth-First Search with Visited Set ===\n"
            "def undirected_path(edges, node_A, node_B):\n"
            "    graph = build_graph(edges)\n"
            "    return has_path(graph, node_A, node_B, set())\n\n"
            "def build_graph(edges):\n"
            "    graph = {}\n"
            "    for edge in edges:\n"
            "        a, b = edge\n"
            "        if a not in graph:\n"
            "            graph[a] = []\n"
            "        if b not in graph:\n"
            "            graph[b] = []\n"
            "        graph[a].append(b)\n"
            "        graph[b].append(a)\n"
            "    return graph\n\n"
            "def has_path(graph, src, dst, visited):\n"
            "    if src == dst:\n"
            "        return True\n"
            "    if src in visited:\n"
            "        return False\n\n"
            "    visited.add(src)\n"
            "    for neighbor in graph[src]:\n"
            "        if has_path(graph, neighbor, dst, visited):\n"
            "            return True\n\n"
            "    return False\n\n\n"
            "# === Breadth-First Search with Visited Set ===\n"
            "from collections import deque\n\n"
            "def undirected_path_bfs(edges, node_A, node_B):\n"
            "    graph = build_graph(edges)\n"
            "    visited = {node_A}\n"
            "    queue = deque([node_A])\n\n"
            "    while queue:\n"
            "        node = queue.popleft()\n"
            "        if node == node_B:\n"
            "            return True\n"
            "        for neighbor in graph[node]:\n"
            "            if neighbor not in visited:\n"
            "                visited.add(neighbor)\n"
            "                queue.append(neighbor)\n\n"
            "    return False\n\n\n"
            "# === Example Test Cases ===\n"
            "edges = [\n"
            "    ('i', 'j'),\n"
            "    ('k', 'i'),\n"
            "    ('m', 'k'),\n"
            "    ('k', 'l'),\n"
            "    ('o', 'n')\n"
            "]\n\n"
            "print(undirected_path(edges, 'j', 'm'))     # -> True\n"
            "print(undirected_path(edges, 'k', 'o'))     # -> False\n"
            "print(undirected_path_bfs(edges, 'j', 'm')) # -> True\n"
        ),
        "time_complexity": "O(e)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Converts the edge list to an adjacency list in O(e) time and searches connected components in O(v + e) time using a visited set to avoid cycles, with O(v) auxiliary space."
        ),
    },
    {
        "id": "connected_components_count",
        "title": "48. connected components count",
        "raw_title": "connected components count",
        "category": "Graph",
        "description": (
            "Write a function, connected_components_count, that takes in the adjacency list "
            "of an undirected graph. The function should return the number of connected components within the graph."
        ),
        "examples": (
            "connected_components_count({\n"
            "  0: [8, 1, 5],\n"
            "  1: [0],\n"
            "  5: [0, 8],\n"
            "  8: [0, 5],\n"
            "  2: [3, 4],\n"
            "  3: [2, 4],\n"
            "  4: [3, 2]\n"
            "}) # -> 2"
        ),
        "starter_code": (
            "def connected_components_count(graph):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Depth-First Search ===\n"
            "def connected_components_count(graph):\n"
            "    visited = set()\n"
            "    count = 0\n"
            "    for node in graph:\n"
            "        if explore(graph, node, visited):\n"
            "            count += 1\n"
            "    return count\n\n"
            "def explore(graph, current, visited):\n"
            "    if current in visited:\n"
            "        return False\n\n"
            "    visited.add(current)\n"
            "    for neighbor in graph[current]:\n"
            "        explore(graph, neighbor, visited)\n\n"
            "    return True\n\n\n"
            "# === Breadth-First Search ===\n"
            "from collections import deque\n\n"
            "def connected_components_count_bfs(graph):\n"
            "    visited = set()\n"
            "    count = 0\n"
            "    for node in graph:\n"
            "        if explore_bfs(graph, node, visited):\n"
            "            count += 1\n"
            "    return count\n\n"
            "def explore_bfs(graph, src, visited):\n"
            "    if src in visited:\n"
            "        return False\n\n"
            "    visited.add(src)\n"
            "    queue = deque([src])\n"
            "    while queue:\n"
            "        current = queue.popleft()\n"
            "        for neighbor in graph[current]:\n"
            "            if neighbor not in visited:\n"
            "                visited.add(neighbor)\n"
            "                queue.append(neighbor)\n\n"
            "    return True\n\n\n"
            "# === Example Test Cases ===\n"
            "graph = {\n"
            "    0: [8, 1, 5],\n"
            "    1: [0],\n"
            "    5: [0, 8],\n"
            "    8: [0, 5],\n"
            "    2: [3, 4],\n"
            "    3: [2, 4],\n"
            "    4: [3, 2]\n"
            "}\n\n"
            "print(connected_components_count(graph))     # -> 2\n"
            "print(connected_components_count_bfs(graph)) # -> 2\n"
        ),
        "time_complexity": "O(e)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Visits each node and edge once across all components in O(v + e) total time. The visited set prevents reprocessing visited nodes, requiring O(v) auxiliary space."
        ),
    },
    {
        "id": "largest_component",
        "title": "49. largest component",
        "raw_title": "largest component",
        "category": "Graph",
        "description": (
            "Write a function, largest_component, that takes in the adjacency list of an undirected graph. "
            "The function should return the size of the largest connected component in the graph."
        ),
        "examples": (
            "largest_component({\n"
            "  0: [8, 1, 5],\n"
            "  1: [0],\n"
            "  5: [0, 8],\n"
            "  8: [0, 5],\n"
            "  2: [3, 4],\n"
            "  3: [2, 4],\n"
            "  4: [3, 2]\n"
            "}) # -> 4"
        ),
        "starter_code": (
            "def largest_component(graph):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Depth-First Search ===\n"
            "def largest_component(graph):\n"
            "    visited = set()\n"
            "    largest = 0\n"
            "    for node in graph:\n"
            "        size = explore_size(graph, node, visited)\n"
            "        if size > largest:\n"
            "            largest = size\n"
            "    return largest\n\n"
            "def explore_size(graph, node, visited):\n"
            "    if node in visited:\n"
            "        return 0\n\n"
            "    visited.add(node)\n"
            "    size = 1\n"
            "    for neighbor in graph[node]:\n"
            "        size += explore_size(graph, neighbor, visited)\n"
            "    return size\n\n\n"
            "# === Breadth-First Search ===\n"
            "from collections import deque\n\n"
            "def largest_component_bfs(graph):\n"
            "    visited = set()\n"
            "    largest = 0\n"
            "    for node in graph:\n"
            "        size = explore_size_bfs(graph, node, visited)\n"
            "        if size > largest:\n"
            "            largest = size\n"
            "    return largest\n\n"
            "def explore_size_bfs(graph, node, visited):\n"
            "    if node in visited:\n"
            "        return 0\n\n"
            "    visited.add(node)\n"
            "    size = 0\n"
            "    queue = deque([node])\n"
            "    while queue:\n"
            "        current = queue.popleft()\n"
            "        size += 1\n"
            "        for neighbor in graph[current]:\n"
            "            if neighbor not in visited:\n"
            "                visited.add(neighbor)\n"
            "                queue.append(neighbor)\n"
            "    return size\n\n\n"
            "# === Example Test Cases ===\n"
            "graph = {\n"
            "    0: [8, 1, 5],\n"
            "    1: [0],\n"
            "    5: [0, 8],\n"
            "    8: [0, 5],\n"
            "    2: [3, 4],\n"
            "    3: [2, 4],\n"
            "    4: [3, 2]\n"
            "}\n\n"
            "print(largest_component(graph))     # -> 4\n"
            "print(largest_component_bfs(graph)) # -> 4\n"
        ),
        "time_complexity": "O(e)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Measures each component size in O(v + e) total time across all nodes using a visited set to avoid re-visiting nodes. Requires O(v) auxiliary memory."
        ),
    },
    {
        "id": "shortest_path",
        "title": "50. shortest path",
        "raw_title": "shortest path",
        "category": "Graph",
        "description": (
            "Write a function, shortest_path, that takes in a list of edges for an undirected graph "
            "and two nodes (node_A, node_B). The function should return the length of the shortest path "
            "between A and B. Consider the length as the number of edges in the path, not the number of nodes. "
            "If there is no path between A and B, then return -1. You can assume that A and B exist as nodes in the graph."
        ),
        "examples": (
            "edges = [\n"
            "  ['w', 'x'],\n"
            "  ['x', 'y'],\n"
            "  ['z', 'y'],\n"
            "  ['z', 'v'],\n"
            "  ['w', 'v']\n"
            "]\n\n"
            "shortest_path(edges, 'w', 'z') # -> 2"
        ),
        "starter_code": (
            "def shortest_path(edges, node_A, node_B):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import deque\n\n"
            "def shortest_path(edges, node_A, node_B):\n"
            "    graph = build_graph(edges)\n"
            "    visited = {node_A}\n"
            "    queue = deque([(node_A, 0)])\n\n"
            "    while queue:\n"
            "        node, distance = queue.popleft()\n"
            "        if node == node_B:\n"
            "            return distance\n\n"
            "        for neighbor in graph[node]:\n"
            "            if neighbor not in visited:\n"
            "                visited.add(neighbor)\n"
            "                queue.append((neighbor, distance + 1))\n\n"
            "    return -1\n\n"
            "def build_graph(edges):\n"
            "    graph = {}\n"
            "    for edge in edges:\n"
            "        a, b = edge\n"
            "        if a not in graph:\n"
            "            graph[a] = []\n"
            "        if b not in graph:\n"
            "            graph[b] = []\n"
            "        graph[a].append(b)\n"
            "        graph[b].append(a)\n"
            "    return graph\n\n\n"
            "# === Example Test Cases ===\n"
            "edges = [\n"
            "    ['w', 'x'],\n"
            "    ['x', 'y'],\n"
            "    ['z', 'y'],\n"
            "    ['z', 'v'],\n"
            "    ['w', 'v']\n"
            "]\n\n"
            "print(shortest_path(edges, 'w', 'z')) # -> 2\n"
            "print(shortest_path(edges, 'y', 'w')) # -> 2\n"
            "print(shortest_path(edges, 'w', 'w')) # -> 0\n"
        ),
        "time_complexity": "O(e)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Breadth-First Search (BFS) is guaranteed to find the shortest edge path first. Builds the graph in O(e) time and explores nodes in O(v + e) time with O(v) queue space."
        ),
    },
    {
        "id": "island_count",
        "title": "51. island count",
        "raw_title": "island count",
        "category": "Graph",
        "description": (
            "Write a function, island_count, that takes in a grid containing Ws and Ls. "
            "W represents water and L represents land. The function should return the number of islands "
            "on the grid. An island is a vertically or horizontally connected region of land."
        ),
        "examples": (
            "grid = [\n"
            "  ['W', 'L', 'W', 'W', 'W'],\n"
            "  ['W', 'L', 'W', 'W', 'W'],\n"
            "  ['W', 'W', 'W', 'L', 'W'],\n"
            "  ['W', 'W', 'L', 'L', 'W'],\n"
            "  ['L', 'W', 'W', 'L', 'L'],\n"
            "  ['L', 'L', 'W', 'W', 'W'],\n"
            "]\n\n"
            "island_count(grid) # -> 3"
        ),
        "starter_code": (
            "def island_count(grid):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Depth-First Search ===\n"
            "def island_count(grid):\n"
            "    visited = set()\n"
            "    count = 0\n"
            "    for r in range(len(grid)):\n"
            "        for c in range(len(grid[0])):\n"
            "            if explore(grid, r, c, visited):\n"
            "                count += 1\n"
            "    return count\n\n"
            "def explore(grid, r, c, visited):\n"
            "    row_inbounds = 0 <= r < len(grid)\n"
            "    col_inbounds = 0 <= c < len(grid[0])\n"
            "    if not row_inbounds or not col_inbounds:\n"
            "        return False\n\n"
            "    if grid[r][c] == 'W':\n"
            "        return False\n\n"
            "    pos = (r, c)\n"
            "    if pos in visited:\n"
            "        return False\n"
            "    visited.add(pos)\n\n"
            "    explore(grid, r - 1, c, visited)\n"
            "    explore(grid, r + 1, c, visited)\n"
            "    explore(grid, r, c - 1, visited)\n"
            "    explore(grid, r, c + 1, visited)\n"
            "    return True\n\n\n"
            "# === Breadth-First Search ===\n"
            "from collections import deque\n\n"
            "def island_count_bfs(grid):\n"
            "    visited = set()\n"
            "    count = 0\n"
            "    for r in range(len(grid)):\n"
            "        for c in range(len(grid[0])):\n"
            "            if explore_bfs(grid, r, c, visited):\n"
            "                count += 1\n"
            "    return count\n\n"
            "def explore_bfs(grid, r, c, visited):\n"
            "    pos = (r, c)\n"
            "    if pos in visited or grid[r][c] == 'W':\n"
            "        return False\n"
            "    visited.add(pos)\n\n"
            "    deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]\n"
            "    queue = deque([pos])\n"
            "    while queue:\n"
            "        currentR, currentC = queue.popleft()\n"
            "        for delta in deltas:\n"
            "            dRow, dCol = delta\n"
            "            neighborR = dRow + currentR\n"
            "            neighborC = dCol + currentC\n"
            "            neighborPos = (neighborR, neighborC)\n"
            "            row_inbounds = 0 <= neighborR < len(grid)\n"
            "            col_inbounds = 0 <= neighborC < len(grid[0])\n"
            "            if neighborPos not in visited and row_inbounds and col_inbounds and grid[neighborR][neighborC] == 'L':\n"
            "                queue.append(neighborPos)\n"
            "                visited.add(neighborPos)\n"
            "    return True\n\n\n"
            "# === Example Test Cases ===\n"
            "grid = [\n"
            "    ['W', 'L', 'W', 'W', 'W'],\n"
            "    ['W', 'L', 'W', 'W', 'W'],\n"
            "    ['W', 'W', 'W', 'L', 'W'],\n"
            "    ['W', 'W', 'L', 'L', 'W'],\n"
            "    ['L', 'W', 'W', 'L', 'L'],\n"
            "    ['L', 'L', 'W', 'W', 'W'],\n"
            "]\n\n"
            "print(island_count(grid))     # -> 3\n"
            "print(island_count_bfs(grid)) # -> 3\n"
        ),
        "time_complexity": "O(r * c)",
        "space_complexity": "O(r * c)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Visits every coordinate in the r x c grid once and explores each connected land component in O(r * c) time with O(r * c) space for the visited coordinate set."
        ),
    },
    {
        "id": "minimum_island",
        "title": "52. minimum island",
        "raw_title": "minimum island",
        "category": "Graph",
        "description": (
            "Write a function, minimum_island, that takes in a grid containing Ws and Ls. "
            "W represents water and L represents land. The function should return the size of the smallest island. "
            "An island is a vertically or horizontally connected region of land.\n\n"
            "You may assume that the grid contains at least one island."
        ),
        "examples": (
            "grid = [\n"
            "  ['W', 'L', 'W', 'W', 'W'],\n"
            "  ['W', 'L', 'W', 'W', 'W'],\n"
            "  ['W', 'W', 'W', 'L', 'W'],\n"
            "  ['W', 'W', 'L', 'L', 'W'],\n"
            "  ['L', 'W', 'W', 'L', 'L'],\n"
            "  ['L', 'L', 'W', 'W', 'W'],\n"
            "]\n\n"
            "minimum_island(grid) # -> 2"
        ),
        "starter_code": (
            "def minimum_island(grid):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Depth-First Search ===\n"
            "def minimum_island(grid):\n"
            "    visited = set()\n"
            "    min_size = float('inf')\n"
            "    for r in range(len(grid)):\n"
            "        for c in range(len(grid[0])):\n"
            "            size = explore_size(grid, r, c, visited)\n"
            "            if 0 < size < min_size:\n"
            "                min_size = size\n"
            "    return min_size\n\n"
            "def explore_size(grid, r, c, visited):\n"
            "    row_inbounds = 0 <= r < len(grid)\n"
            "    col_inbounds = 0 <= c < len(grid[0])\n"
            "    if not row_inbounds or not col_inbounds:\n"
            "        return 0\n\n"
            "    if grid[r][c] == 'W':\n"
            "        return 0\n\n"
            "    pos = (r, c)\n"
            "    if pos in visited:\n"
            "        return 0\n"
            "    visited.add(pos)\n\n"
            "    size = 1\n"
            "    size += explore_size(grid, r - 1, c, visited)\n"
            "    size += explore_size(grid, r + 1, c, visited)\n"
            "    size += explore_size(grid, r, c - 1, visited)\n"
            "    size += explore_size(grid, r, c + 1, visited)\n"
            "    return size\n\n\n"
            "# === Breadth-First Search ===\n"
            "from collections import deque\n\n"
            "def minimum_island_bfs(grid):\n"
            "    visited = set()\n"
            "    min_size = float('inf')\n"
            "    for r in range(len(grid)):\n"
            "        for c in range(len(grid[0])):\n"
            "            size = explore_size_bfs(grid, r, c, visited)\n"
            "            if 0 < size < min_size:\n"
            "                min_size = size\n"
            "    return min_size\n\n"
            "def explore_size_bfs(grid, r, c, visited):\n"
            "    pos = (r, c)\n"
            "    if pos in visited or grid[r][c] == 'W':\n"
            "        return 0\n"
            "    visited.add(pos)\n\n"
            "    deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]\n"
            "    queue = deque([pos])\n"
            "    size = 0\n"
            "    while queue:\n"
            "        currentR, currentC = queue.popleft()\n"
            "        size += 1\n"
            "        for delta in deltas:\n"
            "            dRow, dCol = delta\n"
            "            neighborR = dRow + currentR\n"
            "            neighborC = dCol + currentC\n"
            "            neighborPos = (neighborR, neighborC)\n"
            "            row_inbounds = 0 <= neighborR < len(grid)\n"
            "            col_inbounds = 0 <= neighborC < len(grid[0])\n"
            "            if neighborPos not in visited and row_inbounds and col_inbounds and grid[neighborR][neighborC] == 'L':\n"
            "                queue.append(neighborPos)\n"
            "                visited.add(neighborPos)\n"
            "    return size\n\n\n"
            "# === Example Test Cases ===\n"
            "grid = [\n"
            "    ['W', 'L', 'W', 'W', 'W'],\n"
            "    ['W', 'L', 'W', 'W', 'W'],\n"
            "    ['W', 'W', 'W', 'L', 'W'],\n"
            "    ['W', 'W', 'L', 'L', 'W'],\n"
            "    ['L', 'W', 'W', 'L', 'L'],\n"
            "    ['L', 'L', 'W', 'W', 'W'],\n"
            "]\n\n"
            "print(minimum_island(grid))     # -> 2\n"
            "print(minimum_island_bfs(grid)) # -> 2\n"
        ),
        "time_complexity": "O(r * c)",
        "space_complexity": "O(r * c)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Traverses every position in the r x c grid once, computing the sizes of all disconnected islands in O(r * c) time and O(r * c) space."
        ),
    },
    {
        "id": "closest_carrot",
        "title": "53. closest carrot",
        "raw_title": "closest carrot",
        "category": "Graph",
        "description": (
            "Write a function, closest_carrot, that takes in a grid, a starting row, and a starting column. "
            "In the grid, 'X's are walls, 'O's are open spaces, and 'C's are carrots. The function should "
            "return a number representing the length of the shortest path from the starting position to a carrot. "
            "You may move up, down, left, or right, but cannot pass through walls (X). If there is no possible "
            "path to a carrot, then return -1."
        ),
        "examples": (
            "grid = [\n"
            "  ['O', 'O', 'O', 'O', 'O'],\n"
            "  ['O', 'X', 'O', 'O', 'O'],\n"
            "  ['O', 'X', 'X', 'O', 'O'],\n"
            "  ['O', 'X', 'C', 'O', 'O'],\n"
            "  ['O', 'X', 'X', 'O', 'O'],\n"
            "  ['C', 'O', 'O', 'O', 'O'],\n"
            "]\n\n"
            "closest_carrot(grid, 1, 2) # -> 4"
        ),
        "starter_code": (
            "def closest_carrot(grid, starting_row, starting_col):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import deque\n\n"
            "def closest_carrot(grid, starting_row, starting_col):\n"
            "    visited = {(starting_row, starting_col)}\n"
            "    queue = deque([(starting_row, starting_col, 0)])\n"
            "    deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]\n\n"
            "    while queue:\n"
            "        row, col, distance = queue.popleft()\n"
            "        if grid[row][col] == 'C':\n"
            "            return distance\n\n"
            "        for delta in deltas:\n"
            "            delta_row, delta_col = delta\n"
            "            neighbor_row = row + delta_row\n"
            "            neighbor_col = col + delta_col\n"
            "            pos = (neighbor_row, neighbor_col)\n"
            "            row_inbounds = 0 <= neighbor_row < len(grid)\n"
            "            col_inbounds = 0 <= neighbor_col < len(grid[0])\n\n"
            "            if row_inbounds and col_inbounds and pos not in visited and grid[neighbor_row][neighbor_col] != 'X':\n"
            "                visited.add(pos)\n"
            "                queue.append((neighbor_row, neighbor_col, distance + 1))\n\n"
            "    return -1\n\n\n"
            "# === Example Test Cases ===\n"
            "grid = [\n"
            "    ['O', 'O', 'O', 'O', 'O'],\n"
            "    ['O', 'X', 'O', 'O', 'O'],\n"
            "    ['O', 'X', 'X', 'O', 'O'],\n"
            "    ['O', 'X', 'C', 'O', 'O'],\n"
            "    ['O', 'X', 'X', 'O', 'O'],\n"
            "    ['C', 'O', 'O', 'O', 'O'],\n"
            "]\n\n"
            "print(closest_carrot(grid, 1, 2)) # -> 4\n"
            "print(closest_carrot(grid, 0, 0)) # -> 5\n"
        ),
        "time_complexity": "O(r * c)",
        "space_complexity": "O(r * c)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Breadth-First Search (BFS) spreads outward layer-by-layer, guaranteeing discovery of the closest carrot first in O(r * c) time with O(r * c) space."
        ),
    },
    {
        "id": "best_bridge",
        "title": "54. best bridge",
        "raw_title": "best bridge",
        "category": "Graph",
        "description": (
            "Write a function, best_bridge, that takes in a grid as an argument. The grid contains water (W) "
            "and land (L). There are exactly two islands in the grid. An island is a vertically or horizontally "
            "connected region of land. Return the minimum length bridge needed to connect the two islands. "
            "A bridge does not need to form a straight line."
        ),
        "examples": (
            "grid = [\n"
            "  ['W', 'W', 'W', 'L', 'L'],\n"
            "  ['L', 'L', 'W', 'W', 'L'],\n"
            "  ['L', 'L', 'L', 'W', 'L'],\n"
            "  ['W', 'L', 'W', 'W', 'W'],\n"
            "  ['W', 'W', 'W', 'W', 'W'],\n"
            "  ['W', 'W', 'W', 'W', 'W'],\n"
            "]\n\n"
            "best_bridge(grid) # -> 1"
        ),
        "starter_code": (
            "def best_bridge(grid):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import deque\n\n"
            "def best_bridge(grid):\n"
            "    main_island = None\n"
            "    for r in range(len(grid)):\n"
            "        for c in range(len(grid[0])):\n"
            "            potential_island = traverse_island(grid, r, c, set())\n"
            "            if len(potential_island) > 0:\n"
            "                main_island = potential_island\n"
            "                break\n"
            "        if main_island:\n"
            "            break\n\n"
            "    visited = set(main_island)\n"
            "    queue = deque([])\n"
            "    for pos in main_island:\n"
            "        r, c = pos\n"
            "        queue.append((r, c, 0))\n\n"
            "    while queue:\n"
            "        row, col, distance = queue.popleft()\n"
            "        if grid[row][col] == 'L' and (row, col) not in main_island:\n"
            "            return distance - 1\n\n"
            "        deltas = [(1, 0), (-1, 0), (0, 1), (0, -1)]\n"
            "        for delta in deltas:\n"
            "            delta_row, delta_col = delta\n"
            "            neighbor_row = row + delta_row\n"
            "            neighbor_col = col + delta_col\n"
            "            neighbor_pos = (neighbor_row, neighbor_col)\n"
            "            if inbounds(grid, neighbor_row, neighbor_col) and neighbor_pos not in visited:\n"
            "                visited.add(neighbor_pos)\n"
            "                queue.append((neighbor_row, neighbor_col, distance + 1))\n\n"
            "    return -1\n\n"
            "def inbounds(grid, row, col):\n"
            "    row_inbounds = 0 <= row < len(grid)\n"
            "    col_inbounds = 0 <= col < len(grid[0])\n"
            "    return row_inbounds and col_inbounds\n\n"
            "def traverse_island(grid, row, col, visited):\n"
            "    if not inbounds(grid, row, col) or grid[row][col] == 'W':\n"
            "        return visited\n\n"
            "    pos = (row, col)\n"
            "    if pos in visited:\n"
            "        return visited\n\n"
            "    visited.add(pos)\n\n"
            "    traverse_island(grid, row - 1, col, visited)\n"
            "    traverse_island(grid, row + 1, col, visited)\n"
            "    traverse_island(grid, row, col - 1, visited)\n"
            "    traverse_island(grid, row, col + 1, visited)\n"
            "    return visited\n\n\n"
            "# === Example Test Cases ===\n"
            "grid = [\n"
            "    ['W', 'W', 'W', 'L', 'L'],\n"
            "    ['L', 'L', 'W', 'W', 'L'],\n"
            "    ['L', 'L', 'L', 'W', 'L'],\n"
            "    ['W', 'L', 'W', 'W', 'W'],\n"
            "    ['W', 'W', 'W', 'W', 'W'],\n"
            "    ['W', 'W', 'W', 'W', 'W'],\n"
            "]\n\n"
            "print(best_bridge(grid)) # -> 1\n"
        ),
        "time_complexity": "O(r * c)",
        "space_complexity": "O(r * c)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Isolates the first island via DFS, then launches a multi-source BFS from all its perimeter coordinates until touching the second island in O(r * c) time and O(r * c) space."
        ),
    },
    {
        "id": "has_cycle",
        "title": "55. has cycle",
        "raw_title": "has cycle",
        "category": "Graph",
        "description": (
            "Write a function, has_cycle, that takes in an object representing the adjacency list "
            "of a directed graph. The function should return a boolean indicating whether or not the graph contains a cycle."
        ),
        "examples": (
            "has_cycle({\n"
            "  'a': ['b'],\n"
            "  'b': ['c'],\n"
            "  'c': ['a'],\n"
            "}) # -> True\n\n"
            "has_cycle({\n"
            "  'a': ['b', 'c'],\n"
            "  'b': ['c'],\n"
            "  'c': ['d'],\n"
            "  'd': [],\n"
            "}) # -> False"
        ),
        "starter_code": (
            "def has_cycle(graph):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === White-Grey-Black Cycle Detection Algorithm ===\n"
            "def has_cycle(graph):\n"
            "    visited = set()\n"
            "    for start_node in graph:\n"
            "        if cycle_detect(graph, start_node, set(), visited):\n"
            "            return True\n"
            "    return False\n\n"
            "def cycle_detect(graph, node, visiting, visited):\n"
            "    if node in visited:\n"
            "        return False\n\n"
            "    if node in visiting:\n"
            "        return True\n\n"
            "    visiting.add(node)\n"
            "    for neighbor in graph[node]:\n"
            "        if cycle_detect(graph, neighbor, visiting, visited):\n"
            "            return True\n\n"
            "    visiting.remove(node)\n"
            "    visited.add(node)\n"
            "    return False\n\n\n"
            "# === Example Test Cases ===\n"
            "print(has_cycle({\n"
            "    'a': ['b'],\n"
            "    'b': ['c'],\n"
            "    'c': ['a'],\n"
            "})) # -> True\n\n"
            "print(has_cycle({\n"
            "    'a': ['b', 'c'],\n"
            "    'b': ['c'],\n"
            "    'c': ['d'],\n"
            "    'd': [],\n"
            "})) # -> False\n"
        ),
        "time_complexity": "O(n^2)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Uses the White-Grey-Black algorithm: tracks nodes currently in the recursion path with a 'visiting' set to detect cycles, and caches fully verified non-cyclical nodes in a 'visited' set. Runs in O(n^2) worst-case time with O(n) space."
        ),
    },
    {
        "id": "prereqs_possible",
        "title": "56. prereqs possible",
        "raw_title": "prereqs possible",
        "category": "Graph",
        "description": (
            "Write a function, prereqs_possible, that takes in a number of courses (n) and prerequisites as arguments. "
            "Courses have ids ranging from 0 through n - 1. A single prerequisite of (A, B) means that course A must be "
            "taken before course B. The function should return a boolean indicating whether or not it is possible to complete all courses."
        ),
        "examples": (
            "numCourses = 6\n"
            "prereqs = [\n"
            "  (0, 1),\n"
            "  (2, 3),\n"
            "  (0, 2),\n"
            "  (1, 3),\n"
            "  (4, 5),\n"
            "]\n"
            "prereqs_possible(numCourses, prereqs) # -> True\n\n"
            "numCourses = 6\n"
            "prereqs = [\n"
            "  (0, 1),\n"
            "  (2, 3),\n"
            "  (0, 2),\n"
            "  (1, 3),\n"
            "  (4, 5),\n"
            "  (3, 0),\n"
            "]\n"
            "prereqs_possible(numCourses, prereqs) # -> False"
        ),
        "starter_code": (
            "def prereqs_possible(num_courses, prereqs):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === White-Grey-Black Cycle Detection ===\n"
            "def prereqs_possible(num_courses, prereqs):\n"
            "    graph = build_graph(num_courses, prereqs)\n"
            "    visiting = set()\n"
            "    visited = set()\n\n"
            "    for node in range(num_courses):\n"
            "        if has_cycle(graph, node, visiting, visited):\n"
            "            return False\n\n"
            "    return True\n\n"
            "def has_cycle(graph, node, visiting, visited):\n"
            "    if node in visited:\n"
            "        return False\n\n"
            "    if node in visiting:\n"
            "        return True\n\n"
            "    visiting.add(node)\n"
            "    for neighbor in graph[node]:\n"
            "        if has_cycle(graph, neighbor, visiting, visited):\n"
            "            return True\n\n"
            "    visiting.remove(node)\n"
            "    visited.add(node)\n"
            "    return False\n\n"
            "def build_graph(num_courses, prereqs):\n"
            "    graph = {i: [] for i in range(num_courses)}\n"
            "    for a, b in prereqs:\n"
            "        graph[a].append(b)\n"
            "    return graph\n\n\n"
            "# === Example Test Cases ===\n"
            "print(prereqs_possible(6, [\n"
            "    (0, 1),\n"
            "    (2, 3),\n"
            "    (0, 2),\n"
            "    (1, 3),\n"
            "    (4, 5),\n"
            "])) # -> True\n\n"
            "print(prereqs_possible(6, [\n"
            "    (0, 1),\n"
            "    (2, 3),\n"
            "    (0, 2),\n"
            "    (1, 3),\n"
            "    (4, 5),\n"
            "    (3, 0),\n"
            "])) # -> False\n"
        ),
        "time_complexity": "O(n + p)",
        "space_complexity": "O(n + p)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Models prerequisite dependencies as directed edges. Detects topological cycles across n courses and p prerequisites in O(n + p) time and O(n + p) space."
        ),
    },
    {
        "id": "max_subarray_sum_size_k",
        "title": "57. max subarray sum size k",
        "raw_title": "max subarray sum size k",
        "category": "Sliding Window",
        "description": (
            "Write a function, max_subarray_sum_size_k, that takes in a list of numbers and a size k as arguments. "
            "The function should return the maximum sum of subarrays that contain exactly k elements.\n\n"
            "You can assume that k is less than or equal to the length of the input list."
        ),
        "examples": (
            "max_subarray_sum_size_k([3, 6, 9, 2, 1, 8, 7], 3) # -> 18\n"
            "max_subarray_sum_size_k([1, 2, 3, 4, 5, 6], 2)       # -> 11\n"
            "max_subarray_sum_size_k([10, -2, 5, 6, -1], 2)       # -> 11"
        ),
        "starter_code": (
            "def max_subarray_sum_size_k(nums, k):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Optimized Sliding Window ===\n"
            "def max_subarray_sum_size_k(nums, k):\n"
            "    current_sum = sum(nums[0:k])\n"
            "    max_sum = current_sum\n"
            "    for i in range(0, len(nums) - k):\n"
            "        current_sum -= nums[i]\n"
            "        current_sum += nums[i + k]\n"
            "        if current_sum > max_sum:\n"
            "            max_sum = current_sum\n"
            "    return max_sum\n\n\n"
            "# === Brute Force Slicing (O(n*k)) ===\n"
            "def max_subarray_sum_size_k_brute(nums, k):\n"
            "    max_sum = -float('inf')\n"
            "    for i in range(0, len(nums) - k + 1):\n"
            "        current_sum = sum(nums[i: i + k])\n"
            "        if current_sum > max_sum:\n"
            "            max_sum = current_sum\n"
            "    return max_sum\n\n\n"
            "# === Example Test Cases ===\n"
            "print(max_subarray_sum_size_k([3, 6, 9, 2, 1, 8, 7], 3)) # -> 18\n"
            "print(max_subarray_sum_size_k([1, 2, 3, 4, 5, 6], 2))       # -> 11\n"
            "print(max_subarray_sum_size_k([10, -2, 5, 6, -1], 2))       # -> 11\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Maintains a sliding window of size k by subtracting the element that left the window and adding the newly entered element in O(1) time per shift, achieving linear O(n) total time and O(1) space."
        ),
    },
    {
        "id": "max_subarray_product_size_k",
        "title": "58. max subarray product size k",
        "raw_title": "max subarray product size k",
        "category": "Sliding Window",
        "description": (
            "Write a function, max_subarray_product_size_k, that takes in a list of numbers and a size k as arguments. "
            "The function should return the maximum product of subarrays that contain exactly k elements.\n\n"
            "You can assume that k is less than or equal to the length of the input list.\n\n"
            "You can assume that numbers of the list are non-zero."
        ),
        "examples": (
            "max_subarray_product_size_k([2, 5, 3, 1, 8, 4], 2)  # -> 32\n"
            "max_subarray_product_size_k([1, 2, 3, 4, 5], 3)     # -> 60\n"
            "max_subarray_product_size_k([-2, -3, 4, -1, -2], 2) # -> 6"
        ),
        "starter_code": (
            "def max_subarray_product_size_k(nums, k):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "import math\n\n"
            "# === Optimized Sliding Window ===\n"
            "def max_subarray_product_size_k(nums, k):\n"
            "    current_product = math.prod(nums[:k])\n"
            "    max_product = current_product\n"
            "    for i in range(0, len(nums) - k):\n"
            "        current_product = (current_product // nums[i]) * nums[i + k] if current_product % nums[i] == 0 else (current_product / nums[i]) * nums[i + k]\n"
            "        max_product = max(current_product, max_product)\n"
            "    return int(max_product)\n\n\n"
            "# === Slice Approach (O(n*k)) ===\n"
            "def max_subarray_product_size_k_slice(nums, k):\n"
            "    max_product = -float('inf')\n"
            "    for i in range(0, len(nums) - k + 1):\n"
            "        current_product = math.prod(nums[i: i + k])\n"
            "        if current_product > max_product:\n"
            "            max_product = current_product\n"
            "    return int(max_product)\n\n\n"
            "# === Example Test Cases ===\n"
            "print(max_subarray_product_size_k([2, 5, 3, 1, 8, 4], 2))  # -> 32\n"
            "print(max_subarray_product_size_k([1, 2, 3, 4, 5], 3))     # -> 60\n"
            "print(max_subarray_product_size_k([-2, -3, 4, -1, -2], 2)) # -> 6\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Computes the initial product of the first k elements, then updates the sliding window in O(1) time per element by dividing the outgoing term and multiplying the incoming term. Runs in O(n) time and O(1) space."
        ),
    },
    {
        "id": "subarray_target_sum_size_k",
        "title": "59. subarray target sum size k",
        "raw_title": "subarray target sum size k",
        "category": "Sliding Window",
        "description": (
            "Write a function, subarray_target_sum_size_k, that takes in a list of numbers, a target sum, and a size k as arguments. "
            "The function should return the number of subarrays of size k that sum to the target.\n\n"
            "You can assume that k is less than or equal to the length of the input list."
        ),
        "examples": (
            "subarray_target_sum_size_k([2, 5, 3, 1, 8, 4], 9, 2)  # -> 1\n"
            "subarray_target_sum_size_k([3, 1, 2, 2, 1, 3], 4, 2)  # -> 3\n"
            "subarray_target_sum_size_k([1, 2, 3, 4, 2, 1], 6, 3)  # -> 1"
        ),
        "starter_code": (
            "def subarray_target_sum_size_k(nums, target, k):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Sliding Window (O(n)) ===\n"
            "def subarray_target_sum_size_k(nums, target, k):\n"
            "    current_sum = sum(nums[0:k])\n"
            "    count = 1 if current_sum == target else 0\n"
            "    for i in range(0, len(nums) - k):\n"
            "        current_sum -= nums[i]\n"
            "        current_sum += nums[i + k]\n"
            "        if current_sum == target:\n"
            "            count += 1\n"
            "    return count\n\n\n"
            "# === Example Test Cases ===\n"
            "print(subarray_target_sum_size_k([2, 5, 3, 1, 8, 4], 9, 2))  # -> 1\n"
            "print(subarray_target_sum_size_k([3, 1, 2, 2, 1, 3], 4, 2))  # -> 3\n"
            "print(subarray_target_sum_size_k([1, 2, 3, 4, 2, 1], 6, 3))  # -> 1\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Computes the initial sum of the first k elements, then slides the window across the array in O(1) time per element. Runs in O(n) time and O(1) space."
        ),
    },
    {
        "id": "has_substring_anagram",
        "title": "60. has substring anagram",
        "raw_title": "has substring anagram",
        "category": "Sliding Window",
        "description": (
            "Write a function, has_substring_anagram, that takes in a string and an anagram. "
            "The function should return a boolean indicating whether or not the string contains a substring with the same characters as the anagram.\n\n"
            "You can assume that the string contains no duplicate characters.\n\n"
            "You can assume that the anagram contains no duplicate characters.\n\n"
            "You can assume that the anagram is not longer than the string."
        ),
        "examples": (
            "has_substring_anagram('cats', 'tac')    # -> True\n"
            "has_substring_anagram('abcdef', 'cba')  # -> True\n"
            "has_substring_anagram('monday', 'dno')  # -> True\n"
            "has_substring_anagram('friday', 'ard')  # -> False"
        ),
        "starter_code": (
            "def has_substring_anagram(s, anagram):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Sliding Window with Set (O(n)) ===\n"
            "def has_substring_anagram(s, anagram):\n"
            "    anagram_set = set(anagram)\n"
            "    window_set = set(s[0:len(anagram)])\n"
            "    if anagram_set == window_set:\n"
            "        return True\n\n"
            "    for i in range(0, len(s) - len(anagram)):\n"
            "        window_set.remove(s[i])\n"
            "        window_set.add(s[i + len(anagram)])\n"
            "        if anagram_set == window_set:\n"
            "            return True\n\n"
            "    return False\n\n\n"
            "# === Example Test Cases ===\n"
            "print(has_substring_anagram('cats', 'tac'))    # -> True\n"
            "print(has_substring_anagram('abcdef', 'cba'))  # -> True\n"
            "print(has_substring_anagram('monday', 'dno'))  # -> True\n"
            "print(has_substring_anagram('friday', 'ard'))  # -> False\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(k)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Maintains a sliding set of characters of window size k. Adding, removing, and set comparison take O(k) (or O(1) for small alphabet sizes), running in O(n) time and O(k) space where k is the length of the anagram."
        ),
    },
    {
        "id": "count_substring_anagrams",
        "title": "61. count substring anagrams",
        "raw_title": "count substring anagrams",
        "category": "Sliding Window",
        "description": (
            "Write a function, count_substring_anagrams, that takes in a string and an anagram. "
            "The function should return the number of substrings that appear in the string that have the same characters as the anagram.\n\n"
            "You can assume that the anagram is not longer than the string."
        ),
        "examples": (
            "count_substring_anagrams('mississippi', 'm')      # -> 1\n"
            "count_substring_anagrams('cbaebabacd', 'abc')     # -> 2\n"
            "count_substring_anagrams('cloudyweather', 'lo')   # -> 0\n"
            "count_substring_anagrams('banana', 'an')          # -> 2"
        ),
        "starter_code": (
            "def count_substring_anagrams(s, anagram):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import Counter\n\n\n"
            "# === Sliding Window with Counter (O(n)) ===\n"
            "def count_substring_anagrams(s, anagram):\n"
            "    anagram_counter = Counter(anagram)\n"
            "    window_counter = Counter(s[0:len(anagram)])\n"
            "    num_matches = 1 if anagram_counter == window_counter else 0\n"
            "    for i in range(0, len(s) - len(anagram)):\n"
            "        window_counter[s[i]] -= 1\n"
            "        window_counter[s[i + len(anagram)]] += 1\n"
            "        if window_counter == anagram_counter:\n"
            "            num_matches += 1\n"
            "    return num_matches\n\n\n"
            "# === Example Test Cases ===\n"
            "print(count_substring_anagrams('mississippi', 'm'))      # -> 1\n"
            "print(count_substring_anagrams('cbaebabacd', 'abc'))     # -> 2\n"
            "print(count_substring_anagrams('cloudyweather', 'lo'))   # -> 0\n"
            "print(count_substring_anagrams('banana', 'an'))          # -> 2\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(k)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Uses a frequency Counter over a sliding window of length k. Updates outgoing and incoming characters in O(1) time per step, running in O(n) time and O(k) space."
        ),
    },
    {
        "id": "find_subarray_sum",
        "title": "62. find subarray sum",
        "raw_title": "find subarray sum",
        "category": "Sliding Window",
        "description": (
            "Write a function, find_subarray_sum, that takes in a list and a target sum. "
            "The function should return the start and end indices (inclusive) of a subarray that sums to the target.\n\n"
            "You can assume that the elements of the list are nonnegative."
        ),
        "examples": (
            "find_subarray_sum([1, 2, 3, 7, 5], 12)       # -> (1, 3)\n"
            "find_subarray_sum([1, 2, 3, 4, 5, 6], 9)     # -> (1, 3)\n"
            "find_subarray_sum([1, 4, 20, 3, 10, 5], 33)  # -> (2, 4)"
        ),
        "starter_code": (
            "def find_subarray_sum(nums, target_sum):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Dynamic Sliding Window (O(n)) ===\n"
            "def find_subarray_sum(nums, target_sum):\n"
            "    window_sum = 0\n"
            "    start = 0\n"
            "    for end in range(0, len(nums)):\n"
            "        window_sum += nums[end]\n"
            "        while window_sum > target_sum:\n"
            "            window_sum -= nums[start]\n"
            "            start += 1\n"
            "        if window_sum == target_sum:\n"
            "            return (start, end)\n"
            "    return None\n\n\n"
            "# === Example Test Cases ===\n"
            "print(find_subarray_sum([1, 2, 3, 7, 5], 12))       # -> (1, 3)\n"
            "print(find_subarray_sum([1, 2, 3, 4, 5, 6], 9))     # -> (1, 3)\n"
            "print(find_subarray_sum([1, 4, 20, 3, 10, 5], 33))  # -> (2, 4)\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Expands the end pointer and contracts the start pointer when window sum exceeds target. Since both pointers visit each element at most once, it runs in O(n) time and O(1) auxiliary space."
        ),
    },
    {
        "id": "longest_subarray_sum",
        "title": "63. longest subarray sum",
        "raw_title": "longest subarray sum",
        "category": "Sliding Window",
        "description": (
            "Write a function, longest_subarray_sum, that takes in an list and a target sum. "
            "The function should return the length of the longest subarray that sums to the target.\n\n"
            "You can assume that the elements of the list are nonnegative.\n\n"
            "If there is no subarray that sums to the target, then return -1."
        ),
        "examples": (
            "longest_subarray_sum([1, 2, 3, 4, 1, 1, 1], 7)  # -> 4\n"
            "longest_subarray_sum([1, 2, 3, 7, 5], 12)       # -> 3\n"
            "longest_subarray_sum([1, 2, 3], 10)              # -> -1"
        ),
        "starter_code": (
            "def longest_subarray_sum(nums, target_sum):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Dynamic Sliding Window (O(n)) ===\n"
            "def longest_subarray_sum(nums, target_sum):\n"
            "    start = 0\n"
            "    window_sum = 0\n"
            "    longest = -1\n"
            "    for end in range(0, len(nums)):\n"
            "        window_sum += nums[end]\n"
            "        while window_sum > target_sum:\n"
            "            window_sum -= nums[start]\n"
            "            start += 1\n"
            "        if window_sum == target_sum:\n"
            "            longest = max(end - start + 1, longest)\n"
            "    return longest\n\n\n"
            "# === Example Test Cases ===\n"
            "print(longest_subarray_sum([1, 2, 3, 4, 1, 1, 1], 7))  # -> 4\n"
            "print(longest_subarray_sum([1, 2, 3, 7, 5], 12))       # -> 3\n"
            "print(longest_subarray_sum([1, 2, 3], 10))             # -> -1\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Maintains a sliding window with two pointers expanding and contracting as needed. Each pointer moves forward at most n times, giving O(n) time and O(1) space."
        ),
    },
    {
        "id": "longest_unique_substring",
        "title": "64. longest unique substring",
        "raw_title": "longest unique substring",
        "category": "Sliding Window",
        "description": (
            "Write a function, longest_unique_substring, that takes in a string as an argument. "
            "The function should return the length of the longest substring that consists of only unique characters."
        ),
        "examples": (
            "longest_unique_substring('abcabcbb')  # -> 3\n"
            "longest_unique_substring('bbbbb')     # -> 1\n"
            "longest_unique_substring('pwwkew')    # -> 3\n"
            "longest_unique_substring('')          # -> 0"
        ),
        "starter_code": (
            "def longest_unique_substring(s):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import Counter\n\n\n"
            "# === Sliding Window with Counter (O(n)) ===\n"
            "def longest_unique_substring(s):\n"
            "    start = 0\n"
            "    longest = 0\n"
            "    window_counter = Counter()\n"
            "    for end in range(0, len(s)):\n"
            "        leading_char = s[end]\n"
            "        window_counter[leading_char] += 1\n"
            "        while window_counter[leading_char] > 1:\n"
            "            trailing_char = s[start]\n"
            "            window_counter[trailing_char] -= 1\n"
            "            start += 1\n"
            "        longest = max(end - start + 1, longest)\n"
            "    return longest\n\n\n"
            "# === Example Test Cases ===\n"
            "print(longest_unique_substring('abcabcbb'))  # -> 3\n"
            "print(longest_unique_substring('bbbbb'))     # -> 1\n"
            "print(longest_unique_substring('pwwkew'))    # -> 3\n"
            "print(longest_unique_substring(''))          # -> 0\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(k)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Slides a window maintaining character counts. Shrinks left bound whenever a duplicate character is encountered. Each character is visited at most twice, resulting in O(n) time and O(k) space where k is the unique character set size."
        ),
    },
    {
        "id": "longest_two_char_substring",
        "title": "65. longest two char substring",
        "raw_title": "longest two char substring",
        "category": "Sliding Window",
        "description": (
            "Write a function, longest_two_char_substring, that takes in a string as an argument. "
            "The function should return the length of the longest substring that consists of 2 distinct characters."
        ),
        "examples": (
            "longest_two_char_substring('eceba')    # -> 3\n"
            "longest_two_char_substring('ccaabbb')  # -> 5\n"
            "longest_two_char_substring('a')        # -> 0\n"
            "longest_two_char_substring('abcabc')   # -> 2"
        ),
        "starter_code": (
            "def longest_two_char_substring(s):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import Counter\n\n\n"
            "# === Sliding Window with At Most 2 Distinct Characters (O(n)) ===\n"
            "def longest_two_char_substring(s):\n"
            "    start = 0\n"
            "    window_counter = Counter()\n"
            "    longest = 0\n"
            "    for end, leading_char in enumerate(s):\n"
            "        window_counter[leading_char] += 1\n"
            "        while len(window_counter) > 2:\n"
            "            trailing_char = s[start]\n"
            "            window_counter[trailing_char] -= 1\n"
            "            start += 1\n"
            "            if window_counter[trailing_char] == 0:\n"
            "                del window_counter[trailing_char]\n"
            "        if len(window_counter) == 2:\n"
            "            longest = max(end - start + 1, longest)\n"
            "    return longest\n\n\n"
            "# === Example Test Cases ===\n"
            "print(longest_two_char_substring('eceba'))    # -> 3\n"
            "print(longest_two_char_substring('ccaabbb'))  # -> 5\n"
            "print(longest_two_char_substring('a'))        # -> 0\n"
            "print(longest_two_char_substring('abcabc'))   # -> 2\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Slides a window tracking character frequencies while maintaining at most 2 distinct characters in the counter. Since the counter size is at most 3 keys, hash operations take O(1), yielding O(n) time and O(1) space."
        ),
    },
    {
        "id": "max_ones_with_single_flip",
        "title": "66. max ones with single flip",
        "raw_title": "max ones with single flip",
        "category": "Sliding Window",
        "description": (
            "Write a function, max_ones_with_single_flip, that takes in a string containing only '0's and '1's. "
            "The function should return the length of the longest consecutive streak of '1's possible if you are allowed to change at most one '0' into a '1'."
        ),
        "examples": (
            "max_ones_with_single_flip('10110')     # -> 4\n"
            "max_ones_with_single_flip('10111011')  # -> 6\n"
            "max_ones_with_single_flip('000')       # -> 1\n"
            "max_ones_with_single_flip('1111')      # -> 4"
        ),
        "starter_code": (
            "def max_ones_with_single_flip(s):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Sliding Window with Zero Budget (O(n)) ===\n"
            "def max_ones_with_single_flip(s):\n"
            "    start = 0\n"
            "    longest = 0\n"
            "    num_zeros = 0\n"
            "    for end in range(0, len(s)):\n"
            "        if s[end] == '0':\n"
            "            num_zeros += 1\n"
            "        while num_zeros > 1:\n"
            "            if s[start] == '0':\n"
            "                num_zeros -= 1\n"
            "            start += 1\n"
            "        longest = max(end - start + 1, longest)\n"
            "    return longest\n\n\n"
            "# === Example Test Cases ===\n"
            "print(max_ones_with_single_flip('10110'))     # -> 4\n"
            "print(max_ones_with_single_flip('10111011'))  # -> 6\n"
            "print(max_ones_with_single_flip('000'))       # -> 1\n"
            "print(max_ones_with_single_flip('1111'))      # -> 4\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Maintains a sliding window with at most one zero. When count of zeros exceeds one, increments start until the extra zero is discarded. Runs in O(n) time and O(1) space."
        ),
    },
    {
        "id": "count_subarray_product",
        "title": "67. count subarray product",
        "raw_title": "count subarray product",
        "category": "Sliding Window",
        "description": (
            "Write a function, count_subarray_product, that takes in an array of positive integers and a target product. "
            "The function should return the number of subarrays that have a total product strictly less than the target."
        ),
        "examples": (
            "count_subarray_product([10, 5, 2, 6], 100)  # -> 8\n"
            "count_subarray_product([1, 2, 3], 0)        # -> 0\n"
            "count_subarray_product([1, 1, 1], 2)        # -> 6"
        ),
        "starter_code": (
            "def count_subarray_product(nums, target_product):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Sliding Window (O(n)) ===\n"
            "def count_subarray_product(nums, target_product):\n"
            "    start = 0\n"
            "    count = 0\n"
            "    window_product = 1\n"
            "    for end in range(0, len(nums)):\n"
            "        window_product *= nums[end]\n"
            "        while window_product >= target_product and start <= end:\n"
            "            window_product /= nums[start]\n"
            "            start += 1\n"
            "        count += end - start + 1\n"
            "    return count\n\n\n"
            "# === Example Test Cases ===\n"
            "print(count_subarray_product([10, 5, 2, 6], 100))  # -> 8\n"
            "print(count_subarray_product([1, 2, 3], 0))        # -> 0\n"
            "print(count_subarray_product([1, 1, 1], 2))        # -> 6\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "For each end index, shrinks start until window_product < target_product. The number of valid subarrays ending at end is (end - start + 1). Both pointers move at most n times, giving O(n) time and O(1) space."
        ),
    },
    {
        "id": "count_substring_at_most_k_distinct",
        "title": "68. count substring at most k distinct",
        "raw_title": "count substring at most k distinct",
        "category": "Sliding Window",
        "description": (
            "Write a function, count_substring_at_most_k_distinct, that takes in a string and a number k. "
            "The function should return the number of substrings that consist of at most k distinct characters."
        ),
        "examples": (
            "count_substring_at_most_k_distinct('aba', 2)    # -> 6\n"
            "count_substring_at_most_k_distinct('aba', 1)    # -> 3\n"
            "count_substring_at_most_k_distinct('pqpqs', 2)  # -> 12"
        ),
        "starter_code": (
            "def count_substring_at_most_k_distinct(s, k):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import Counter\n\n\n"
            "# === Sliding Window with Counter (O(n)) ===\n"
            "def count_substring_at_most_k_distinct(s, k):\n"
            "    start = 0\n"
            "    window_counter = Counter()\n"
            "    num_substrings = 0\n"
            "    for end, leading_char in enumerate(s):\n"
            "        window_counter[leading_char] += 1\n"
            "        while len(window_counter) > k:\n"
            "            trailing_char = s[start]\n"
            "            window_counter[trailing_char] -= 1\n"
            "            start += 1\n"
            "            if window_counter[trailing_char] == 0:\n"
            "                del window_counter[trailing_char]\n"
            "        num_substrings += end - start + 1\n"
            "    return num_substrings\n\n\n"
            "# === Example Test Cases ===\n"
            "print(count_substring_at_most_k_distinct('aba', 2))    # -> 6\n"
            "print(count_substring_at_most_k_distinct('aba', 1))    # -> 3\n"
            "print(count_substring_at_most_k_distinct('pqpqs', 2))  # -> 12\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(k)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Maintains a sliding window with at most k distinct characters. At each step, (end - start + 1) valid substrings end at index end. Runs in O(n) time and O(k) space."
        ),
    },
    {
        "id": "count_substring_exactly_k_distinct",
        "title": "69. count substring exactly k distinct",
        "raw_title": "count substring exactly k distinct",
        "category": "Sliding Window",
        "description": (
            "Write a function, count_substring_exactly_k_distinct, that takes in a string and a number k. "
            "The function should return the number of substrings that consist of exactly k distinct characters."
        ),
        "examples": (
            "count_substring_exactly_k_distinct('aba', 2)    # -> 3\n"
            "count_substring_exactly_k_distinct('aba', 1)    # -> 3\n"
            "count_substring_exactly_k_distinct('pqpqs', 2)  # -> 7"
        ),
        "starter_code": (
            "def count_substring_exactly_k_distinct(s, k):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import Counter\n\n\n"
            "# === Exact K using (At Most K - At Most K-1) (O(n)) ===\n"
            "def at_most_k_distinct(s, k):\n"
            "    if k < 0:\n"
            "        return 0\n"
            "    start = 0\n"
            "    window_counter = Counter()\n"
            "    num_substrings = 0\n"
            "    for end, leading_char in enumerate(s):\n"
            "        window_counter[leading_char] += 1\n"
            "        while len(window_counter) > k:\n"
            "            trailing_char = s[start]\n"
            "            window_counter[trailing_char] -= 1\n"
            "            start += 1\n"
            "            if window_counter[trailing_char] == 0:\n"
            "                del window_counter[trailing_char]\n"
            "        num_substrings += end - start + 1\n"
            "    return num_substrings\n\n\n"
            "def count_substring_exactly_k_distinct(s, k):\n"
            "    return at_most_k_distinct(s, k) - at_most_k_distinct(s, k - 1)\n\n\n"
            "# === Example Test Cases ===\n"
            "print(count_substring_exactly_k_distinct('aba', 2))    # -> 3\n"
            "print(count_substring_exactly_k_distinct('aba', 1))    # -> 3\n"
            "print(count_substring_exactly_k_distinct('pqpqs', 2))  # -> 7\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(k)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Computes exact k as (at_most_k - at_most_(k-1)). Each helper call processes the string in O(n) time with a sliding window counter, resulting in O(n) total time and O(k) space."
        ),
    },
    {
        "id": "is_palindrome",
        "title": "70. is palindrome",
        "raw_title": "is palindrome",
        "category": "Two Pointer",
        "description": (
            "Write a function, is_palindrome, that takes in a string and returns a boolean indicating whether or not the string is the same forwards and backwards."
        ),
        "examples": (
            "is_palindrome('pop')       # -> True\n"
            "is_palindrome('kayak')     # -> True\n"
            "is_palindrome('racecar')   # -> True\n"
            "is_palindrome('rotator')   # -> True\n"
            "is_palindrome('hello')     # -> False"
        ),
        "starter_code": (
            "def is_palindrome(s):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Two Pointer (O(n)) ===\n"
            "def is_palindrome(s):\n"
            "    i = 0\n"
            "    j = len(s) - 1\n"
            "    while i < j:\n"
            "        if s[i] != s[j]:\n"
            "            return False\n"
            "        i += 1\n"
            "        j -= 1\n"
            "    return True\n\n\n"
            "# === Example Test Cases ===\n"
            "print(is_palindrome('pop'))      # -> True\n"
            "print(is_palindrome('kayak'))    # -> True\n"
            "print(is_palindrome('racecar'))  # -> True\n"
            "print(is_palindrome('rotator'))  # -> True\n"
            "print(is_palindrome('hello'))    # -> False\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Uses two pointers starting at opposite ends of the string and moving inward. Compares characters until they meet in the middle, running in O(n) time and O(1) space."
        ),
    },
    {
        "id": "uncompress",
        "title": "71. uncompress",
        "raw_title": "uncompress",
        "category": "Two Pointer",
        "description": (
            "Write a function, uncompress, that takes in a string as an argument. The input string will be formatted into multiple groups according to the following pattern:\n\n"
            "<number><char>\n"
            "for example, '2c' or '3a'.\n\n"
            "The function should return an uncompressed version of the string where each 'char' of a group is repeated 'number' times consecutively. "
            "You may assume that the input string is well-formed according to the pattern of groups."
        ),
        "examples": (
            "uncompress('2c3a1t')   # -> 'ccaaat'\n"
            "uncompress('4s2b')     # -> 'ssssbb'\n"
            "uncompress('2p1o5p')   # -> 'ppoppppp'\n"
            "uncompress('3n12e2z')  # -> 'nnneeeeeeeeeeeezz'"
        ),
        "starter_code": (
            "def uncompress(s):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Two Pointer String Expansion (O(n*m)) ===\n"
            "def uncompress(s):\n"
            "    numbers = '0123456789'\n"
            "    result = []\n"
            "    i = 0\n"
            "    j = 0\n"
            "    while j < len(s):\n"
            "        if s[j] in numbers:\n"
            "            j += 1\n"
            "        else:\n"
            "            num = int(s[i:j])\n"
            "            result.append(s[j] * num)\n"
            "            j += 1\n"
            "            i = j\n"
            "    return ''.join(result)\n\n\n"
            "# === Example Test Cases ===\n"
            "print(uncompress('2c3a1t'))   # -> 'ccaaat'\n"
            "print(uncompress('4s2b'))     # -> 'ssssbb'\n"
            "print(uncompress('2p1o5p'))   # -> 'ppoppppp'\n"
            "print(uncompress('3n12e2z'))  # -> 'nnneeeeeeeeeeeezz'\n"
        ),
        "time_complexity": "O(n * m)",
        "space_complexity": "O(n * m)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Uses two pointers i and j to slice multi-digit numbers before each character. Builds the output string by repeating each character, running in O(n*m) time and O(n*m) space where n is the number of groups and m is the maximum repeat count."
        ),
    },
    {
        "id": "compress",
        "title": "72. compress",
        "raw_title": "compress",
        "category": "Two Pointer",
        "description": (
            "Write a function, compress, that takes in a string as an argument. The function should return a compressed "
            "version of the string where consecutive occurrences of the same characters are compressed into the number of "
            "occurrences followed by the character. Single character occurrences should not be changed.\n\n"
            "'aaa' compresses to '3a'\n"
            "'cc' compresses to '2c'\n"
            "'t' should remain as 't'\n\n"
            "You can assume that the input only contains alphabetic characters."
        ),
        "examples": (
            "compress('ccaaatsss')          # -> '2c3at3s'\n"
            "compress('ssssbbz')            # -> '4s2bz'\n"
            "compress('ppoppppp')           # -> '2po5p'\n"
            "compress('nnneeeeeeeeeeeezz')  # -> '3n12e2z'"
        ),
        "starter_code": (
            "def compress(s):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Two Pointer (O(n)) ===\n"
            "def compress(s):\n"
            "    s += '!'\n"
            "    result = []\n"
            "    i = 0\n"
            "    j = 0\n"
            "    while j < len(s):\n"
            "        if s[i] == s[j]:\n"
            "            j += 1\n"
            "        else:\n"
            "            num = j - i\n"
            "            if num == 1:\n"
            "                result.append(s[i])\n"
            "            else:\n"
            "                result.append(str(num))\n"
            "                result.append(s[i])\n"
            "            i = j\n"
            "    return ''.join(result)\n\n\n"
            "# === Example Test Cases ===\n"
            "print(compress('ccaaatsss'))          # -> '2c3at3s'\n"
            "print(compress('ssssbbz'))            # -> '4s2bz'\n"
            "print(compress('ppoppppp'))           # -> '2po5p'\n"
            "print(compress('nnneeeeeeeeeeeezz'))  # -> '3n12e2z'\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Uses two pointers i and j to track run lengths of repeating characters in a single pass. Appends each group in linear time, running in O(n) time and O(n) space."
        ),
    },
    {
        "id": "five_sort",
        "title": "73. five sort",
        "raw_title": "five sort",
        "category": "Two Pointer",
        "description": (
            "Write a function, five_sort, that takes in a list of numbers as an argument. The function should rearrange "
            "elements of the list such that all 5s appear at the end. Your function should perform this operation in-place "
            "by mutating the original list. The function should return the list.\n\n"
            "Elements that are not 5 can appear in any order in the output, as long as all 5s are at the end of the list.\n\n"
            "Important: Your function needs to mutate the original list in-place and should not return a new list. "
            "It will fail the test cases if you do not modify the original input list."
        ),
        "examples": (
            "five_sort([12, 5, 1, 5, 12, 7])            # -> [12, 7, 1, 12, 5, 5]\n"
            "five_sort([5, 2, 5, 6, 5, 1, 10, 2, 5, 5]) # -> [2, 2, 10, 6, 1, 5, 5, 5, 5, 5]\n"
            "five_sort([5, 5, 5, 1, 1, 1, 4])           # -> [4, 1, 1, 1, 5, 5, 5]"
        ),
        "starter_code": (
            "def five_sort(nums):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === In-Place Two Pointer (O(n)) ===\n"
            "def five_sort(nums):\n"
            "    i = 0\n"
            "    j = len(nums) - 1\n"
            "    while i < j:\n"
            "        if nums[j] == 5:\n"
            "            j -= 1\n"
            "        elif nums[i] == 5:\n"
            "            nums[i], nums[j] = nums[j], nums[i]\n"
            "            i += 1\n"
            "        else:\n"
            "            i += 1\n"
            "    return nums\n\n\n"
            "# === Example Test Cases ===\n"
            "print(five_sort([12, 5, 1, 5, 12, 7]))                     # -> [12, 7, 1, 12, 5, 5]\n"
            "print(five_sort([5, 2, 5, 6, 5, 1, 10, 2, 5, 5]))          # -> [2, 2, 10, 6, 1, 5, 5, 5, 5, 5]\n"
            "print(five_sort([5, 5, 5, 1, 1, 1, 4]))                    # -> [4, 1, 1, 1, 5, 5, 5]\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Two pointers move toward each other from opposite ends of the array, swapping 5s from the left with non-5s on the right. Mutates in-place in O(n) time and O(1) space."
        ),
    },
    {
        "id": "is_subsequence",
        "title": "74. is subsequence",
        "raw_title": "is subsequence",
        "category": "Two Pointer",
        "description": (
            "Write a function, is_subsequence, that takes in string_1 and string_2. The function should return a boolean "
            "indicating whether or not string_1 is a subsequence of string_2.\n\n"
            "A subsequence is a string that can be formed by deleting 0 or more characters from another string."
        ),
        "examples": (
            "is_subsequence('hello', 'helleo world')  # -> True\n"
            "is_subsequence('app', 'apple')          # -> True\n"
            "is_subsequence('bba', 'abracadabra')     # -> True\n"
            "is_subsequence('xyz', 'abracadabra')     # -> False"
        ),
        "starter_code": (
            "def is_subsequence(string_1, string_2):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Two Pointer Matching (O(n)) ===\n"
            "def is_subsequence(string_1, string_2):\n"
            "    i = 0\n"
            "    j = 0\n"
            "    while i < len(string_1) and j < len(string_2):\n"
            "        if string_1[i] == string_2[j]:\n"
            "            i += 1\n"
            "            j += 1\n"
            "        else:\n"
            "            j += 1\n"
            "    return i == len(string_1)\n\n\n"
            "# === Example Test Cases ===\n"
            "print(is_subsequence('hello', 'helleo world'))  # -> True\n"
            "print(is_subsequence('app', 'apple'))          # -> True\n"
            "print(is_subsequence('bba', 'abracadabra'))     # -> True\n"
            "print(is_subsequence('xyz', 'abracadabra'))     # -> False\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Advances pointer i whenever string_1[i] matches string_2[j], while pointer j scans linearly through string_2. Runs in O(n) time where n is the length of string_2, and O(1) space."
        ),
    },
    {
        "id": "binary_search",
        "title": "75. binary search",
        "raw_title": "binary search",
        "category": "Binary Search",
        "description": (
            "Write a function, binary_search, that takes in a sorted list of numbers and a target. The function should return the "
            "index where the target can be found within the list. If the target is not found in the list, then return -1.\n\n"
            "You may assume that the input array contains unique numbers sorted in increasing order.\n\n"
            "Your function must implement the binary search algorithm."
        ),
        "examples": (
            "binary_search([0, 1, 2, 3, 4, 5, 6, 7, 8], 6)             # -> 6\n"
            "binary_search([0, 6, 8, 12, 16, 19, 20, 24, 28], 27)      # -> -1\n"
            "binary_search([0, 6, 8, 12, 16, 19, 20, 28], 8)          # -> 2\n"
            "binary_search([], 7)                                      # -> -1"
        ),
        "starter_code": (
            "def binary_search(numbers, target):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Binary Search (O(log n)) ===\n"
            "def binary_search(numbers, target):\n"
            "    lo = 0\n"
            "    hi = len(numbers) - 1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if target < numbers[mid]:\n"
            "            hi = mid - 1\n"
            "        elif target > numbers[mid]:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            return mid\n"
            "    return -1\n\n\n"
            "# === Example Test Cases ===\n"
            "print(binary_search([0, 1, 2, 3, 4, 5, 6, 7, 8], 6))             # -> 6\n"
            "print(binary_search([0, 6, 8, 12, 16, 19, 20, 24, 28], 27))      # -> -1\n"
            "print(binary_search([0, 6, 8, 12, 16, 19, 20, 28], 8))          # -> 2\n"
            "print(binary_search([], 7))                                      # -> -1\n"
        ),
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(log n)",
        "complexity_explanation": (
            "Halves the search space on each iteration by comparing the target with the middle element. Runs in O(log n) time and O(1) space."
        ),
    },
    {
        "id": "binary_search_index",
        "title": "76. binary search index",
        "raw_title": "binary search index",
        "category": "Binary Search",
        "description": (
            "Write a function that takes in a sorted list of numbers and a target. The function should return the index where the "
            "target can be found within the list. If the target is not found in the list, then return the index where it should "
            "appear in the sorted order.\n\n"
            "You may assume that the input list contains unique numbers sorted in increasing order.\n\n"
            "Your solution should have a runtime of O(logn)."
        ),
        "examples": (
            "binary_search_index([1, 3, 5, 6], 5)  # -> 2\n"
            "binary_search_index([1, 3, 5, 6], 2)  # -> 1\n"
            "binary_search_index([1, 3, 5, 6], 7)  # -> 4\n"
            "binary_search_index([1, 3, 5, 6], 0)  # -> 0"
        ),
        "starter_code": (
            "def binary_search_index(nums, target):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Binary Search Insertion Index (O(log n)) ===\n"
            "def binary_search_index(nums, target):\n"
            "    lo = 0\n"
            "    hi = len(nums) - 1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if target < nums[mid]:\n"
            "            hi = mid - 1\n"
            "        elif target > nums[mid]:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            return mid\n"
            "    return lo\n\n\n"
            "# === Example Test Cases ===\n"
            "print(binary_search_index([1, 3, 5, 6], 5))  # -> 2\n"
            "print(binary_search_index([1, 3, 5, 6], 2))  # -> 1\n"
            "print(binary_search_index([1, 3, 5, 6], 7))  # -> 4\n"
            "print(binary_search_index([1, 3, 5, 6], 0))  # -> 0\n"
        ),
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(log n)",
        "complexity_explanation": (
            "Performs binary search. If target is found, returns its index. If not found, lo converges to the exact index where target should be inserted to maintain sorted order. Runs in O(log n) time and O(1) space."
        ),
    },
    {
        "id": "square_root",
        "title": "77. square root",
        "raw_title": "square root",
        "category": "Binary Search",
        "description": (
            "Write a function that takes in a nonnegative integer n as input. The function should return the square root of n "
            "rounded down to the nearest integer.\n\n"
            "You may not use built-in methods that trivialize this problem.\n\n"
            "Your solution should have a time complexity of O(log(n))."
        ),
        "examples": (
            "square_root(4)   # -> 2\n"
            "square_root(8)   # -> 2\n"
            "square_root(16)  # -> 4\n"
            "square_root(25)  # -> 5\n"
            "square_root(26)  # -> 5"
        ),
        "starter_code": (
            "def square_root(n):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Binary Search on Answer Space (O(log n)) ===\n"
            "def square_root(n):\n"
            "    lo = 0\n"
            "    hi = n\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if n < mid * mid:\n"
            "            hi = mid - 1\n"
            "        elif n > mid * mid:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            return mid\n"
            "    return hi\n\n\n"
            "# === Example Test Cases ===\n"
            "print(square_root(4))   # -> 2\n"
            "print(square_root(8))   # -> 2\n"
            "print(square_root(16))  # -> 4\n"
            "print(square_root(25))  # -> 5\n"
            "print(square_root(26))  # -> 5\n"
        ),
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(log n)",
        "complexity_explanation": (
            "Searches the candidate root space [0, n] logarithmically by checking mid * mid against n. Runs in O(log n) time and O(1) space."
        ),
    },
    {
        "id": "find_leftmost_index",
        "title": "78. find leftmost index",
        "raw_title": "find leftmost index",
        "category": "Binary Search",
        "description": (
            "Write a function that takes in a sorted list of numbers and a target as arguments. The function should return the "
            "leftmost index where the target can be found in the list. If the target does not exist in the list, then return -1.\n\n"
            "Your solution should have a time complexity of O(logn)."
        ),
        "examples": (
            "find_leftmost_index([1, 2, 2, 2, 3], 2)  # -> 1\n"
            "find_leftmost_index([1, 2, 3, 4, 5], 3)  # -> 2\n"
            "find_leftmost_index([4, 4, 4, 4, 4], 4)  # -> 0\n"
            "find_leftmost_index([1, 2, 3, 4, 5], 9)  # -> -1"
        ),
        "starter_code": (
            "def find_leftmost_index(nums, target):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Binary Search Left Boundary (O(log n)) ===\n"
            "def find_leftmost_index(nums, target):\n"
            "    lo = 0\n"
            "    hi = len(nums) - 1\n"
            "    leftmost = -1\n"
            "    while lo <= hi:\n"
            "        mid = (hi + lo) // 2\n"
            "        if target < nums[mid]:\n"
            "            hi = mid - 1\n"
            "        elif target > nums[mid]:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "            leftmost = mid\n"
            "    return leftmost\n\n\n"
            "# === Example Test Cases ===\n"
            "print(find_leftmost_index([1, 2, 2, 2, 3], 2))  # -> 1\n"
            "print(find_leftmost_index([1, 2, 3, 4, 5], 3))  # -> 2\n"
            "print(find_leftmost_index([4, 4, 4, 4, 4], 4))  # -> 0\n"
            "print(find_leftmost_index([1, 2, 3, 4, 5], 9))  # -> -1\n"
        ),
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(log n)",
        "complexity_explanation": (
            "When target matches nums[mid], records mid and continues searching the left sub-array (hi = mid - 1) to find the leftmost occurrence. Runs in O(log n) time and O(1) space."
        ),
    },
    {
        "id": "count_in_sorted_array",
        "title": "79. count in sorted array",
        "raw_title": "count in sorted array",
        "category": "Binary Search",
        "description": (
            "Write a function that takes in a sorted list of numbers and a target as arguments. The function should return the "
            "number of times the target element appears in the list.\n\n"
            "Your solution should have a time complexity of O(logn)."
        ),
        "examples": (
            "count_in_sorted_array([1, 2, 2, 2, 3], 2)  # -> 3\n"
            "count_in_sorted_array([1, 2, 3, 4, 5], 3)  # -> 1\n"
            "count_in_sorted_array([4, 4, 4, 4, 4], 4)  # -> 5\n"
            "count_in_sorted_array([1, 2, 3, 4, 5], 9)  # -> 0"
        ),
        "starter_code": (
            "def count_in_sorted_array(nums, target):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Binary Search Double Boundary (O(log n)) ===\n"
            "def find_leftmost_index(nums, target):\n"
            "    lo = 0\n"
            "    hi = len(nums) - 1\n"
            "    leftmost = -1\n"
            "    while lo <= hi:\n"
            "        mid = (hi + lo) // 2\n"
            "        if target < nums[mid]:\n"
            "            hi = mid - 1\n"
            "        elif target > nums[mid]:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid - 1\n"
            "            leftmost = mid\n"
            "    return leftmost\n\n\n"
            "def find_rightmost_index(nums, target):\n"
            "    lo = 0\n"
            "    hi = len(nums) - 1\n"
            "    rightmost = -1\n"
            "    while lo <= hi:\n"
            "        mid = (hi + lo) // 2\n"
            "        if target < nums[mid]:\n"
            "            hi = mid - 1\n"
            "        elif target > nums[mid]:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            lo = mid + 1\n"
            "            rightmost = mid\n"
            "    return rightmost\n\n\n"
            "def count_in_sorted_array(nums, target):\n"
            "    right_index = find_rightmost_index(nums, target)\n"
            "    left_index = find_leftmost_index(nums, target)\n"
            "    if right_index == -1:\n"
            "        return 0\n"
            "    else:\n"
            "        return right_index - left_index + 1\n\n\n"
            "# === Example Test Cases ===\n"
            "print(count_in_sorted_array([1, 2, 2, 2, 3], 2))  # -> 3\n"
            "print(count_in_sorted_array([1, 2, 3, 4, 5], 3))  # -> 1\n"
            "print(count_in_sorted_array([4, 4, 4, 4, 4], 4))  # -> 5\n"
            "print(count_in_sorted_array([1, 2, 3, 4, 5], 9))  # -> 0\n"
        ),
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(log n)",
        "complexity_explanation": (
            "Finds the leftmost and rightmost indices of target using two binary searches, then calculates count as (right - left + 1). Runs in O(log n) time and O(1) space."
        ),
    },
    {
        "id": "min_in_rotated_sorted_array",
        "title": "80. min in rotated sorted array",
        "raw_title": "min in rotated sorted array",
        "category": "Binary Search",
        "description": (
            "Write a function that takes in a list of sorted numbers that has been rotated a number of times. The function should "
            "return the minimum element of the list.\n\n"
            "Your solution should have a time complexity of O(logn).\n\n"
            "You can assume that the numbers of the input list are unique."
        ),
        "examples": (
            "min_in_rotated_sorted_array([3, 4, 5, 1, 2])        # -> 1\n"
            "min_in_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2])  # -> 0\n"
            "min_in_rotated_sorted_array([11, 13, 15, 17])       # -> 11\n"
            "min_in_rotated_sorted_array([2, 1])                 # -> 1"
        ),
        "starter_code": (
            "def min_in_rotated_sorted_array(nums):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Binary Search Inflection Point (O(log n)) ===\n"
            "def min_in_rotated_sorted_array(nums):\n"
            "    lo = 0\n"
            "    hi = len(nums) - 1\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if nums[mid] < nums[hi]:\n"
            "            hi = mid\n"
            "        else:\n"
            "            lo = mid + 1\n"
            "    return nums[lo]\n\n\n"
            "# === Example Test Cases ===\n"
            "print(min_in_rotated_sorted_array([3, 4, 5, 1, 2]))        # -> 1\n"
            "print(min_in_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2]))  # -> 0\n"
            "print(min_in_rotated_sorted_array([11, 13, 15, 17]))       # -> 11\n"
            "print(min_in_rotated_sorted_array([2, 1]))                 # -> 1\n"
        ),
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(log n)",
        "complexity_explanation": (
            "Compares nums[mid] against nums[hi]. If nums[mid] < nums[hi], the minimum lies in the left half including mid; otherwise it is in the right half. Runs in O(log n) time and O(1) space."
        ),
    },
    {
        "id": "find_in_rotated_sorted_array",
        "title": "81. find in rotated sorted array",
        "raw_title": "find in rotated sorted array",
        "category": "Binary Search",
        "description": (
            "Write a function that takes in a list of sorted numbers that has been rotated a number of times, as well as a target "
            "element. The function should return the index of the target in the list. If the target is not found in the list, then return -1.\n\n"
            "Your solution should have a time complexity of O(logn).\n\n"
            "You can assume that the input list contains unique elements."
        ),
        "examples": (
            "find_in_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2], 0)  # -> 4\n"
            "find_in_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2], 3)  # -> -1\n"
            "find_in_rotated_sorted_array([6, 7, 1, 2, 3, 4, 5], 4)  # -> 5\n"
            "find_in_rotated_sorted_array([1], 0)                    # -> -1"
        ),
        "starter_code": (
            "def find_in_rotated_sorted_array(nums, target):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Binary Search with Pivot (O(log n)) ===\n"
            "def find_min_index(nums):\n"
            "    lo = 0\n"
            "    hi = len(nums) - 1\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if nums[mid] < nums[hi]:\n"
            "            hi = mid\n"
            "        else:\n"
            "            lo = mid + 1\n"
            "    return lo\n\n\n"
            "def binary_search(nums, target, lo, hi):\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if target < nums[mid]:\n"
            "            hi = mid - 1\n"
            "        elif target > nums[mid]:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            return mid\n"
            "    return -1\n\n\n"
            "def find_in_rotated_sorted_array(nums, target):\n"
            "    min_index = find_min_index(nums)\n"
            "    left_result = binary_search(nums, target, 0, min_index - 1)\n"
            "    right_result = binary_search(nums, target, min_index, len(nums) - 1)\n"
            "    if left_result == -1:\n"
            "        return right_result\n"
            "    else:\n"
            "        return left_result\n\n\n"
            "# === Example Test Cases ===\n"
            "print(find_in_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2], 0))  # -> 4\n"
            "print(find_in_rotated_sorted_array([4, 5, 6, 7, 0, 1, 2], 3))  # -> -1\n"
            "print(find_in_rotated_sorted_array([6, 7, 1, 2, 3, 4, 5], 4))  # -> 5\n"
            "print(find_in_rotated_sorted_array([1], 0))                    # -> -1\n"
        ),
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(log n)",
        "complexity_explanation": (
            "Locates the rotation pivot in O(log n) time, then performs standard binary search on the appropriate sorted half. Runs in O(log n) time and O(1) space."
        ),
    },
    {
        "id": "find_peak",
        "title": "82. find peak",
        "raw_title": "find peak",
        "category": "Binary Search",
        "description": (
            "Write a function that takes in a list of numbers. The function should return the index of a 'peak' element. "
            "A 'peak' is an element that is greater than both of its adjacent neighbors. If there are multiple peaks, "
            "you may return the index of any one of them.\n\n"
            "Note that the first and last elements of the list only need to be greater than their single neighbor to be considered a 'peak'.\n\n"
            "Your solution should have a time complexity of O(logn).\n\n"
            "You can assume that adjacent numbers of the list are not equal."
        ),
        "examples": (
            "find_peak([1, 2, 3, 1])          # -> 2\n"
            "find_peak([1, 2, 1, 3, 5, 6, 4]) # -> 5 (or 1)\n"
            "find_peak([5, 4, 3, 2, 1])       # -> 0\n"
            "find_peak([1, 2, 3, 4, 5])       # -> 4"
        ),
        "starter_code": (
            "def find_peak(nums):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Binary Search Peak Finding (O(log n)) ===\n"
            "def find_peak(nums):\n"
            "    lo = 0\n"
            "    hi = len(nums) - 1\n"
            "    while lo < hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if nums[mid] < nums[mid + 1]:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            hi = mid\n"
            "    return lo\n\n\n"
            "# === Example Test Cases ===\n"
            "print(find_peak([1, 2, 3, 1]))          # -> 2\n"
            "print(find_peak([1, 2, 1, 3, 5, 6, 4])) # -> 5 (or 1)\n"
            "print(find_peak([5, 4, 3, 2, 1]))       # -> 0\n"
            "print(find_peak([1, 2, 3, 4, 5]))       # -> 4\n"
        ),
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(log n)",
        "complexity_explanation": (
            "If nums[mid] < nums[mid + 1], an ascending slope guarantees a peak exists to the right; otherwise a peak exists to the left including mid. Runs in O(log n) time and O(1) space."
        ),
    },
    {
        "id": "search_sorted_grid",
        "title": "83. search sorted grid",
        "raw_title": "search sorted grid",
        "category": "Binary Search",
        "description": (
            "Write a function that takes in a grid of numbers and a target element as input. The function should return a boolean "
            "indicating whether or not the target is present in the grid. Each row of the grid is sorted in increasing order. "
            "The first element of each row is greater than the last element of the previous row.\n\n"
            "Your solution should have a time complexity of O(log(m*n)), where m is the number of rows and n is the number of columns in the grid."
        ),
        "examples": (
            "grid = [[1, 3, 5, 7], [10, 11, 16, 20], [23, 30, 34, 60]]\n"
            "search_sorted_grid(grid, 3)    # -> True\n"
            "search_sorted_grid(grid, 13)   # -> False\n"
            "search_sorted_grid(grid, 20)   # -> True\n"
            "search_sorted_grid(grid, 100)  # -> False"
        ),
        "starter_code": (
            "def search_sorted_grid(grid, target):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === 2D Binary Search (O(log(m*n))) ===\n"
            "def find_row(grid, target):\n"
            "    lo = 0\n"
            "    hi = len(grid) - 1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if grid[mid][0] <= target <= grid[mid][-1]:\n"
            "            return mid\n"
            "        elif target < grid[mid][0]:\n"
            "            hi = mid - 1\n"
            "        else:\n"
            "            lo = mid + 1\n"
            "    return -1\n\n\n"
            "def binary_search_row(grid, target, row):\n"
            "    lo = 0\n"
            "    hi = len(grid[0]) - 1\n"
            "    while lo <= hi:\n"
            "        mid = (lo + hi) // 2\n"
            "        if target < grid[row][mid]:\n"
            "            hi = mid - 1\n"
            "        elif target > grid[row][mid]:\n"
            "            lo = mid + 1\n"
            "        else:\n"
            "            return True\n"
            "    return False\n\n\n"
            "def search_sorted_grid(grid, target):\n"
            "    row = find_row(grid, target)\n"
            "    if row == -1:\n"
            "        return False\n"
            "    else:\n"
            "        return binary_search_row(grid, target, row)\n\n\n"
            "# === Example Test Cases ===\n"
            "grid = [\n"
            "    [1, 3, 5, 7],\n"
            "    [10, 11, 16, 20],\n"
            "    [23, 30, 34, 60]\n"
            "]\n"
            "print(search_sorted_grid(grid, 3))    # -> True\n"
            "print(search_sorted_grid(grid, 13))   # -> False\n"
            "print(search_sorted_grid(grid, 20))   # -> True\n"
            "print(search_sorted_grid(grid, 100))  # -> False\n"
        ),
        "time_complexity": "O(log(m*n))",
        "space_complexity": "O(1)",
        "complexity_type": "O(log n)",
        "complexity_explanation": (
            "Performs binary search across rows to locate candidate row in O(log m) time, then binary searches within that row in O(log n) time. Total time is O(log(m*n)) and space is O(1)."
        ),
    },
    {
        "id": "fib",
        "title": "84. fib",
        "raw_title": "fib",
        "category": "Dynamic Programming",
        "description": (
            "Write a function fib that takes in a number argument, n, and returns the n-th number of the Fibonacci sequence.\n\n"
            "The 0-th number of the sequence is 0.\n\n"
            "The 1-st number of the sequence is 1.\n\n"
            "To generate further numbers of the sequence, calculate the sum of previous two numbers.\n\n"
            "Solve this recursively."
        ),
        "examples": (
            "fib(0)   # -> 0\n"
            "fib(1)   # -> 1\n"
            "fib(5)   # -> 5\n"
            "fib(35)  # -> 9227465\n"
            "fib(46)  # -> 1836311903"
        ),
        "starter_code": (
            "def fib(n):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Memoized Dynamic Programming (O(n)) ===\n"
            "def fib(n):\n"
            "    memo = {}\n"
            "    return _fib(n, memo)\n\n\n"
            "def _fib(n, memo):\n"
            "    if n == 0 or n == 1:\n"
            "        return n\n\n"
            "    if n in memo:\n"
            "        return memo[n]\n\n"
            "    memo[n] = _fib(n - 1, memo) + _fib(n - 2, memo)\n"
            "    return memo[n]\n\n\n"
            "# === Example Test Cases ===\n"
            "print(fib(0))   # -> 0\n"
            "print(fib(1))   # -> 1\n"
            "print(fib(5))   # -> 5\n"
            "print(fib(35))  # -> 9227465\n"
            "print(fib(46))  # -> 1836311903\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "With memoization, each subproblem from 0 to n is solved and cached exactly once. Runs in O(n) time and O(n) call-stack/hash-table space, avoiding the exponential O(2^n) brute force runtime."
        ),
    },
    {
        "id": "tribonacci",
        "title": "85. tribonacci",
        "raw_title": "tribonacci",
        "category": "Dynamic Programming",
        "description": (
            "Write a function tribonacci that takes in a number argument, n, and returns the n-th number of the Tribonacci sequence.\n\n"
            "The 0-th and 1-st numbers of the sequence are both 0.\n\n"
            "The 2-nd number of the sequence is 1.\n\n"
            "To generate further numbers of the sequence, calculate the sum of previous three numbers.\n\n"
            "Solve this recursively."
        ),
        "examples": (
            "tribonacci(0)   # -> 0\n"
            "tribonacci(1)   # -> 0\n"
            "tribonacci(2)   # -> 1\n"
            "tribonacci(5)   # -> 4\n"
            "tribonacci(7)   # -> 13\n"
            "tribonacci(20)  # -> 35890\n"
            "tribonacci(37)  # -> 1132436852"
        ),
        "starter_code": (
            "def tribonacci(n):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Memoized Dynamic Programming (O(n)) ===\n"
            "def tribonacci(n):\n"
            "    return _tribonacci(n, {})\n\n\n"
            "def _tribonacci(n, memo):\n"
            "    if n in memo:\n"
            "        return memo[n]\n\n"
            "    if n == 0 or n == 1:\n"
            "        return 0\n\n"
            "    if n == 2:\n"
            "        return 1\n\n"
            "    memo[n] = _tribonacci(n - 1, memo) + _tribonacci(n - 2, memo) + _tribonacci(n - 3, memo)\n"
            "    return memo[n]\n\n\n"
            "# === Example Test Cases ===\n"
            "print(tribonacci(0))   # -> 0\n"
            "print(tribonacci(1))   # -> 0\n"
            "print(tribonacci(2))   # -> 1\n"
            "print(tribonacci(5))   # -> 4\n"
            "print(tribonacci(7))   # -> 13\n"
            "print(tribonacci(20))  # -> 35890\n"
            "print(tribonacci(37))  # -> 1132436852\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Caches previously computed Tribonacci numbers in a memo dictionary. Reduces an exponential O(3^n) tree to O(n) linear time and O(n) space."
        ),
    },
    {
        "id": "sum_possible",
        "title": "86. sum possible",
        "raw_title": "sum possible",
        "category": "Dynamic Programming",
        "description": (
            "Write a function sum_possible that takes in an amount and a list of positive numbers. The function should return a boolean "
            "indicating whether or not it is possible to create the amount by summing numbers of the list. You may reuse numbers of "
            "the list as many times as necessary.\n\n"
            "You may assume that the target amount is non-negative."
        ),
        "examples": (
            "sum_possible(8, [5, 12, 4])       # -> True (4 + 4)\n"
            "sum_possible(15, [6, 2, 10, 19])  # -> False\n"
            "sum_possible(13, [6, 2, 1])       # -> True\n"
            "sum_possible(103, [6, 20, 1])     # -> True\n"
            "sum_possible(0, [])               # -> True\n"
            "sum_possible(12, [])              # -> False"
        ),
        "starter_code": (
            "def sum_possible(amount, numbers):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Memoized Dynamic Programming (O(amount * n)) ===\n"
            "def sum_possible(amount, numbers):\n"
            "    return _sum_possible(amount, numbers, {})\n\n\n"
            "def _sum_possible(amount, numbers, memo):\n"
            "    if amount in memo:\n"
            "        return memo[amount]\n\n"
            "    if amount < 0:\n"
            "        return False\n\n"
            "    if amount == 0:\n"
            "        return True\n\n"
            "    for num in numbers:\n"
            "        if _sum_possible(amount - num, numbers, memo):\n"
            "            memo[amount] = True\n"
            "            return True\n\n"
            "    memo[amount] = False\n"
            "    return False\n\n\n"
            "# === Example Test Cases ===\n"
            "print(sum_possible(8, [5, 12, 4]))        # -> True (4 + 4)\n"
            "print(sum_possible(15, [6, 2, 10, 19]))   # -> False\n"
            "print(sum_possible(13, [6, 2, 1]))        # -> True\n"
            "print(sum_possible(103, [6, 20, 1]))      # -> True\n"
            "print(sum_possible(0, []))                # -> True\n"
            "print(sum_possible(12, []))               # -> False\n"
        ),
        "time_complexity": "O(a * n)",
        "space_complexity": "O(a)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "There are at most a unique subproblem amounts to solve (where a is the target amount). For each amount, we iterate through n numbers. Memoization bounds the runtime to O(a * n) time and O(a) call-stack space."
        ),
    },
    {
        "id": "min_change",
        "title": "87. min change",
        "raw_title": "min change",
        "category": "Dynamic Programming",
        "description": (
            "Write a function min_change that takes in an amount and a list of coins. The function should return the minimum "
            "number of coins required to create the amount. You may use each coin as many times as necessary.\n\n"
            "If it is not possible to create the amount, then return -1."
        ),
        "examples": (
            "min_change(8, [1, 5, 4, 12])        # -> 2 (4 + 4)\n"
            "min_change(13, [1, 9, 5, 14, 30])   # -> 5 (9 + 1 + 1 + 1 + 1)\n"
            "min_change(23, [2, 5, 7])           # -> 4 (7 + 7 + 7 + 2)\n"
            "min_change(13, [5, 10])             # -> -1\n"
            "min_change(0, [4, 2, 10])           # -> 0"
        ),
        "starter_code": (
            "def min_change(amount, coins):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Memoized Dynamic Programming (O(amount * c)) ===\n"
            "def min_change(amount, coins):\n"
            "    ans = _min_change(amount, coins, {})\n"
            "    if ans == float('inf'):\n"
            "        return -1\n"
            "    else:\n"
            "        return ans\n\n\n"
            "def _min_change(amount, coins, memo):\n"
            "    if amount in memo:\n"
            "        return memo[amount]\n\n"
            "    if amount == 0:\n"
            "        return 0\n\n"
            "    if amount < 0:\n"
            "        return float('inf')\n\n"
            "    min_coins = float('inf')\n"
            "    for coin in coins:\n"
            "        num_coins = 1 + _min_change(amount - coin, coins, memo)\n"
            "        min_coins = min(min_coins, num_coins)\n\n"
            "    memo[amount] = min_coins\n"
            "    return min_coins\n\n\n"
            "# === Example Test Cases ===\n"
            "print(min_change(8, [1, 5, 4, 12]))        # -> 2 (4 + 4)\n"
            "print(min_change(13, [1, 9, 5, 14, 30]))   # -> 5\n"
            "print(min_change(23, [2, 5, 7]))           # -> 4\n"
            "print(min_change(13, [5, 10]))             # -> -1\n"
            "print(min_change(0, [4, 2, 10]))           # -> 0\n"
        ),
        "time_complexity": "O(a * c)",
        "space_complexity": "O(a)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "With memoization, each amount from 0 to a is computed once by exploring c coin choices. Runs in O(a * c) time and O(a) call-stack space where a is amount and c is coin count."
        ),
    },
    {
        "id": "count_paths",
        "title": "88. count paths",
        "raw_title": "count paths",
        "category": "Dynamic Programming",
        "description": (
            "Write a function, count_paths, that takes in a grid as an argument. In the grid, 'X' represents walls and 'O' "
            "represents open spaces. You may only move down or to the right and cannot pass through walls. The function should "
            "return the number of ways possible to travel from the top-left corner of the grid to the bottom-right corner."
        ),
        "examples": (
            "grid = [\n"
            "  ['O', 'O'],\n"
            "  ['O', 'O']\n"
            "]\n"
            "count_paths(grid)  # -> 2\n\n"
            "grid = [\n"
            "  ['O', 'O', 'X'],\n"
            "  ['O', 'O', 'O'],\n"
            "  ['O', 'O', 'O']\n"
            "]\n"
            "count_paths(grid)  # -> 5"
        ),
        "starter_code": (
            "def count_paths(grid):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Grid Memoization (O(r * c)) ===\n"
            "def count_paths(grid):\n"
            "    return _count_paths(grid, 0, 0, {})\n\n\n"
            "def _count_paths(grid, r, c, memo):\n"
            "    pos = (r, c)\n"
            "    if pos in memo:\n"
            "        return memo[pos]\n\n"
            "    if r == len(grid) or c == len(grid[0]) or grid[r][c] == 'X':\n"
            "        return 0\n\n"
            "    if r == len(grid) - 1 and c == len(grid[0]) - 1:\n"
            "        return 1\n\n"
            "    memo[pos] = _count_paths(grid, r + 1, c, memo) + _count_paths(grid, r, c + 1, memo)\n"
            "    return memo[pos]\n\n\n"
            "# === Example Test Cases ===\n"
            "grid = [\n"
            "  ['O', 'O'],\n"
            "  ['O', 'O']\n"
            "]\n"
            "print(count_paths(grid))  # -> 2\n"
        ),
        "time_complexity": "O(r * c)",
        "space_complexity": "O(r * c)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Each position (r, c) in the grid of dimension r by c is visited and cached once. Runs in O(r * c) time and O(r * c) space."
        ),
    },
    {
        "id": "max_path_sum",
        "title": "89. max path sum",
        "raw_title": "max path sum",
        "category": "Dynamic Programming",
        "description": (
            "Write a function, max_path_sum, that takes in a grid as an argument. The function should return the maximum sum "
            "possible by traveling a path from the top-left corner to the bottom-right corner. You may only travel through the grid "
            "by moving down or right.\n\n"
            "You can assume that all numbers are non-negative."
        ),
        "examples": (
            "grid = [\n"
            "  [1, 3, 12],\n"
            "  [5, 1, 1],\n"
            "  [3, 6, 1]\n"
            "]\n"
            "max_path_sum(grid)  # -> 18 (1 + 3 + 12 + 1 + 1)"
        ),
        "starter_code": (
            "def max_path_sum(grid):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Grid Memoization (O(r * c)) ===\n"
            "def max_path_sum(grid):\n"
            "    return _max_path_sum(grid, 0, 0, {})\n\n\n"
            "def _max_path_sum(grid, r, c, memo):\n"
            "    pos = (r, c)\n"
            "    if pos in memo:\n"
            "        return memo[pos]\n\n"
            "    if r == len(grid) or c == len(grid[0]):\n"
            "        return float('-inf')\n\n"
            "    if r == len(grid) - 1 and c == len(grid[0]) - 1:\n"
            "        return grid[r][c]\n\n"
            "    down = _max_path_sum(grid, r + 1, c, memo)\n"
            "    right = _max_path_sum(grid, r, c + 1, memo)\n\n"
            "    memo[pos] = grid[r][c] + max(down, right)\n"
            "    return memo[pos]\n\n\n"
            "# === Example Test Cases ===\n"
            "grid = [\n"
            "  [1, 3, 12],\n"
            "  [5, 1, 1],\n"
            "  [3, 6, 1]\n"
            "]\n"
            "print(max_path_sum(grid))  # -> 18\n"
        ),
        "time_complexity": "O(r * c)",
        "space_complexity": "O(r * c)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Visits each cell (r, c) once and caches the maximum suffix path sum. Runs in O(r * c) time and O(r * c) space."
        ),
    },
    {
        "id": "non_adjacent_sum",
        "title": "90. non adjacent sum",
        "raw_title": "non adjacent sum",
        "category": "Dynamic Programming",
        "description": (
            "Write a function, non_adjacent_sum, that takes in a list of numbers as an argument. The function should return the "
            "maximum sum of non-adjacent items in the list. There is no limit on how many items can be taken into the sum as long "
            "as they are not adjacent.\n\n"
            "You can assume that the numbers are nonnegative."
        ),
        "examples": (
            "non_adjacent_sum([2, 4, 5, 12, 7])  # -> 16 (4 + 12)\n"
            "non_adjacent_sum([7, 5, 5, 12])      # -> 19 (7 + 12)\n"
            "non_adjacent_sum([7, 5, 5, 12, 17, 29]) # -> 48"
        ),
        "starter_code": (
            "def non_adjacent_sum(nums):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Memoized Dynamic Programming (O(n)) ===\n"
            "def non_adjacent_sum(nums):\n"
            "    return _non_adjacent_sum(nums, 0, {})\n\n\n"
            "def _non_adjacent_sum(nums, i, memo):\n"
            "    if i in memo:\n"
            "        return memo[i]\n\n"
            "    if i >= len(nums):\n"
            "        return 0\n\n"
            "    include = nums[i] + _non_adjacent_sum(nums, i + 2, memo)\n"
            "    exclude = _non_adjacent_sum(nums, i + 1, memo)\n"
            "    memo[i] = max(include, exclude)\n"
            "    return memo[i]\n\n\n"
            "# === Example Test Cases ===\n"
            "print(non_adjacent_sum([2, 4, 5, 12, 7]))  # -> 16\n"
            "print(non_adjacent_sum([7, 5, 5, 12]))      # -> 19\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "At each index i, compares including nums[i] (skipping to i+2) vs excluding nums[i] (moving to i+1). Each subproblem i is computed once, running in O(n) time and O(n) space."
        ),
    },
    {
        "id": "summing_squares",
        "title": "91. summing squares",
        "raw_title": "summing squares",
        "category": "Dynamic Programming",
        "description": (
            "Write a function, summing_squares, that takes a target number as an argument. The function should return the minimum "
            "number of perfect squares that sum to the target. A perfect square is a number of the form (i*i) where i >= 1.\n\n"
            "For example: 1, 4, 9, 16 are perfect squares, but 8 is not a perfect square."
        ),
        "examples": (
            "summing_squares(8)   # -> 2 (4 + 4)\n"
            "summing_squares(9)   # -> 1 (9)\n"
            "summing_squares(12)  # -> 3 (4 + 4 + 4)\n"
            "summing_squares(1)   # -> 1"
        ),
        "starter_code": (
            "def summing_squares(n):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "import math\n\n\n"
            "# === Memoized Dynamic Programming (O(n * sqrt(n))) ===\n"
            "def summing_squares(n):\n"
            "    return _summing_squares(n, {})\n\n\n"
            "def _summing_squares(n, memo):\n"
            "    if n in memo:\n"
            "        return memo[n]\n\n"
            "    if n == 0:\n"
            "        return 0\n\n"
            "    min_squares = float('inf')\n"
            "    for i in range(1, math.floor(math.sqrt(n) + 1)):\n"
            "        square = i * i\n"
            "        num_squares = 1 + _summing_squares(n - square, memo)\n"
            "        min_squares = min(min_squares, num_squares)\n\n"
            "    memo[n] = min_squares\n"
            "    return min_squares\n\n\n"
            "# === Example Test Cases ===\n"
            "print(summing_squares(8))   # -> 2 (4 + 4)\n"
            "print(summing_squares(9))   # -> 1 (9)\n"
            "print(summing_squares(12))  # -> 3 (4 + 4 + 4)\n"
        ),
        "time_complexity": "O(n * sqrt(n))",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Computes each value from 1 to n once. For each target, iterates over at most sqrt(n) perfect squares. Runs in O(n * sqrt(n)) time and O(n) space."
        ),
    },
    {
        "id": "counting_change",
        "title": "92. counting change",
        "raw_title": "counting change",
        "category": "Dynamic Programming",
        "description": (
            "Write a function, counting_change, that takes in an amount and a list of coins. The function should return the "
            "number of different ways it is possible to make change for the given amount using the coins.\n\n"
            "You may reuse a coin as many times as necessary."
        ),
        "examples": (
            "counting_change(4, [1, 2, 3])      # -> 4\n"
            "counting_change(8, [1, 5, 4, 12])   # -> 6\n"
            "counting_change(24, [5, 7, 3])      # -> 5\n"
            "counting_change(0, [16])            # -> 1"
        ),
        "starter_code": (
            "def counting_change(amount, coins):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === 2D Memoized Dynamic Programming (O(amount * c)) ===\n"
            "def counting_change(amount, coins):\n"
            "    return _counting_change(amount, coins, 0, {})\n\n\n"
            "def _counting_change(amount, coins, i, memo):\n"
            "    key = (amount, i)\n"
            "    if key in memo:\n"
            "        return memo[key]\n\n"
            "    if amount == 0:\n"
            "        return 1\n\n"
            "    if i == len(coins):\n"
            "        return 0\n\n"
            "    coin = coins[i]\n"
            "    total_count = 0\n"
            "    for qty in range(0, (amount // coin) + 1):\n"
            "        remainder = amount - (qty * coin)\n"
            "        total_count += _counting_change(remainder, coins, i + 1, memo)\n\n"
            "    memo[key] = total_count\n"
            "    return total_count\n\n\n"
            "# === Example Test Cases ===\n"
            "print(counting_change(4, [1, 2, 3]))      # -> 4\n"
            "print(counting_change(8, [1, 5, 4, 12]))   # -> 6\n"
            "print(counting_change(24, [5, 7, 3]))      # -> 5\n"
        ),
        "time_complexity": "O(a * c)",
        "space_complexity": "O(a * c)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Tracks subproblems keyed by (amount, coin_index). Each unique pair is solved once, running in O(a * c) time and O(a * c) space where a is amount and c is coin count."
        ),
    },
    {
        "id": "array_stepper",
        "title": "93. array stepper",
        "raw_title": "array stepper",
        "category": "Dynamic Programming",
        "description": (
            "Write a function, array_stepper, that takes in a list of numbers as an argument. You start at the first position "
            "of the list. The function should return a boolean indicating whether or not it is possible to reach the last "
            "position of the list. When situated at some position of the list, you may take a maximum number of steps based on "
            "the number at that position."
        ),
        "examples": (
            "array_stepper([2, 4, 2, 0, 0, 1])          # -> True\n"
            "array_stepper([2, 3, 1, 1, 0, 4, 7, 8])    # -> False\n"
            "array_stepper([1, 1, 1, 1, 1, 0])          # -> True"
        ),
        "starter_code": (
            "def array_stepper(numbers):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Memoized Dynamic Programming (O(n^2)) ===\n"
            "def array_stepper(numbers):\n"
            "    return _array_stepper(numbers, 0, {})\n\n\n"
            "def _array_stepper(numbers, i, memo):\n"
            "    if i in memo:\n"
            "        return memo[i]\n\n"
            "    if i >= len(numbers) - 1:\n"
            "        return True\n\n"
            "    max_step = numbers[i]\n"
            "    for step in range(1, max_step + 1):\n"
            "        if _array_stepper(numbers, i + step, memo):\n"
            "            memo[i] = True\n"
            "            return True\n\n"
            "    memo[i] = False\n"
            "    return False\n\n\n"
            "# === Example Test Cases ===\n"
            "print(array_stepper([2, 4, 2, 0, 0, 1]))          # -> True\n"
            "print(array_stepper([2, 3, 1, 1, 0, 4, 7, 8]))    # -> False\n"
        ),
        "time_complexity": "O(n^2)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Each index i is visited once and can branch up to numbers[i] <= n forward steps. Runs in O(n^2) worst-case time and O(n) space."
        ),
    },
    {
        "id": "max_palin_subsequence",
        "title": "94. max palin subsequence",
        "raw_title": "max palin subsequence",
        "category": "Dynamic Programming",
        "description": (
            "Write a function, max_palin_subsequence, that takes in a string as an argument. The function should return the "
            "length of the longest subsequence of the string that is also a palindrome.\n\n"
            "A subsequence of a string can be created by deleting any characters of the string, while maintaining the relative order of characters."
        ),
        "examples": (
            "max_palin_subsequence('luwxult')   # -> 5 ('luxul')\n"
            "max_palin_subsequence('xyzaxxzy')  # -> 6\n"
            "max_palin_subsequence('lol')       # -> 3"
        ),
        "starter_code": (
            "def max_palin_subsequence(string):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Two-Pointer Interval Memoization (O(n^2)) ===\n"
            "def max_palin_subsequence(string):\n"
            "    return _max_palin_subsequence(string, 0, len(string) - 1, {})\n\n\n"
            "def _max_palin_subsequence(string, i, j, memo):\n"
            "    key = (i, j)\n"
            "    if key in memo:\n"
            "        return memo[key]\n\n"
            "    if i == j:\n"
            "        return 1\n\n"
            "    if i > j:\n"
            "        return 0\n\n"
            "    if string[i] == string[j]:\n"
            "        memo[key] = 2 + _max_palin_subsequence(string, i + 1, j - 1, memo)\n"
            "    else:\n"
            "        memo[key] = max(\n"
            "            _max_palin_subsequence(string, i + 1, j, memo),\n"
            "            _max_palin_subsequence(string, i, j - 1, memo)\n"
            "        )\n\n"
            "    return memo[key]\n\n\n"
            "# === Example Test Cases ===\n"
            "print(max_palin_subsequence('luwxult'))   # -> 5\n"
            "print(max_palin_subsequence('xyzaxxzy'))  # -> 6\n"
        ),
        "time_complexity": "O(n^2)",
        "space_complexity": "O(n^2)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Subproblems correspond to substrings s[i:j+1], yielding O(n^2) interval states. Each state is evaluated in O(1) time, giving O(n^2) time and O(n^2) space."
        ),
    },
    {
        "id": "overlap_subsequence",
        "title": "95. overlap subsequence",
        "raw_title": "overlap subsequence",
        "category": "Dynamic Programming",
        "description": (
            "Write a function, overlap_subsequence, that takes in two strings as arguments. The function should return the "
            "length of the longest overlapping subsequence.\n\n"
            "A subsequence of a string can be created by deleting any characters of the string, while maintaining the relative order of characters."
        ),
        "examples": (
            "overlap_subsequence('dogs', 'daaaaogs')      # -> 4 ('dogs')\n"
            "overlap_subsequence('xcyats', 'cactivity')   # -> 4 ('cats')\n"
            "overlap_subsequence('kinfolks', 'frogs')     # -> 2 ('os')"
        ),
        "starter_code": (
            "def overlap_subsequence(string_1, string_2):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Longest Common Subsequence Memoization (O(n * m)) ===\n"
            "def overlap_subsequence(string_1, string_2):\n"
            "    return _overlap_subsequence(string_1, string_2, 0, 0, {})\n\n\n"
            "def _overlap_subsequence(string_1, string_2, i, j, memo):\n"
            "    key = (i, j)\n"
            "    if key in memo:\n"
            "        return memo[key]\n\n"
            "    if i == len(string_1) or j == len(string_2):\n"
            "        return 0\n\n"
            "    if string_1[i] == string_2[j]:\n"
            "        memo[key] = 1 + _overlap_subsequence(string_1, string_2, i + 1, j + 1, memo)\n"
            "    else:\n"
            "        memo[key] = max(\n"
            "            _overlap_subsequence(string_1, string_2, i + 1, j, memo),\n"
            "            _overlap_subsequence(string_1, string_2, i, j + 1, memo)\n"
            "        )\n"
            "    return memo[key]\n\n\n"
            "# === Example Test Cases ===\n"
            "print(overlap_subsequence('dogs', 'daaaaogs'))    # -> 4\n"
            "print(overlap_subsequence('xcyats', 'cactivity')) # -> 4\n"
        ),
        "time_complexity": "O(n * m)",
        "space_complexity": "O(n * m)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Standard LCS formulation over indices (i, j). Solves and caches n * m subproblems in O(n * m) time and O(n * m) space."
        ),
    },
    {
        "id": "can_concat",
        "title": "96. can concat",
        "raw_title": "can concat",
        "category": "Dynamic Programming",
        "description": (
            "Write a function, can_concat, that takes in a string and a list of words as arguments. The function should return a "
            "boolean indicating whether or not it is possible to concatenate words of the list together to form the string.\n\n"
            "You may reuse words of the list as many times as needed."
        ),
        "examples": (
            "can_concat('oneisnone', ['one', 'none', 'is'])     # -> True\n"
            "can_concat('oneisnone', ['on', 'e', 'is'])         # -> False\n"
            "can_concat('santahat', ['santah', 'hat'])          # -> False"
        ),
        "starter_code": (
            "def can_concat(s, words):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === String Prefix Memoization (O(s * w * max_len)) ===\n"
            "def can_concat(s, words):\n"
            "    return _can_concat(s, words, 0, {})\n\n\n"
            "def _can_concat(s, words, i, memo):\n"
            "    if i in memo:\n"
            "        return memo[i]\n\n"
            "    if i == len(s):\n"
            "        return True\n\n"
            "    for word in words:\n"
            "        if s.startswith(word, i):\n"
            "            if _can_concat(s, words, i + len(word), memo) == True:\n"
            "                memo[i] = True\n"
            "                return True\n\n"
            "    memo[i] = False\n"
            "    return False\n\n\n"
            "# === Example Test Cases ===\n"
            "print(can_concat('oneisnone', ['one', 'none', 'is']))  # -> True\n"
            "print(can_concat('oneisnone', ['on', 'e', 'is']))      # -> False\n"
        ),
        "time_complexity": "O(s * w)",
        "space_complexity": "O(s)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "There are s possible suffix index states. At each index, checks w words with prefix matching. Runs in O(s * w * max_len) time and O(s) space."
        ),
    },
    {
        "id": "quickest_concat",
        "title": "97. quickest concat",
        "raw_title": "quickest concat",
        "category": "Dynamic Programming",
        "description": (
            "Write a function, quickest_concat, that takes in a string and a list of words as arguments. The function should "
            "return the minimum number of words needed to build the string by concatenating words of the list. If it is not "
            "possible to build the string, then return -1.\n\n"
            "You may use words of the list as many times as needed."
        ),
        "examples": (
            "quickest_concat('caution', ['ca', 'ion', 'caut', 'ut'])           # -> 2 ('caut' + 'ion')\n"
            "quickest_concat('caution', ['ion', 'caut', 'caution'])            # -> 1 ('caution')\n"
            "quickest_concat('respondormir', ['respond', 'dormir', 'yes'])     # -> 2"
        ),
        "starter_code": (
            "def quickest_concat(s, words):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Min Word Concatenation (O(s * w * max_len)) ===\n"
            "def quickest_concat(s, words):\n"
            "    result = _quickest_concat(s, words, 0, {})\n"
            "    if result == float('inf'):\n"
            "        return -1\n"
            "    else:\n"
            "        return result\n\n\n"
            "def _quickest_concat(s, words, i, memo):\n"
            "    if i in memo:\n"
            "        return memo[i]\n\n"
            "    if i == len(s):\n"
            "        return 0\n\n"
            "    min_words = float('inf')\n"
            "    for word in words:\n"
            "        if s.startswith(word, i):\n"
            "            attempt = 1 + _quickest_concat(s, words, i + len(word), memo)\n"
            "            min_words = min(attempt, min_words)\n\n"
            "    memo[i] = min_words\n"
            "    return min_words\n\n\n"
            "# === Example Test Cases ===\n"
            "print(quickest_concat('caution', ['ca', 'ion', 'caut', 'ut']))       # -> 2\n"
            "print(quickest_concat('caution', ['ion', 'caut', 'caution']))        # -> 1\n"
        ),
        "time_complexity": "O(s * w)",
        "space_complexity": "O(s)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Evaluates each suffix index i by finding the minimum branch count across all matching words. Runs in O(s * w * max_len) time and O(s) space."
        ),
    },
    {
        "id": "valid_compound",
        "title": "98. valid compound",
        "raw_title": "valid compound",
        "category": "Dynamic Programming",
        "description": (
            "You are a chemist and have to figure out if you can make a compound from some given elements!\n\n"
            "Write a function, valid_compound, that takes in a target compound and a list of elements. The function should "
            "return a boolean indicating whether or not the compound can be created from the given elements.\n\n"
            "A compound is made by concatenating one or more elements together.\n\n"
            "You may reuse elements of the list as many times as needed to make a compound."
        ),
        "examples": (
            "valid_compound('water', ['H', 'He', 'W', 'At', 'Er'])           # -> True\n"
            "valid_compound('crafter', ['C', 'Ra', 'F', 'Te', 'R', 'K'])     # -> True\n"
            "valid_compound('rubber', ['R', 'U', 'B', 'Be', 'Ar'])           # -> False"
        ),
        "starter_code": (
            "def valid_compound(compound, elements):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Case-Insensitive Prefix Memoization (O(c * e)) ===\n"
            "def valid_compound(compound, elements):\n"
            "    return _valid_compound(compound, elements, 0, {})\n\n\n"
            "def _valid_compound(compound, elements, i, memo):\n"
            "    if i == len(compound):\n"
            "        return True\n\n"
            "    if i in memo:\n"
            "        return memo[i]\n\n"
            "    for ele in elements:\n"
            "        if compound.startswith(ele.lower(), i):\n"
            "            if _valid_compound(compound, elements, i + len(ele), memo):\n"
            "                memo[i] = True\n"
            "                return True\n\n"
            "    memo[i] = False\n"
            "    return False\n\n\n"
            "# === Example Test Cases ===\n"
            "print(valid_compound('water', ['H', 'He', 'W', 'At', 'Er']))       # -> True\n"
            "print(valid_compound('rubber', ['R', 'U', 'B', 'Be', 'Ar']))       # -> False\n"
        ),
        "time_complexity": "O(c * e)",
        "space_complexity": "O(c)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Matches elements case-insensitively against suffixes of length c. Each index i is solved once, giving O(c * e) time and O(c) space."
        ),
    },
    {
        "id": "count_compounds",
        "title": "99. count compounds",
        "raw_title": "count compounds",
        "category": "Dynamic Programming",
        "description": (
            "You are a chemist and have to figure out how many ways you can make a given compound.\n\n"
            "Write a function, count_compounds, that takes in a target compound and a list of elements. The function should "
            "return the number of ways we can make the compound with the given elements.\n\n"
            "A compound is made by concatenating one or more elements together.\n\n"
            "You may reuse elements of the list as many times as needed to make a compound."
        ),
        "examples": (
            "count_compounds('crafter', ['C', 'Ra', 'F', 'Te', 'R', 'K'])   # -> 1\n"
            "count_compounds('banana', ['Ba', 'Na', 'An', 'A'])            # -> 4\n"
            "count_compounds('rubber', ['R', 'U', 'B', 'Be', 'Ar'])        # -> 0"
        ),
        "starter_code": (
            "def count_compounds(compound, elements):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Case-Insensitive Way-Counting (O(c * e)) ===\n"
            "def count_compounds(compound, elements):\n"
            "    return _count_compounds(compound, elements, 0, {})\n\n\n"
            "def _count_compounds(compound, elements, idx, memo):\n"
            "    if idx == len(compound):\n"
            "        return 1\n\n"
            "    if idx in memo:\n"
            "        return memo[idx]\n\n"
            "    count = 0\n"
            "    for ele in elements:\n"
            "        if compound.startswith(ele.lower(), idx):\n"
            "            count += _count_compounds(compound, elements, idx + len(ele), memo)\n\n"
            "    memo[idx] = count\n"
            "    return count\n\n\n"
            "# === Example Test Cases ===\n"
            "print(count_compounds('crafter', ['C', 'Ra', 'F', 'Te', 'R', 'K']))  # -> 1\n"
            "print(count_compounds('banana', ['Ba', 'Na', 'An', 'A']))            # -> 4\n"
        ),
        "time_complexity": "O(c * e)",
        "space_complexity": "O(c)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Sums combinations for each suffix index, caching results to avoid recalculating overlapping subproblems. Runs in O(c * e) time and O(c) space."
        ),
    },
    {
        "id": "longest_path",
        "title": "100. longest path",
        "raw_title": "longest path",
        "category": "Dynamic Programming",
        "description": (
            "Write a function, longest_path, that takes in an adjacency list for a directed acyclic graph. The function should "
            "return the length of the longest path within the graph. A path may start and end at any two nodes. The length of a path "
            "is considered the number of edges in the path, not the number of nodes."
        ),
        "examples": (
            "graph = {\n"
            "  'a': ['c', 'b'],\n"
            "  'b': ['c'],\n"
            "  'c': []\n"
            "}\n"
            "longest_path(graph)  # -> 2 ('a' -> 'b' -> 'c')"
        ),
        "starter_code": (
            "def longest_path(graph):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === DAG Longest Path via Post-Order Memoization (O(e)) ===\n"
            "def longest_path(graph):\n"
            "    distance = {}\n"
            "    for node in graph:\n"
            "        if len(graph[node]) == 0:\n"
            "            distance[node] = 0\n\n"
            "    for node in graph:\n"
            "        traverse_distance(graph, node, distance)\n\n"
            "    return max(distance.values())\n\n\n"
            "def traverse_distance(graph, node, distance):\n"
            "    if node in distance:\n"
            "        return distance[node]\n\n"
            "    largest = 0\n"
            "    for neighbor in graph[node]:\n"
            "        attempt = traverse_distance(graph, neighbor, distance)\n"
            "        if attempt > largest:\n"
            "            largest = attempt\n\n"
            "    distance[node] = 1 + largest\n"
            "    return distance[node]\n\n\n"
            "# === Example Test Cases ===\n"
            "graph = {\n"
            "  'a': ['c', 'b'],\n"
            "  'b': ['c'],\n"
            "  'c': []\n"
            "}\n"
            "print(longest_path(graph))  # -> 2\n"
        ),
        "time_complexity": "O(e)",
        "space_complexity": "O(v)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Explores a DAG memoizing the longest path from each node to any terminal node. Each edge is traversed once, yielding O(e) time and O(v) space."
        ),
    },
    {
        "id": "semesters_required",
        "title": "101. semesters required",
        "raw_title": "semesters required",
        "category": "Dynamic Programming",
        "description": (
            "Write a function, semesters_required, that takes in a number of courses (n) and a list of prerequisites as arguments. "
            "Courses have ids ranging from 0 through n - 1. A single prerequisite of (A, B) means that course A must be taken before "
            "course B. Return the minimum number of semesters required to complete all n courses. There is no limit on how many "
            "courses you can take in a single semester, as long as the prerequisites of a course are satisfied before taking it.\n\n"
            "Note that given prerequisite (A, B), you cannot take course A and course B concurrently in the same semester. "
            "You must take A in some semester before B.\n\n"
            "You can assume that it is possible to eventually complete all courses."
        ),
        "examples": (
            "semesters_required(6, [(1, 2), (2, 4), (3, 5), (0, 5)])  # -> 3\n"
            "semesters_required(7, [(4, 3), (3, 2), (2, 1), (1, 0), (5, 2), (5, 6)]) # -> 5"
        ),
        "starter_code": (
            "def semesters_required(num_courses, prereqs):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Prerequisite DAG Critical Path (O(c + p)) ===\n"
            "def semesters_required(num_courses, prereqs):\n"
            "    graph = build_graph(num_courses, prereqs)\n"
            "    distance = {}\n"
            "    for course in range(num_courses):\n"
            "        if len(graph[course]) == 0:\n"
            "            distance[course] = 1\n\n"
            "    for course in range(num_courses):\n"
            "        traverse_distance(graph, course, distance)\n\n"
            "    return max(distance.values())\n\n\n"
            "def traverse_distance(graph, node, distance):\n"
            "    if node in distance:\n"
            "        return distance[node]\n\n"
            "    max_distance = 0\n"
            "    for neighbor in graph[node]:\n"
            "        neighbor_distance = traverse_distance(graph, neighbor, distance)\n"
            "        if neighbor_distance > max_distance:\n"
            "            max_distance = neighbor_distance\n\n"
            "    distance[node] = 1 + max_distance\n"
            "    return distance[node]\n\n\n"
            "def build_graph(num_courses, prereqs):\n"
            "    graph = {}\n"
            "    for course in range(num_courses):\n"
            "        graph[course] = []\n"
            "    for prereq in prereqs:\n"
            "        a, b = prereq\n"
            "        graph[a].append(b)\n"
            "    return graph\n\n\n"
            "# === Example Test Cases ===\n"
            "print(semesters_required(6, [(1, 2), (2, 4), (3, 5), (0, 5)]))  # -> 3\n"
        ),
        "time_complexity": "O(c + p)",
        "space_complexity": "O(c + p)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Builds prerequisite graph and computes the longest directed path through the DAG with memoization. Runs in O(c + p) time and O(c + p) space where c is courses and p is prereqs."
        ),
    },
    {
        "id": "reverse_some_chars",
        "title": "102. reverse some chars",
        "raw_title": "reverse some chars",
        "category": "Stack",
        "description": (
            "Write a function, reverse_some_chars, that takes in string and an list of target characters. "
            "The function should return the string with the order of the given characters in reverse."
        ),
        "examples": (
            "reverse_some_chars('hello world', ['e', 'o'])       # -> 'hollo werld'\n"
            "reverse_some_chars('apple', ['a', 'p', 'e'])        # -> 'eppla'\n"
            "reverse_some_chars('abstraction', ['a', 't', 'i'])  # -> 'ibstrctaon'"
        ),
        "starter_code": (
            "def reverse_some_chars(s, chars):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Stack Approach (O(n)) ===\n"
            "def reverse_some_chars(s, chars):\n"
            "    char_set = set(chars)\n"
            "    stack = []\n"
            "    for ch in s:\n"
            "        if ch in char_set:\n"
            "            stack.append(ch)\n\n"
            "    result = []\n"
            "    for ch in s:\n"
            "        if ch in char_set:\n"
            "            result.append(stack.pop())\n"
            "        else:\n"
            "            result.append(ch)\n\n"
            "    return ''.join(result)\n\n\n"
            "# === Example Test Cases ===\n"
            "print(reverse_some_chars('hello world', ['e', 'o']))       # -> 'hollo werld'\n"
            "print(reverse_some_chars('apple', ['a', 'p', 'e']))        # -> 'eppla'\n"
            "print(reverse_some_chars('abstraction', ['a', 't', 'i']))  # -> 'ibstrctaon'\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Pushes matching characters onto a LIFO stack in a first pass, then pops them in reverse order during the second pass. Runs in O(n) time and O(n) space."
        ),
    },
    {
        "id": "paired_parentheses",
        "title": "103. paired parentheses",
        "raw_title": "paired parentheses",
        "category": "Stack",
        "description": (
            "Write a function, paired_parentheses, that takes in a string as an argument. The function should return a boolean "
            "indicating whether or not the string has well-formed parentheses.\n\n"
            "You may assume the string contains only alphabetic characters, '(', or ')'."
        ),
        "examples": (
            "paired_parentheses('(david)((cb))')          # -> True\n"
            "paired_parentheses('()rose( AnTelephone )')  # -> True\n"
            "paired_parentheses(')(')                     # -> False\n"
            "paired_parentheses('()')                     # -> True\n"
            "paired_parentheses('(())(bb')                # -> False"
        ),
        "starter_code": (
            "def paired_parentheses(string):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Counter / Stack Approach (O(n)) ===\n"
            "def paired_parentheses(string):\n"
            "    count = 0\n"
            "    for char in string:\n"
            "        if char == '(': \n"
            "            count += 1\n"
            "        elif char == ')':\n"
            "            if count == 0:\n"
            "                return False\n"
            "            count -= 1\n"
            "    return count == 0\n\n\n"
            "# === Example Test Cases ===\n"
            "print(paired_parentheses('(david)((cb))'))          # -> True\n"
            "print(paired_parentheses('()rose( AnTelephone )'))  # -> True\n"
            "print(paired_parentheses(')('))                     # -> False\n"
            "print(paired_parentheses('(())(bb'))                # -> False\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Tracks open parentheses counter. Decrements on closing paren, rejecting immediately if count drops below zero. Runs in O(n) time and O(1) space."
        ),
    },
    {
        "id": "befitting_brackets",
        "title": "104. befitting brackets",
        "raw_title": "befitting brackets",
        "category": "Stack",
        "description": (
            "Write a function, befitting_brackets, that takes in a string as an argument. The function should return a boolean "
            "indicating whether or not the string contains correctly matched brackets.\n\n"
            "You may assume the string contains only characters: ( ) [ ] { }"
        ),
        "examples": (
            "befitting_brackets('(){}[](())')  # -> True\n"
            "befitting_brackets('({[]})')      # -> True\n"
            "befitting_brackets('[][}')        # -> False\n"
            "befitting_brackets('{[(])}')      # -> False\n"
            "befitting_brackets('{[}')         # -> False"
        ),
        "starter_code": (
            "def befitting_brackets(string):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Stack Matching (O(n)) ===\n"
            "def befitting_brackets(string):\n"
            "    stack = []\n"
            "    brackets = {\n"
            "        '(': ')',\n"
            "        '[': ']',\n"
            "        '{': '}',\n"
            "    }\n"
            "    for char in string:\n"
            "        if char in brackets:\n"
            "            stack.append(brackets[char])\n"
            "        else:\n"
            "            if stack and stack[-1] == char:\n"
            "                stack.pop()\n"
            "            else:\n"
            "                return False\n"
            "    return len(stack) == 0\n\n\n"
            "# === Example Test Cases ===\n"
            "print(befitting_brackets('(){}[](())'))  # -> True\n"
            "print(befitting_brackets('({[]})'))      # -> True\n"
            "print(befitting_brackets('[][}'))        # -> False\n"
            "print(befitting_brackets('{[(])}'))      # -> False\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Pushes expected closing brackets onto a stack when opening brackets appear. Pops and compares on closing brackets, verifying balanced brackets in O(n) time and O(n) space."
        ),
    },
    {
        "id": "decompress_braces",
        "title": "105. decompress braces",
        "raw_title": "decompress braces",
        "category": "Stack",
        "description": (
            "Write a function, decompress_braces, that takes in a compressed string as an argument. The function should return the "
            "string decompressed.\n\n"
            "The compression format of the input string is 'n{sub_string}', where the sub_string within braces should be repeated n times.\n\n"
            "You may assume that every number n is guaranteed to be an integer between 1 through 9.\n\n"
            "You may assume that the input is valid and the decompressed string will only contain alphabetic characters."
        ),
        "examples": (
            "decompress_braces('2{q}3{tu}v')    # -> 'qqtututuv'\n"
            "decompress_braces('ch3{ao}')       # -> 'chaoaoao'\n"
            "decompress_braces('2{y3{o}}s')     # -> 'yoooyooos'\n"
            "decompress_braces('z3{a} 2{b}')    # -> 'zaaabb'"
        ),
        "starter_code": (
            "def decompress_braces(string):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Stack Evaluation (O(m)) ===\n"
            "def decompress_braces(string):\n"
            "    numbers = '123456789'\n"
            "    stack = []\n"
            "    for char in string:\n"
            "        if char in numbers:\n"
            "            stack.append(int(char))\n"
            "        else:\n"
            "            if char == '}':\n"
            "                segment = ''\n"
            "                while isinstance(stack[-1], str):\n"
            "                    popped = stack.pop()\n"
            "                    segment = popped + segment\n"
            "                num = stack.pop()\n"
            "                stack.append(segment * num)\n"
            "            elif char != '{':\n"
            "                stack.append(char)\n"
            "    return ''.join(stack)\n\n\n"
            "# === Example Test Cases ===\n"
            "print(decompress_braces('2{q}3{tu}v'))    # -> 'qqtututuv'\n"
            "print(decompress_braces('ch3{ao}'))       # -> 'chaoaoao'\n"
            "print(decompress_braces('2{y3{o}}s'))     # -> 'yoooyooos'\n"
        ),
        "time_complexity": "O(m)",
        "space_complexity": "O(m)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Pushes numbers and characters onto a stack, expanding nested segments upon hitting closing brace '}'. Runs in O(m) time and O(m) space where m is the uncompressed length."
        ),
    },
    {
        "id": "nesting_score",
        "title": "106. nesting score",
        "raw_title": "nesting score",
        "category": "Stack",
        "description": (
            "Write a function, nesting_score, that takes in a string of brackets as an argument. The function should return the "
            "score of the string according to the following rules:\n\n"
            "[] is worth 1 point\n"
            "XY is worth X + Y points where X, Y are substrings of well-formed brackets\n"
            "[S] is worth S * 2 points where S is a substring of well-formed brackets\n\n"
            "For example:\n"
            "[[][][]] is equivalent to (1 + 1 + 1) * 2 = 6\n\n"
            "You may assume that the input only contains well-formed square brackets."
        ),
        "examples": (
            "nesting_score('[]')          # -> 1\n"
            "nesting_score('[][][]')      # -> 3\n"
            "nesting_score('[[]]')        # -> 2\n"
            "nesting_score('[[][]]')      # -> 4\n"
            "nesting_score('[[][][]]')    # -> 6\n"
            "nesting_score('[[][]][[]]')  # -> 6"
        ),
        "starter_code": (
            "def nesting_score(string):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Stack Scoring (O(n)) ===\n"
            "def nesting_score(string):\n"
            "    stack = [0]\n"
            "    for char in string:\n"
            "        if char == '[':\n"
            "            stack.append(0)\n"
            "        else:\n"
            "            popped = stack.pop()\n"
            "            if popped == 0:\n"
            "                stack[-1] += 1\n"
            "            else:\n"
            "                stack[-1] += 2 * popped\n"
            "    return stack[0]\n\n\n"
            "# === Example Test Cases ===\n"
            "print(nesting_score('[]'))          # -> 1\n"
            "print(nesting_score('[][][]'))      # -> 3\n"
            "print(nesting_score('[[]]'))        # -> 2\n"
            "print(nesting_score('[[][]]'))      # -> 4\n"
            "print(nesting_score('[[][][]]'))    # -> 6\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Maintains a stack of nested score totals. Adds 1 for empty bracket pairs [] or doubles the inner enclosed sum for [S]. Runs in O(n) time and O(n) space."
        ),
    },
    {
        "id": "running_sum",
        "title": "107. running sum",
        "raw_title": "running sum",
        "category": "Array and String",
        "description": (
            "Write a function, running_sum, that takes in a list of numbers. The function should return a new list of the same "
            "length where each element contains the running sum up to that index of the original list."
        ),
        "examples": (
            "running_sum([1, 2, 3, 4])        # -> [1, 3, 6, 10]\n"
            "running_sum([1, 1, 1, 1, 1])     # -> [1, 2, 3, 4, 5]\n"
            "running_sum([3, 1, 2, 10, 1])    # -> [3, 4, 6, 16, 17]\n"
            "running_sum([])                  # -> []"
        ),
        "starter_code": (
            "def running_sum(numbers):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Prefix Running Sum (O(n)) ===\n"
            "def running_sum(numbers):\n"
            "    total = 0\n"
            "    result = []\n"
            "    for num in numbers:\n"
            "        total += num\n"
            "        result.append(total)\n"
            "    return result\n\n\n"
            "# === Example Test Cases ===\n"
            "print(running_sum([1, 2, 3, 4]))        # -> [1, 3, 6, 10]\n"
            "print(running_sum([1, 1, 1, 1, 1]))     # -> [1, 2, 3, 4, 5]\n"
            "print(running_sum([3, 1, 2, 10, 1]))    # -> [3, 4, 6, 16, 17]\n"
            "print(running_sum([]))                  # -> []\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Iterates linearly through numbers, accumulating a rolling total and appending to result. Runs in O(n) time and O(n) space."
        ),
    },
    {
        "id": "has_subarray_sum",
        "title": "108. has subarray sum",
        "raw_title": "has subarray sum",
        "category": "Array and String",
        "description": (
            "Write a function, has_subarray_sum, that takes in an list of numbers and a target_sum. The function should return a "
            "boolean indicating whether or not there exists a subarray of numbers that sums to the given target.\n\n"
            "A subarray is a consecutive series of one or more elements of the list."
        ),
        "examples": (
            "has_subarray_sum([1, 4, 20, 3, 10, 5], 33)  # -> True (20 + 3 + 10)\n"
            "has_subarray_sum([1, 2, 3], 6)               # -> True (1 + 2 + 3)\n"
            "has_subarray_sum([1, 2, 3], 7)               # -> False\n"
            "has_subarray_sum([1, -1, 1, -1], 0)          # -> True"
        ),
        "starter_code": (
            "def has_subarray_sum(numbers, target_sum):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Prefix Sums Hash Set (O(n)) ===\n"
            "def has_subarray_sum(numbers, target_sum):\n"
            "    prefix_sums = {0}\n"
            "    total = 0\n"
            "    for num in numbers:\n"
            "        total += num\n"
            "        if (total - target_sum) in prefix_sums:\n"
            "            return True\n"
            "        prefix_sums.add(total)\n"
            "    return False\n\n\n"
            "# === Example Test Cases ===\n"
            "print(has_subarray_sum([1, 4, 20, 3, 10, 5], 33))  # -> True\n"
            "print(has_subarray_sum([1, 2, 3], 6))               # -> True\n"
            "print(has_subarray_sum([1, 2, 3], 7))               # -> False\n"
            "print(has_subarray_sum([1, -1, 1, -1], 0))          # -> True\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Computes running prefix sums and checks if (current_sum - target_sum) was previously seen in O(1) set lookup time. Runs in O(n) time and O(n) space."
        ),
    },
    {
        "id": "subarray_sum_count",
        "title": "109. subarray sum count",
        "raw_title": "subarray sum count",
        "category": "Array and String",
        "description": (
            "Write a function, subarray_sum_count, that takes in an list of numbers and a targetSum. The function should return the "
            "number of subarrays that sum to the given target.\n\n"
            "A subarray is a consecutive series of one or more elements of the list."
        ),
        "examples": (
            "subarray_sum_count([10, 2, -2, -20, 10], -10)  # -> 3\n"
            "subarray_sum_count([1, 1, 1], 2)                # -> 2\n"
            "subarray_sum_count([1, 2, 3], 3)                # -> 2\n"
            "subarray_sum_count([0, 0, 0], 0)                # -> 6"
        ),
        "starter_code": (
            "def subarray_sum_count(numbers, target_sum):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import Counter\n\n\n"
            "# === Prefix Sum Frequency Counter (O(n)) ===\n"
            "def subarray_sum_count(numbers, target_sum):\n"
            "    prefix_sums = [0]\n"
            "    total = 0\n"
            "    for num in numbers:\n"
            "        total += num\n"
            "        prefix_sums.append(total)\n\n"
            "    seen = Counter()\n"
            "    count = 0\n"
            "    for current in prefix_sums:\n"
            "        complement = current - target_sum\n"
            "        count += seen[complement]\n"
            "        seen[current] += 1\n"
            "    return count\n\n\n"
            "# === Example Test Cases ===\n"
            "print(subarray_sum_count([10, 2, -2, -20, 10], -10))  # -> 3\n"
            "print(subarray_sum_count([1, 1, 1], 2))                # -> 2\n"
            "print(subarray_sum_count([1, 2, 3], 3))                # -> 2\n"
            "print(subarray_sum_count([0, 0, 0], 0))                # -> 6\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Maintains counts of prefix sums in a hash map. For each prefix sum, adds occurrences of (prefix_sum - target_sum) to total. Runs in O(n) time and O(n) space."
        ),
    },
    {
        "id": "merge_sort",
        "title": "110. merge sort",
        "raw_title": "merge sort",
        "category": "Array and String",
        "description": (
            "Write a function, merge_sort, that takes in a list of numbers as an argument. The function should return a new list "
            "containing elements of the original list sorted in ascending order. Your function must implement the merge sort algorithm."
        ),
        "examples": (
            "merge_sort([5, 4, 3, 2, 1])      # -> [1, 2, 3, 4, 5]\n"
            "merge_sort([10, -2, 5, 3, 8])    # -> [-2, 3, 5, 8, 10]\n"
            "merge_sort([7])                  # -> [7]\n"
            "merge_sort([])                   # -> []"
        ),
        "starter_code": (
            "def merge_sort(nums):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import deque\n\n\n"
            "# === Divide & Conquer Merge Sort (O(n log n)) ===\n"
            "def merge_sort(nums):\n"
            "    if len(nums) <= 1:\n"
            "        return nums\n"
            "    mid_idx = len(nums) // 2\n"
            "    left_sorted = merge_sort(nums[:mid_idx])\n"
            "    right_sorted = merge_sort(nums[mid_idx:])\n"
            "    return merge(left_sorted, right_sorted)\n\n\n"
            "def merge(list_1, list_2):\n"
            "    list_1 = deque(list_1)\n"
            "    list_2 = deque(list_2)\n"
            "    merged = []\n"
            "    while list_1 and list_2:\n"
            "        if list_1[0] < list_2[0]:\n"
            "            merged.append(list_1.popleft())\n"
            "        else:\n"
            "            merged.append(list_2.popleft())\n"
            "    merged += list_1\n"
            "    merged += list_2\n"
            "    return merged\n\n\n"
            "# === Example Test Cases ===\n"
            "print(merge_sort([5, 4, 3, 2, 1]))      # -> [1, 2, 3, 4, 5]\n"
            "print(merge_sort([10, -2, 5, 3, 8]))    # -> [-2, 3, 5, 8, 10]\n"
            "print(merge_sort([]))                  # -> []\n"
        ),
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n log n)",
        "complexity_explanation": (
            "Recursively divides array into halves (log n levels) and merges sorted halves in O(n) time per level. Guaranteed O(n log n) time and O(n) auxiliary space."
        ),
    },
    {
        "id": "combine_intervals",
        "title": "111. combine intervals",
        "raw_title": "combine intervals",
        "category": "Array and String",
        "description": (
            "Write a function, combine_intervals, that takes in a list of intervals as an argument. Each interval is a tuple "
            "containing a pair of numbers representing a start and end time. Your function should combine overlapping intervals "
            "and return a list containing the combined intervals.\n\n"
            "For example:\n"
            "Given two intervals: (1, 4) and (3, 7)\n"
            "The intervals overlap and should be combined into: (1, 7)\n\n"
            "You may return the combined intervals in any order.\n\n"
            "You can assume that the input list contains at least one interval and all intervals are valid with start < end."
        ),
        "examples": (
            "combine_intervals([(1, 4), (3, 7), (8, 10)])  # -> [(1, 7), (8, 10)]\n"
            "combine_intervals([(1, 5), (6, 8), (2, 4)])   # -> [(1, 5), (6, 8)]\n"
            "combine_intervals([(3, 7), (5, 8), (1, 5)])   # -> [(1, 8)]"
        ),
        "starter_code": (
            "def combine_intervals(intervals):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Sort and Linear Merge (O(n log n)) ===\n"
            "def combine_intervals(intervals):\n"
            "    sorted_intervals = sorted(intervals, key=lambda x: x[0])\n"
            "    combined = [sorted_intervals[0]]\n\n"
            "    for current_interval in sorted_intervals[1:]:\n"
            "        last_start, last_end = combined[-1]\n"
            "        current_start, current_end = current_interval\n\n"
            "        if current_start <= last_end:\n"
            "            if current_end > last_end:\n"
            "                combined[-1] = (last_start, current_end)\n"
            "        else:\n"
            "            combined.append(current_interval)\n\n"
            "    return combined\n\n\n"
            "# === Example Test Cases ===\n"
            "print(combine_intervals([(1, 4), (3, 7), (8, 10)]))  # -> [(1, 7), (8, 10)]\n"
            "print(combine_intervals([(1, 5), (6, 8), (2, 4)]))   # -> [(1, 5), (6, 8)]\n"
            "print(combine_intervals([(3, 7), (5, 8), (1, 5)]))   # -> [(1, 8)]\n"
        ),
        "time_complexity": "O(n log n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n log n)",
        "complexity_explanation": (
            "Sorts intervals by start time in O(n log n), then performs a single linear pass merging overlapping intervals. Runs in O(n log n) time and O(n) space."
        ),
    },
    {
        "id": "lexical_order",
        "title": "112. lexical order",
        "raw_title": "lexical order",
        "category": "Array and String",
        "description": (
            "Write a function, lexical_order, that takes in 2 words and an alphabet string as an argument. The function should "
            "return True if the first word should appear before the second word if lexically-ordered according to the given alphabet "
            "order. If the second word should appear first, then return False.\n\n"
            "Note that the alphabet string may be any arbitrary string.\n\n"
            "You can assume that all characters are lowercase a-z.\n\n"
            "You can assume that the alphabet contains all 26 letters."
        ),
        "examples": (
            "alphabet = 'abcdefghijklmnopqrstuvwxyz'\n"
            "lexical_order('apple', 'dock', alphabet)    # -> True\n"
            "lexical_order('apple', 'banana', alphabet)  # -> True\n"
            "lexical_order('apple', 'app', alphabet)     # -> False"
        ),
        "starter_code": (
            "def lexical_order(word_1, word_2, alphabet):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Custom Alphabet Lexical Comparison (O(max(n, m))) ===\n"
            "def lexical_order(word_1, word_2, alphabet):\n"
            "    length = max(len(word_1), len(word_2))\n"
            "    for i in range(length):\n"
            "        value_1 = alphabet.index(word_1[i]) if i < len(word_1) else float('-inf')\n"
            "        value_2 = alphabet.index(word_2[i]) if i < len(word_2) else float('-inf')\n"
            "        if value_1 < value_2:\n"
            "            return True\n"
            "        elif value_2 < value_1:\n"
            "            return False\n"
            "    return True\n\n\n"
            "# === Example Test Cases ===\n"
            "alphabet = 'abcdefghijklmnopqrstuvwxyz'\n"
            "print(lexical_order('apple', 'dock', alphabet))    # -> True\n"
            "print(lexical_order('apple', 'banana', alphabet))  # -> True\n"
            "print(lexical_order('apple', 'app', alphabet))     # -> False\n"
        ),
        "time_complexity": "O(max(n, m))",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Compares character indices against the custom alphabet up to the length of the longer word. Runs in O(max(n, m)) time and O(1) auxiliary space."
        ),
    },
    {
        "id": "detect_dictionary",
        "title": "113. detect dictionary",
        "raw_title": "detect dictionary",
        "category": "Array and String",
        "description": (
            "Write a function, detect_dictionary, that takes in a dictionary of words and an alphabet string. The function should "
            "return a boolean indicating whether or not all words of the dictionary are lexically-ordered according to the alphabet.\n\n"
            "You can assume that all characters are lowercase a-z.\n\n"
            "You can assume that the alphabet contains all 26 letters."
        ),
        "examples": (
            "alphabet = 'abcdefghijklmnopqrstuvwxyz'\n"
            "detect_dictionary(['zoo', 'tick', 'tack', 'door'], alphabet)  # -> False\n"
            "detect_dictionary(['apple', 'banana', 'cherry'], alphabet)    # -> True"
        ),
        "starter_code": (
            "def detect_dictionary(dictionary, alphabet):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Adjacent Pair Lexical Verification (O(k * m)) ===\n"
            "def lexical_order(word_1, word_2, alphabet):\n"
            "    length = max(len(word_1), len(word_2))\n"
            "    for i in range(length):\n"
            "        value_1 = alphabet.index(word_1[i]) if i < len(word_1) else float('-inf')\n"
            "        value_2 = alphabet.index(word_2[i]) if i < len(word_2) else float('-inf')\n"
            "        if value_1 < value_2:\n"
            "            return True\n"
            "        elif value_2 < value_1:\n"
            "            return False\n"
            "    return True\n\n\n"
            "def detect_dictionary(dictionary, alphabet):\n"
            "    for i in range(0, len(dictionary) - 1):\n"
            "        current = dictionary[i]\n"
            "        next_word = dictionary[i + 1]\n"
            "        if not lexical_order(current, next_word, alphabet):\n"
            "            return False\n"
            "    return True\n\n\n"
            "# === Example Test Cases ===\n"
            "alphabet = 'abcdefghijklmnopqrstuvwxyz'\n"
            "print(detect_dictionary(['zoo', 'tick', 'tack', 'door'], alphabet))  # -> False\n"
            "print(detect_dictionary(['apple', 'banana', 'cherry'], alphabet))    # -> True\n"
        ),
        "time_complexity": "O(k * m)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Compares each adjacent pair in the dictionary using the custom lexical order helper. Runs in O(k * m) time where k is number of words and m is word length, and O(1) space."
        ),
    },
    {
        "id": "linked_palindrome",
        "title": "114. linked palindrome",
        "raw_title": "linked palindrome",
        "category": "Linked List II",
        "description": (
            "Write a function, linked_palindrome, that takes in the head of a linked list as an argument. The function should "
            "return a boolean indicating whether or not the linked list is a palindrome. A palindrome is a sequence that is "
            "the same both forwards and backwards."
        ),
        "examples": (
            "a = Node(3)\n"
            "b = Node(2)\n"
            "c = Node(7)\n"
            "d = Node(2)\n"
            "e = Node(3)\n"
            "a.next = b; b.next = c; c.next = d; d.next = e\n"
            "linked_palindrome(a)  # -> True\n\n"
            "x = Node(1); y = Node(2); x.next = y\n"
            "linked_palindrome(x)  # -> False"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def linked_palindrome(head):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n\n"
            "# === Array Extraction Approach (O(n)) ===\n"
            "def linked_palindrome(head):\n"
            "    values = []\n"
            "    current = head\n"
            "    while current is not None:\n"
            "        values.append(current.val)\n"
            "        current = current.next\n"
            "    return values == values[::-1]\n\n\n"
            "# === Example Test Cases ===\n"
            "a = Node(3)\n"
            "b = Node(2)\n"
            "c = Node(7)\n"
            "d = Node(2)\n"
            "e = Node(3)\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n"
            "d.next = e\n"
            "print(linked_palindrome(a))  # -> True\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Traverses the linked list, copying node values into an array, then checks if array equals its reverse. Runs in O(n) time and O(n) space."
        ),
    },
    {
        "id": "middle_value",
        "title": "115. middle value",
        "raw_title": "middle value",
        "category": "Linked List II",
        "description": (
            "Write a function, middle_value, that takes in the head of a linked list as an argument. The function should return the "
            "value of the middle node in the linked list. If the linked list has an even number of nodes, then return the value of "
            "the second middle node.\n\n"
            "You may assume that the input list is non-empty."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "a.next = b; b.next = c; c.next = d; d.next = e\n"
            "middle_value(a)  # -> 'c'"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def middle_value(head):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n\n"
            "# === Fast & Slow Pointer (O(n) time, O(1) space) ===\n"
            "def middle_value(head):\n"
            "    slow = head\n"
            "    fast = head\n"
            "    while fast is not None and fast.next is not None:\n"
            "        slow = slow.next\n"
            "        fast = fast.next.next\n"
            "    return slow.val\n\n\n"
            "# === Example Test Cases ===\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n"
            "d.next = e\n"
            "print(middle_value(a))  # -> 'c'\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Slow pointer advances 1 step while fast pointer advances 2 steps. When fast reaches the end, slow is positioned exactly at the middle node. Runs in O(n) time and O(1) space."
        ),
    },
    {
        "id": "linked_list_cycle",
        "title": "116. linked list cycle",
        "raw_title": "linked list cycle",
        "category": "Linked List II",
        "description": (
            "Write a function, linked_list_cycle, that takes in the head of a linked list as an argument. "
            "The function should return a boolean indicating whether or not the linked list contains a cycle."
        ),
        "examples": (
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "a.next = b; b.next = c; c.next = d; d.next = b\n"
            "linked_list_cycle(a)  # -> True\n\n"
            "q = Node('q')\n"
            "r = Node('r')\n"
            "q.next = r\n"
            "linked_list_cycle(q)  # -> False"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def linked_list_cycle(head):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n\n"
            "# === Fast & Slow Pointer (O(n) time, O(1) space) ===\n"
            "def linked_list_cycle(head):\n"
            "    first_iteration = True\n"
            "    fast = head\n"
            "    slow = head\n"
            "    while fast is not None and fast.next is not None:\n"
            "        if slow is fast and not first_iteration:\n"
            "            return True\n"
            "        first_iteration = False\n"
            "        slow = slow.next\n"
            "        fast = fast.next.next\n"
            "    return False\n\n\n"
            "# === Example Test Cases ===\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "a.next = b\n"
            "b.next = c\n"
            "c.next = d\n"
            "d.next = b\n"
            "print(linked_list_cycle(a))  # -> True\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Floyd's Tortoise and Hare algorithm uses fast and slow pointers that will meet inside any cycle in O(n) time using O(1) space."
        ),
    },
    {
        "id": "undupe_sorted_linked_list",
        "title": "117. undupe sorted linked list",
        "raw_title": "undupe sorted linked list",
        "category": "Linked List II",
        "description": (
            "Write a function that takes in a linked list that contains values in increasing order. The function should return "
            "a new linked list containing the original values, with duplicates removed. The relative order of values in the resulting "
            "linked list should be unchanged.\n\n"
            "You must create and return a new set of linked list nodes and not just modify the input nodes."
        ),
        "examples": (
            "a = Node(1); b = Node(2); c = Node(2); d = Node(3)\n"
            "a.next = b; b.next = c; c.next = d\n"
            "undupe_sorted_linked_list(a)  # -> 1 -> 2 -> 3"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def undupe_sorted_linked_list(head):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n\n"
            "# === Dummy Head Single Pass (O(n)) ===\n"
            "def undupe_sorted_linked_list(head):\n"
            "    dummy_head = Node(None)\n"
            "    tail = dummy_head\n"
            "    current = head\n"
            "    while current is not None:\n"
            "        if current.val != tail.val:\n"
            "            tail.next = Node(current.val)\n"
            "            tail = tail.next\n"
            "        current = current.next\n"
            "    return dummy_head.next\n\n\n"
            "# === Example Test Cases ===\n"
            "a = Node(1); b = Node(2); c = Node(2); d = Node(3)\n"
            "a.next = b; b.next = c; c.next = d\n"
            "res = undupe_sorted_linked_list(a)\n"
            "vals = []\n"
            "while res: vals.append(res.val); res = res.next\n"
            "print(vals)  # -> [1, 2, 3]\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Traverses the sorted linked list in a single pass, appending a new node only when the value differs from the current tail. Runs in O(n) time and O(n) space."
        ),
    },
    {
        "id": "create_linked_list",
        "title": "118. create linked list",
        "raw_title": "create linked list",
        "category": "Linked List II",
        "description": (
            "Write a function, create_linked_list, that takes in a list of values as an argument. The function should create "
            "a linked list containing each item of the list as the values of the nodes. The function should return the head of the linked list."
        ),
        "examples": (
            "create_linked_list(['h', 'e', 'y'])  # -> 'h' -> 'e' -> 'y'\n"
            "create_linked_list([1, 7, 1, 8])      # -> 1 -> 7 -> 1 -> 8\n"
            "create_linked_list(['a'])             # -> 'a'\n"
            "create_linked_list([])                # -> None"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def create_linked_list(values):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n\n"
            "# === Iterative Dummy Head (O(n)) ===\n"
            "def create_linked_list(values):\n"
            "    dummy_head = Node(None)\n"
            "    tail = dummy_head\n"
            "    for val in values:\n"
            "        tail.next = Node(val)\n"
            "        tail = tail.next\n"
            "    return dummy_head.next\n\n\n"
            "# === Example Test Cases ===\n"
            "res = create_linked_list(['h', 'e', 'y'])\n"
            "vals = []\n"
            "while res: vals.append(res.val); res = res.next\n"
            "print(vals)  # -> ['h', 'e', 'y']\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Creates a chain of n linked nodes with a dummy head sentinel. Runs in O(n) time and O(n) space."
        ),
    },
    {
        "id": "build_a_queue",
        "title": "119. build a queue",
        "raw_title": "build a queue",
        "category": "Linked List II",
        "description": (
            "Implement the enqueue and dequeue methods for the existing Queue class. The enqueue method should add a given "
            "value into the queue. The dequeue should return and remove an item from the queue following first-in, first-out order.\n\n"
            "Your implementation should use a linked-list and not any built in containers."
        ),
        "examples": (
            "queue = Queue()\n"
            "queue.enqueue('a')\n"
            "queue.enqueue('b')\n"
            "queue.dequeue()  # -> 'a'\n"
            "queue.enqueue('c')\n"
            "queue.dequeue()  # -> 'b'"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "class Queue:\n"
            "  def __init__(self):\n"
            "    self.head = None\n"
            "    self.tail = None\n"
            "    self.size = 0\n\n"
            "  def enqueue(self, val):\n"
            "    pass # todo\n\n"
            "  def dequeue(self):\n"
            "    pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n\n"
            "class Queue:\n"
            "    def __init__(self):\n"
            "        self.head = None\n"
            "        self.tail = None\n"
            "        self.size = 0\n\n"
            "    def enqueue(self, val):\n"
            "        if self.size == 0:\n"
            "            self.head = Node(val)\n"
            "            self.tail = self.head\n"
            "        else:\n"
            "            self.tail.next = Node(val)\n"
            "            self.tail = self.tail.next\n"
            "        self.size += 1\n\n"
            "    def dequeue(self):\n"
            "        if self.size == 0:\n"
            "            return None\n"
            "        value = self.head.val\n"
            "        if self.size == 1:\n"
            "            self.head = None\n"
            "            self.tail = None\n"
            "        else:\n"
            "            self.head = self.head.next\n"
            "        self.size -= 1\n"
            "        return value\n\n\n"
            "# === Example Test Cases ===\n"
            "q = Queue()\n"
            "q.enqueue('a')\n"
            "q.enqueue('b')\n"
            "print(q.dequeue())  # -> 'a'\n"
            "print(q.dequeue())  # -> 'b'\n"
            "print(q.dequeue())  # -> None\n"
        ),
        "time_complexity": "O(1)",
        "space_complexity": "O(n)",
        "complexity_type": "O(1)",
        "complexity_explanation": (
            "Enqueue appends to tail in O(1) time and dequeue extracts from head in O(1) time. Space complexity is O(n) for n elements."
        ),
    },
    {
        "id": "add_lists",
        "title": "120. add lists",
        "raw_title": "add lists",
        "category": "Linked List II",
        "description": (
            "Write a function, add_lists, that takes in the head of two linked lists, each representing a number. The nodes of the "
            "linked lists contain digits as values. The nodes in the input lists are reversed; this means that the least significant "
            "digit of the number is the head. The function should return the head of a new linked listed representing the sum of the "
            "input lists. The output list should have its digits reversed as well.\n\n"
            "You must do this by traversing through the linked lists once."
        ),
        "examples": (
            "#  621\n"
            "#+ 354\n"
            "# -----\n"
            "#  975\n"
            "a1 = Node(1); a2 = Node(2); a3 = Node(6); a1.next = a2; a2.next = a3\n"
            "b1 = Node(4); b2 = Node(5); b3 = Node(3); b1.next = b2; b2.next = b3\n"
            "add_lists(a1, b1) # -> 5 -> 7 -> 9"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.next = None\n\n"
            "def add_lists(head_1, head_2):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.next = None\n\n\n"
            "# === Single-Pass Ripple Addition (O(max(n, m))) ===\n"
            "def add_lists(head_1, head_2):\n"
            "    dummy_head = Node(None)\n"
            "    tail = dummy_head\n"
            "    carry = 0\n"
            "    current_1 = head_1\n"
            "    current_2 = head_2\n"
            "    while current_1 is not None or current_2 is not None or carry == 1:\n"
            "        val_1 = 0 if current_1 is None else current_1.val\n"
            "        val_2 = 0 if current_2 is None else current_2.val\n"
            "        total = val_1 + val_2 + carry\n"
            "        carry = 1 if total > 9 else 0\n"
            "        digit = total % 10\n"
            "        tail.next = Node(digit)\n"
            "        tail = tail.next\n"
            "        if current_1 is not None:\n"
            "            current_1 = current_1.next\n"
            "        if current_2 is not None:\n"
            "            current_2 = current_2.next\n"
            "    return dummy_head.next\n\n\n"
            "# === Example Test Cases ===\n"
            "a1 = Node(1); a2 = Node(2); a3 = Node(6); a1.next = a2; a2.next = a3\n"
            "b1 = Node(4); b2 = Node(5); b3 = Node(3); b1.next = b2; b2.next = b3\n"
            "res = add_lists(a1, b1)\n"
            "vals = []\n"
            "while res: vals.append(res.val); res = res.next\n"
            "print(vals)  # -> [5, 7, 9]\n"
        ),
        "time_complexity": "O(max(n, m))",
        "space_complexity": "O(max(n, m))",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Performs single-pass addition digit-by-digit with carry propagation. Runs in O(max(n, m)) time and O(max(n, m)) space."
        ),
    },
    {
        "id": "lowest_common_ancestor",
        "title": "121. lowest common ancestor",
        "raw_title": "lowest common ancestor",
        "category": "Binary Tree II",
        "description": (
            "Write a function, lowest_common_ancestor, that takes in the root of a binary tree and two values. The function should "
            "return the value of the lowest common ancestor of the two values in the tree.\n\n"
            "You may assume that the tree values are unique and the tree is non-empty.\n\n"
            "Note that a node may be considered an ancestor of itself."
        ),
        "examples": (
            "a = Node('a'); b = Node('b'); c = Node('c')\n"
            "a.left = b; a.right = c\n"
            "lowest_common_ancestor(a, 'b', 'c')  # -> 'a'"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def lowest_common_ancestor(root, val1, val2):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n\n"
            "# === Depth First Path Comparison (O(n)) ===\n"
            "def find_path(root, target_val):\n"
            "    if root is None:\n"
            "        return None\n"
            "    if root.val == target_val:\n"
            "        return [root.val]\n"
            "    left_path = find_path(root.left, target_val)\n"
            "    if left_path is not None:\n"
            "        left_path.append(root.val)\n"
            "        return left_path\n"
            "    right_path = find_path(root.right, target_val)\n"
            "    if right_path is not None:\n"
            "        right_path.append(root.val)\n"
            "        return right_path\n"
            "    return None\n\n\n"
            "def lowest_common_ancestor(root, val1, val2):\n"
            "    path1 = find_path(root, val1)\n"
            "    path2 = find_path(root, val2)\n"
            "    set2 = set(path2)\n"
            "    for val in path1:\n"
            "        if val in set2:\n"
            "            return val\n\n\n"
            "# === Example Test Cases ===\n"
            "a = Node('a'); b = Node('b'); c = Node('c')\n"
            "a.left = b; a.right = c\n"
            "print(lowest_common_ancestor(a, 'b', 'c'))  # -> 'a'\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Traces the paths from root to both target values in O(n) time, then finds their deepest common intersection node. Runs in O(n) time and O(n) space."
        ),
    },
    {
        "id": "flip_tree",
        "title": "122. flip tree",
        "raw_title": "flip tree",
        "category": "Binary Tree II",
        "description": (
            "Write a function, flip_tree, that takes in the root of a binary tree. The function should flip the binary tree, "
            "turning left subtrees into right subtrees and vice-versa. This flipping should occur in-place by modifying the original tree. "
            "The function should return the root of the tree."
        ),
        "examples": (
            "a = Node('a'); b = Node('b'); c = Node('c')\n"
            "a.left = b; a.right = c\n"
            "flip_tree(a)  # a.left becomes c, a.right becomes b"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def flip_tree(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n\n"
            "# === In-Place Recursive Inversion (O(n)) ===\n"
            "def flip_tree(root):\n"
            "    if root is None:\n"
            "        return None\n"
            "    left = flip_tree(root.left)\n"
            "    right = flip_tree(root.right)\n"
            "    root.left = right\n"
            "    root.right = left\n"
            "    return root\n\n\n"
            "# === Example Test Cases ===\n"
            "a = Node('a'); b = Node('b'); c = Node('c')\n"
            "a.left = b; a.right = c\n"
            "flip_tree(a)\n"
            "print(a.left.val, a.right.val)  # -> 'c' 'b'\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(h)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Recursively inverts the left and right pointers of every node in-place. Visits each of the n nodes once, running in O(n) time and O(h) call-stack space where h is tree height."
        ),
    },
    {
        "id": "lefty_nodes",
        "title": "123. lefty nodes",
        "raw_title": "lefty nodes",
        "category": "Binary Tree II",
        "description": (
            "Write a function, lefty_nodes, that takes in the root of a binary tree. The function should return a list containing "
            "the left-most value on every level of the tree. The list must be ordered in a top-down fashion where the root is the first item.\n\n"
            "Note that the left-most node on a level may not necessarily be a left child."
        ),
        "examples": (
            "a = Node('a'); b = Node('b'); c = Node('c')\n"
            "a.left = b; a.right = c\n"
            "lefty_nodes(a)  # -> ['a', 'b']"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def lefty_nodes(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n\n"
            "# === Depth-First Level Traversal (O(n)) ===\n"
            "def lefty_nodes(root):\n"
            "    values = []\n"
            "    def traverse(node, level):\n"
            "        if node is None:\n"
            "            return\n"
            "        if len(values) == level:\n"
            "            values.append(node.val)\n"
            "        traverse(node.left, level + 1)\n"
            "        traverse(node.right, level + 1)\n"
            "    traverse(root, 0)\n"
            "    return values\n\n\n"
            "# === Example Test Cases ===\n"
            "a = Node('a'); b = Node('b'); c = Node('c')\n"
            "a.left = b; a.right = c\n"
            "print(lefty_nodes(a))  # -> ['a', 'b']\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(h)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Visits nodes left-to-right on each depth level. Appends the first encountered node at each level depth, running in O(n) time and O(h) space."
        ),
    },
    {
        "id": "binary_search_tree_includes",
        "title": "124. binary search tree includes",
        "raw_title": "binary search tree includes",
        "category": "Binary Tree II",
        "description": (
            "Write a function, binary_search_tree_includes, that takes in the root of a binary search tree containing numbers and a "
            "target value. The function should return a boolean indicating whether or not the target is found within the tree.\n\n"
            "A binary search tree is a binary tree where all values within a node's left subtree are smaller than the node's value and all "
            "values in a node's right subtree are greater than or equal to the node's value.\n\n"
            "Your solution should have a best case runtime of O(log(n))."
        ),
        "examples": (
            "a = Node(12); b = Node(5); c = Node(18)\n"
            "a.left = b; a.right = c\n"
            "binary_search_tree_includes(a, 5)   # -> True\n"
            "binary_search_tree_includes(a, 15)  # -> False"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def binary_search_tree_includes(root, target):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n\n"
            "# === Iterative BST Search (O(h)) ===\n"
            "def binary_search_tree_includes(root, target):\n"
            "    current = root\n"
            "    while current is not None:\n"
            "        if target > current.val:\n"
            "            current = current.right\n"
            "        elif target < current.val:\n"
            "            current = current.left\n"
            "        else:\n"
            "            return True\n"
            "    return False\n\n\n"
            "# === Example Test Cases ===\n"
            "a = Node(12); b = Node(5); c = Node(18)\n"
            "a.left = b; a.right = c\n"
            "print(binary_search_tree_includes(a, 5))   # -> True\n"
            "print(binary_search_tree_includes(a, 15))  # -> False\n"
        ),
        "time_complexity": "O(h)",
        "space_complexity": "O(1)",
        "complexity_type": "O(log n)",
        "complexity_explanation": (
            "Leverages the binary search tree property to eliminate half the remaining nodes at each step. Runs in O(h) time (O(log n) for balanced BST) and O(1) space."
        ),
    },
    {
        "id": "is_binary_search_tree",
        "title": "125. is binary search tree",
        "raw_title": "is binary search tree",
        "category": "Binary Tree II",
        "description": (
            "Write a function, is_binary_search_tree, that takes in the root of a binary tree. The function should return a boolean "
            "indicating whether or not the tree satisfies the binary search tree property.\n\n"
            "A binary tree where all values within a node's left subtree are smaller than the node's value and all values in a node's "
            "right subtree are greater than the node's value."
        ),
        "examples": (
            "a = Node(12); b = Node(5); c = Node(18)\n"
            "a.left = b; a.right = c\n"
            "is_binary_search_tree(a)  # -> True\n\n"
            "x = Node(12); y = Node(20); z = Node(18)\n"
            "x.left = y; x.right = z\n"
            "is_binary_search_tree(x)  # -> False"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def is_binary_search_tree(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n\n"
            "# === In-Order Traversal Monotonicity Check (O(n)) ===\n"
            "def is_binary_search_tree(root):\n"
            "    values = []\n"
            "    def in_order_traversal(n):\n"
            "        if n is None:\n"
            "            return\n"
            "        in_order_traversal(n.left)\n"
            "        values.append(n.val)\n"
            "        in_order_traversal(n.right)\n"
            "    in_order_traversal(root)\n"
            "    for i in range(len(values) - 1):\n"
            "        if values[i + 1] <= values[i]:\n"
            "            return False\n"
            "    return True\n\n\n"
            "# === Example Test Cases ===\n"
            "a = Node(12); b = Node(5); c = Node(18)\n"
            "a.left = b; a.right = c\n"
            "print(is_binary_search_tree(a))  # -> True\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "An in-order traversal of a valid BST yields strictly increasing values. Checking monotonic order runs in O(n) time and O(n) space."
        ),
    },
    {
        "id": "post_order",
        "title": "126. post order",
        "raw_title": "post order",
        "category": "Binary Tree II",
        "description": (
            "Write a function, post_order, that takes in the root of a binary tree. The function should return a list containing the "
            "post-ordered values of the tree.\n\n"
            "Post-order traversal is when nodes are recursively visited in the order: left child, right child, self."
        ),
        "examples": (
            "a = Node('a'); b = Node('b'); c = Node('c')\n"
            "a.left = b; a.right = c\n"
            "post_order(a)  # -> ['b', 'c', 'a']"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def post_order(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n\n"
            "# === Recursive Post-Order (O(n)) ===\n"
            "def post_order(root):\n"
            "    values = []\n"
            "    def post_order_traversal(n):\n"
            "        if n is None:\n"
            "            return\n"
            "        post_order_traversal(n.left)\n"
            "        post_order_traversal(n.right)\n"
            "        values.append(n.val)\n"
            "    post_order_traversal(root)\n"
            "    return values\n\n\n"
            "# === Example Test Cases ===\n"
            "a = Node('a'); b = Node('b'); c = Node('c')\n"
            "a.left = b; a.right = c\n"
            "print(post_order(a))  # -> ['b', 'c', 'a']\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Visits left subtree, right subtree, then current node. Each node is processed once in O(n) time and O(n) space."
        ),
    },
    {
        "id": "build_tree_in_post",
        "title": "127. build tree in post",
        "raw_title": "build tree in post",
        "category": "Binary Tree II",
        "description": (
            "Write a function, build_tree_in_post, that takes in a list of in-ordered values and a list of post-ordered values for a "
            "binary tree. The function should build a binary tree that has the given in-order and post-order traversal structure. "
            "The function should return the root of this tree.\n\n"
            "You can assume that the values of inorder and postorder are unique."
        ),
        "examples": (
            "build_tree_in_post(['y', 'x', 'z'], ['y', 'z', 'x'])  # root 'x', left 'y', right 'z'"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def build_tree_in_post(in_order, post_order):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n\n"
            "# === Recursive In-Order & Post-Order Reconstruction (O(n)) ===\n"
            "def build_tree_in_post(in_order, post_order):\n"
            "    if len(in_order) == 0:\n"
            "        return None\n"
            "    value = post_order[-1]\n"
            "    root = Node(value)\n"
            "    mid = in_order.index(value)\n"
            "    left_in = in_order[:mid]\n"
            "    right_in = in_order[mid + 1:]\n"
            "    left_post = post_order[:len(left_in)]\n"
            "    right_post = post_order[len(left_in):-1]\n"
            "    root.left = build_tree_in_post(left_in, left_post)\n"
            "    root.right = build_tree_in_post(right_in, right_post)\n"
            "    return root\n\n\n"
            "# === Example Test Cases ===\n"
            "root = build_tree_in_post(['y', 'x', 'z'], ['y', 'z', 'x'])\n"
            "print(root.val, root.left.val, root.right.val)  # -> 'x' 'y' 'z'\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "The last element of post_order is the subtree root. Slicing in_order around that root divides into left and right subtrees. Runs in O(n) time and O(n) space."
        ),
    },
    {
        "id": "build_tree_in_pre",
        "title": "128. build tree in pre",
        "raw_title": "build tree in pre",
        "category": "Binary Tree II",
        "description": (
            "Write a function, build_tree_in_pre, that takes in a list of in-ordered values and a list of pre-ordered values for a "
            "binary tree. The function should build a binary tree that has the given in-order and pre-order traversal structure. "
            "The function should return the root of this tree.\n\n"
            "You can assume that the values of inorder and preorder are unique."
        ),
        "examples": (
            "build_tree_in_pre(['z', 'y', 'x'], ['y', 'z', 'x'])  # root 'y', left 'z', right 'x'"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def build_tree_in_pre(in_order, pre_order):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n\n"
            "# === Hash Map Indexed Reconstruction (O(n)) ===\n"
            "def build_tree_in_pre(in_order, pre_order):\n"
            "    in_order_index = {ele: i for i, ele in enumerate(in_order)}\n"
            "    def _build(in_start, in_end, pre_start, pre_end):\n"
            "        if in_end < in_start:\n"
            "            return None\n"
            "        value = pre_order[pre_start]\n"
            "        root = Node(value)\n"
            "        mid = in_order_index[value]\n"
            "        left_size = mid - in_start\n"
            "        root.left = _build(in_start, mid - 1, pre_start + 1, pre_start + left_size)\n"
            "        root.right = _build(mid + 1, in_end, pre_start + left_size + 1, pre_end)\n"
            "        return root\n"
            "    return _build(0, len(in_order) - 1, 0, len(pre_order) - 1)\n\n\n"
            "# === Example Test Cases ===\n"
            "root = build_tree_in_pre(['z', 'y', 'x'], ['y', 'z', 'x'])\n"
            "print(root.val, root.left.val, root.right.val)  # -> 'y' 'z' 'x'\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Pre-indexes in_order positions with a hash map to achieve O(1) split index lookups. Constructs the tree in O(n) time and O(n) space."
        ),
    },
    {
        "id": "is_tree_balanced",
        "title": "129. is tree balanced",
        "raw_title": "is tree balanced",
        "category": "Binary Tree II",
        "description": (
            "Write a function, is_tree_balanced, that takes in the root of a binary tree. The function should return a boolean "
            "indicating whether or not the tree is 'balanced'.\n\n"
            "A 'balanced' binary tree is a binary tree where the height between the left and right subtrees differs by at most 1 for every node."
        ),
        "examples": (
            "a = Node('a'); b = Node('b'); c = Node('c')\n"
            "a.left = b; a.right = c\n"
            "is_tree_balanced(a)  # -> True"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def is_tree_balanced(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n\n"
            "# === Bottom-Up Height Balance (O(n)) ===\n"
            "def check_height_balance(root):\n"
            "    if root is None:\n"
            "        return 0\n"
            "    left_height = check_height_balance(root.left)\n"
            "    if left_height == -1:\n"
            "        return -1\n"
            "    right_height = check_height_balance(root.right)\n"
            "    if right_height == -1:\n"
            "        return -1\n"
            "    if abs(left_height - right_height) > 1:\n"
            "        return -1\n"
            "    return 1 + max(left_height, right_height)\n\n\n"
            "def is_tree_balanced(root):\n"
            "    return check_height_balance(root) > -1\n\n\n"
            "# === Example Test Cases ===\n"
            "a = Node('a'); b = Node('b'); c = Node('c')\n"
            "a.left = b; a.right = c\n"
            "print(is_tree_balanced(a))  # -> True\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(h)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Computes subtree height bottom-up, short-circuiting with -1 immediately upon detecting any unbalanced node. Runs in O(n) time and O(h) space."
        ),
    },
    {
        "id": "heap_insertion",
        "title": "130. heap insertion",
        "raw_title": "heap insertion",
        "category": "Heap",
        "description": (
            "Implement the insert method for the MinHeap class. The method should properly add a given value into the heap, "
            "maintaining min heap order and height balance using sift-up."
        ),
        "examples": (
            "heap = MinHeap()\n"
            "heap.insert(10)\n"
            "heap.insert(5)\n"
            "heap.insert(15)\n"
            "heap.list[0]  # -> 5"
        ),
        "starter_code": (
            "class MinHeap:\n"
            "  def __init__(self):\n"
            "    self.list = []\n\n"
            "  def is_empty(self):\n"
            "    return len(self.list) == 0\n\n"
            "  def size(self):\n"
            "    return len(self.list)\n\n"
            "  def insert(self, val):\n"
            "    pass # todo\n"
        ),
        "solution_code": (
            "class MinHeap:\n"
            "    def __init__(self):\n"
            "        self.list = []\n\n"
            "    def is_empty(self):\n"
            "        return len(self.list) == 0\n\n"
            "    def size(self):\n"
            "        return len(self.list)\n\n"
            "    def swap(self, index_1, index_2):\n"
            "        self.list[index_1], self.list[index_2] = self.list[index_2], self.list[index_1]\n\n"
            "    def sift_up(self, index):\n"
            "        current_index = index\n"
            "        while current_index > 0:\n"
            "            parent_index = (current_index - 1) // 2\n"
            "            if self.list[current_index] < self.list[parent_index]:\n"
            "                self.swap(current_index, parent_index)\n"
            "                current_index = parent_index\n"
            "            else:\n"
            "                break\n\n"
            "    def insert(self, val):\n"
            "        self.list.append(val)\n"
            "        self.sift_up(self.size() - 1)\n\n\n"
            "# === Example Test Cases ===\n"
            "heap = MinHeap()\n"
            "heap.insert(10)\n"
            "heap.insert(5)\n"
            "heap.insert(15)\n"
            "print(heap.list)  # -> [5, 10, 15]\n"
        ),
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(log n)",
        "complexity_explanation": (
            "Appends new element to list tail and restores heap invariant via sift_up along tree height. Runs in O(log n) time and O(1) auxiliary space."
        ),
    },
    {
        "id": "heap_deletion",
        "title": "131. heap deletion",
        "raw_title": "heap deletion",
        "category": "Heap",
        "description": (
            "Implement the extract_min method for the MinHeap class. The method should return and remove the smallest value in the heap, "
            "maintaining min heap order and height balance using sift-down."
        ),
        "examples": (
            "heap = MinHeap()\n"
            "heap.insert(10); heap.insert(5); heap.insert(15)\n"
            "heap.extract_min()  # -> 5\n"
            "heap.extract_min()  # -> 10\n"
            "heap.extract_min()  # -> 15"
        ),
        "starter_code": (
            "class MinHeap:\n"
            "  def __init__(self):\n"
            "    self.list = []\n\n"
            "  def is_empty(self):\n"
            "    return len(self.list) == 0\n\n"
            "  def size(self):\n"
            "    return len(self.list)\n\n"
            "  def extract_min(self):\n"
            "    pass # todo\n"
        ),
        "solution_code": (
            "class MinHeap:\n"
            "    def __init__(self):\n"
            "        self.list = []\n\n"
            "    def is_empty(self):\n"
            "        return len(self.list) == 0\n\n"
            "    def size(self):\n"
            "        return len(self.list)\n\n"
            "    def swap(self, index_1, index_2):\n"
            "        self.list[index_1], self.list[index_2] = self.list[index_2], self.list[index_1]\n\n"
            "    def sift_up(self, index):\n"
            "        current_index = index\n"
            "        while current_index > 0:\n"
            "            parent_index = (current_index - 1) // 2\n"
            "            if self.list[current_index] < self.list[parent_index]:\n"
            "                self.swap(current_index, parent_index)\n"
            "                current_index = parent_index\n"
            "            else:\n"
            "                break\n\n"
            "    def insert(self, val):\n"
            "        self.list.append(val)\n"
            "        self.sift_up(self.size() - 1)\n\n"
            "    def sift_down(self, index):\n"
            "        current_index = index\n"
            "        while current_index < self.size() - 1:\n"
            "            left_child_index = current_index * 2 + 1\n"
            "            right_child_index = current_index * 2 + 2\n"
            "            left_child_val = float('inf') if left_child_index >= self.size() else self.list[left_child_index]\n"
            "            right_child_val = float('inf') if right_child_index >= self.size() else self.list[right_child_index]\n"
            "            smaller_child_val = min(left_child_val, right_child_val)\n"
            "            smaller_child_index = left_child_index if left_child_val < right_child_val else right_child_index\n"
            "            if self.list[current_index] > smaller_child_val:\n"
            "                self.swap(current_index, smaller_child_index)\n"
            "                current_index = smaller_child_index\n"
            "            else:\n"
            "                break\n\n"
            "    def extract_min(self):\n"
            "        if self.is_empty():\n"
            "            return None\n"
            "        if self.size() == 1:\n"
            "            return self.list.pop()\n"
            "        min_val = self.list[0]\n"
            "        self.list[0] = self.list.pop()\n"
            "        self.sift_down(0)\n"
            "        return min_val\n\n\n"
            "# === Example Test Cases ===\n"
            "heap = MinHeap()\n"
            "heap.insert(10); heap.insert(5); heap.insert(15)\n"
            "print(heap.extract_min())  # -> 5\n"
            "print(heap.extract_min())  # -> 10\n"
            "print(heap.extract_min())  # -> 15\n"
        ),
        "time_complexity": "O(log n)",
        "space_complexity": "O(1)",
        "complexity_type": "O(log n)",
        "complexity_explanation": (
            "Swaps root with last element and restores heap invariant using sift_down down tree height. Runs in O(log n) time and O(1) space."
        ),
    },
    {
        "id": "kth_largest",
        "title": "132. kth largest",
        "raw_title": "kth largest",
        "category": "Heap",
        "description": (
            "Write a function, kth_largest, that takes in a list of numbers and a value, k. "
            "The function should return the k-th largest element of the list."
        ),
        "examples": (
            "kth_largest([3, 2, 1, 5, 6, 4], 2)              # -> 5\n"
            "kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4)     # -> 4\n"
            "kth_largest([12, 10, 8, 7, 5, 2], 1)            # -> 12"
        ),
        "starter_code": (
            "def kth_largest(numbers, k):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "import heapq\n\n\n"
            "# === Approach 1: Using Sort (O(n log n)) ===\n"
            "def kth_largest(numbers, k):\n"
            "    sorted_numbers = sorted(numbers)\n"
            "    return sorted_numbers[-k]\n\n\n"
            "# === Approach 2: Using Custom MinHeap (O(n log k)) ===\n"
            "class MinHeap:\n"
            "    def __init__(self):\n"
            "        self.list = []\n\n"
            "    def is_empty(self):\n"
            "        return len(self.list) == 0\n\n"
            "    def size(self):\n"
            "        return len(self.list)\n\n"
            "    def swap(self, index_1, index_2):\n"
            "        self.list[index_1], self.list[index_2] = self.list[index_2], self.list[index_1]\n\n"
            "    def sift_up(self, index):\n"
            "        current_index = index\n"
            "        while current_index > 0:\n"
            "            parent_index = (current_index - 1) // 2\n"
            "            if self.list[current_index] < self.list[parent_index]:\n"
            "                self.swap(current_index, parent_index)\n"
            "                current_index = parent_index\n"
            "            else:\n"
            "                break\n\n"
            "    def insert(self, val):\n"
            "        self.list.append(val)\n"
            "        self.sift_up(self.size() - 1)\n\n"
            "    def sift_down(self, index):\n"
            "        current_index = index\n"
            "        while current_index < self.size() - 1:\n"
            "            left_child_index = current_index * 2 + 1\n"
            "            right_child_index = current_index * 2 + 2\n\n"
            "            left_child_val = float('inf') if left_child_index >= self.size() else self.list[left_child_index]\n"
            "            right_child_val = float('inf') if right_child_index >= self.size() else self.list[right_child_index]\n\n"
            "            smaller_child_val = left_child_val if left_child_val < right_child_val else right_child_val\n"
            "            smaller_child_index = left_child_index if left_child_val < right_child_val else right_child_index\n\n"
            "            if self.list[current_index] > smaller_child_val:\n"
            "                self.swap(current_index, smaller_child_index)\n"
            "                current_index = smaller_child_index\n"
            "            else:\n"
            "                break\n\n"
            "    def extract_min(self):\n"
            "        if self.is_empty():\n"
            "            return None\n"
            "        if self.size() == 1:\n"
            "            return self.list.pop()\n"
            "        min_val = self.list[0]\n"
            "        self.list[0] = self.list.pop()\n"
            "        self.sift_down(0)\n"
            "        return min_val\n\n"
            "def kth_largest_heap(numbers, k):\n"
            "    heap = MinHeap()\n"
            "    for num in numbers:\n"
            "        heap.insert(num)\n"
            "        if heap.size() > k:\n"
            "            heap.extract_min()\n"
            "    return heap.extract_min()\n\n\n"
            "# === Approach 3: Using Built-in heapq (O(n log k)) ===\n"
            "def kth_largest_builtin(numbers, k):\n"
            "    heap = []\n"
            "    for num in numbers:\n"
            "        heapq.heappush(heap, num)\n"
            "        if len(heap) > k:\n"
            "            heapq.heappop(heap)\n"
            "    return heapq.heappop(heap)\n\n\n"
            "# === Example Test Cases ===\n"
            "print(kth_largest([3, 2, 1, 5, 6, 4], 2))           # -> 5\n"
            "print(kth_largest([3, 2, 3, 1, 2, 4, 5, 5, 6], 4))  # -> 4\n"
            "print(kth_largest_heap([3, 2, 1, 5, 6, 4], 2))      # -> 5\n"
            "print(kth_largest_builtin([3, 2, 1, 5, 6, 4], 2))   # -> 5\n"
        ),
        "time_complexity": "O(n log k)",
        "space_complexity": "O(k)",
        "complexity_type": "O(log n)",
        "complexity_explanation": (
            "Maintains a min-heap bounded at k elements while scanning the list of n numbers. Runs in O(n log k) time and O(k) space."
        ),
    },
    {
        "id": "k_smallest",
        "title": "133. k smallest",
        "raw_title": "k smallest",
        "category": "Heap",
        "description": (
            "Write a function that takes in a list of numbers and a value, k. The function should return the k smallest "
            "numbers in the list. The resulting list should be ordered from least to greatest."
        ),
        "examples": (
            "k_smallest([3, 2, 1, 5, 6, 4], 3)          # -> [1, 2, 3]\n"
            "k_smallest([7, 10, 4, 3, 20, 15], 3)       # -> [3, 4, 7]\n"
            "k_smallest([2, 5, 9, 11, 4, 2, 1, 8], 2)   # -> [1, 2]"
        ),
        "starter_code": (
            "def k_smallest(nums, k):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "import heapq\n\n\n"
            "# === Approach 1: Using Sort (O(n log n)) ===\n"
            "def k_smallest(nums, k):\n"
            "    sorted_nums = sorted(nums)\n"
            "    return sorted_nums[:k]\n\n\n"
            "# === Approach 2: Using Max-Heap with heapq (O(n log k)) ===\n"
            "def k_smallest_heap(nums, k):\n"
            "    max_heap = []\n"
            "    for v in nums:\n"
            "        item = (-v, v)\n"
            "        heapq.heappush(max_heap, item)\n"
            "        if len(max_heap) > k:\n"
            "            heapq.heappop(max_heap)\n\n"
            "    result = []\n"
            "    while len(max_heap) > 0:\n"
            "        item = heapq.heappop(max_heap)\n"
            "        result.append(item[1])\n\n"
            "    return result[::-1]\n\n\n"
            "# === Example Test Cases ===\n"
            "print(k_smallest([3, 2, 1, 5, 6, 4], 3))          # -> [1, 2, 3]\n"
            "print(k_smallest([7, 10, 4, 3, 20, 15], 3))       # -> [3, 4, 7]\n"
            "print(k_smallest_heap([3, 2, 1, 5, 6, 4], 3))     # -> [1, 2, 3]\n"
        ),
        "time_complexity": "O(n log k)",
        "space_complexity": "O(k)",
        "complexity_type": "O(log n)",
        "complexity_explanation": (
            "Uses a max-heap of capacity k to track the k smallest values seen so far. Runs in O(n log k) time and O(k) space."
        ),
    },
    {
        "id": "subsets",
        "title": "134. subsets",
        "raw_title": "subsets",
        "category": "Exhaustive Recursion",
        "description": (
            "Write a function, subsets, that takes in a list as an argument. The function should return a 2D list where each "
            "sublist represents one of the possible subsets of the list.\n\n"
            "The elements within the subsets and the subsets themselves may be returned in any order.\n\n"
            "You may assume that the input list contains unique elements."
        ),
        "examples": (
            "subsets(['a', 'b'])          # -> [[], ['b'], ['a'], ['a', 'b']]\n"
            "subsets(['a', 'b', 'c'])     # -> 8 subsets\n"
            "subsets([])                  # -> [[]]"
        ),
        "starter_code": (
            "def subsets(elements):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Exhaustive Recursive Power Set (O(2^n)) ===\n"
            "def subsets(elements):\n"
            "    if not elements:\n"
            "        return [[]]\n"
            "    first = elements[0]\n"
            "    remaining_elements = elements[1:]\n"
            "    subsets_without_first = subsets(remaining_elements)\n\n"
            "    subsets_with_first = []\n"
            "    for sub in subsets_without_first:\n"
            "        subsets_with_first.append([first, *sub])\n\n"
            "    return subsets_without_first + subsets_with_first\n\n\n"
            "# === Example Test Cases ===\n"
            "print(subsets(['a', 'b']))          # -> [[], ['b'], ['a'], ['a', 'b']]\n"
            "print(len(subsets(['a', 'b', 'c']))) # -> 8\n"
        ),
        "time_complexity": "O(2^n)",
        "space_complexity": "O(2^n)",
        "complexity_type": "O(2^n)",
        "complexity_explanation": (
            "Generates all 2^n subsets by branching on whether each element is included or excluded. Runs in O(2^n) time and O(2^n) space."
        ),
    },
    {
        "id": "permutations",
        "title": "135. permutations",
        "raw_title": "permutations",
        "category": "Exhaustive Recursion",
        "description": (
            "Write a function, permutations, that takes in a list an argument. The function should return a 2D list where each "
            "sublist represents one of the possible permutations of the list.\n\n"
            "The sublists may be returned in any order.\n\n"
            "You may assume that the input list contains unique items."
        ),
        "examples": (
            "permutations(['a', 'b', 'c'])  # -> 6 permutations\n"
            "permutations(['red', 'blue'])  # -> [['red', 'blue'], ['blue', 'red']]\n"
            "permutations([])               # -> [[]]"
        ),
        "starter_code": (
            "def permutations(items):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Exhaustive Recursive Permutations (O(n!)) ===\n"
            "def permutations(items):\n"
            "    if not items:\n"
            "        return [[]]\n"
            "    first = items[0]\n"
            "    remaining = items[1:]\n"
            "    perms = permutations(remaining)\n"
            "    result = []\n"
            "    for perm in perms:\n"
            "        for i in range(len(perm) + 1):\n"
            "            result.append([*perm[:i], first, *perm[i:]])\n"
            "    return result\n\n\n"
            "# === Example Test Cases ===\n"
            "print(permutations(['red', 'blue']))  # -> [['red', 'blue'], ['blue', 'red']]\n"
            "print(len(permutations(['a', 'b', 'c']))) # -> 6\n"
        ),
        "time_complexity": "O(n!)",
        "space_complexity": "O(n!)",
        "complexity_type": "O(2^n)",
        "complexity_explanation": (
            "Constructs all n! orderings by inserting each item into every possible index position of sub-permutations. Runs in O(n!) time and O(n!) space."
        ),
    },
    {
        "id": "create_combinations",
        "title": "136. create combinations",
        "raw_title": "create combinations",
        "category": "Exhaustive Recursion",
        "description": (
            "Write a function, create_combinations, that takes in a list and a length as arguments. "
            "The function should return a 2D list representing all of the combinations of the specified length.\n\n"
            "The items within the combinations and the combinations themselves may be returned in any order.\n\n"
            "You may assume that the input list contains unique elements and 1 <= k <= len(items)."
        ),
        "examples": (
            "create_combinations(['a', 'b', 'c'], 2)   # -> [['a', 'b'], ['a', 'c'], ['b', 'c']]\n"
            "create_combinations(['q', 'r', 's', 't'], 2) # -> 6 combinations\n"
            "create_combinations(['q', 'r', 's', 't'], 3) # -> 4 combinations\n"
            "create_combinations([1, 28, 94], 3)         # -> [[1, 28, 94]]"
        ),
        "starter_code": (
            "def create_combinations(items, k):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Exhaustive Recursive Combinations (O(C(n, k))) ===\n"
            "def create_combinations(items, k):\n"
            "    if len(items) < k:\n"
            "        return []\n\n"
            "    if k == 0:\n"
            "        return [[]]\n\n"
            "    first = items[0]\n"
            "    combos_with_first = []\n"
            "    for combo in create_combinations(items[1:], k - 1):\n"
            "        combos_with_first.append([first, *combo])\n\n"
            "    combos_without_first = create_combinations(items[1:], k)\n"
            "    return combos_with_first + combos_without_first\n\n\n"
            "# === Example Test Cases ===\n"
            "print(create_combinations(['a', 'b', 'c'], 2))   # -> [['a', 'b'], ['a', 'c'], ['b', 'c']]\n"
            "print(len(create_combinations(['q', 'r', 's', 't'], 2))) # -> 6\n"
            "print(create_combinations([1, 28, 94], 3))         # -> [[1, 28, 94]]\n"
        ),
        "time_complexity": "O(C(n, k))",
        "space_complexity": "O(C(n, k))",
        "complexity_type": "O(2^n)",
        "complexity_explanation": (
            "Generates all n choose k combinations recursively by choosing whether to include each item. Runs in O(C(n, k)) time and O(C(n, k)) space."
        ),
    },
    {
        "id": "grocery_budget",
        "title": "137. grocery budget",
        "raw_title": "grocery budget",
        "category": "Exhaustive Recursion",
        "description": (
            "Write a function, grocery_budget, that takes in grocery_list and a number budget. "
            "Every item in grocery_list is a pair containing the item name and price. "
            "Your function should return all possible ways to purchase items without spending more than the given budget.\n\n"
            "The order of the items in the return value does not matter.\n\n"
            "You cannot purchase an item more than once. You do not have to spend the budget fully."
        ),
        "examples": (
            "items = [('eggs', 3), ('bread', 2), ('milk', 4), ('cheese', 6)]\n"
            "grocery_budget(items, 5) # -> [['bread', 'eggs'], ['eggs'], ['bread'], ['milk'], []]\n"
            "grocery_budget([], 10)   # -> [[]]"
        ),
        "starter_code": (
            "def grocery_budget(grocery_list, budget):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Exhaustive Recursive Knapsack / Budget Combos (O(2^n)) ===\n"
            "def grocery_budget(grocery_list, budget):\n"
            "    if budget < 0:\n"
            "        return []\n\n"
            "    if not grocery_list:\n"
            "        return [[]]\n\n"
            "    all_lists = []\n"
            "    current_item_name, current_item_price = grocery_list[0]\n"
            "    for list_with_current_item in grocery_budget(grocery_list[1:], budget - current_item_price):\n"
            "        list_with_current_item.append(current_item_name)\n"
            "        all_lists.append(list_with_current_item)\n\n"
            "    lists_without_current_item = grocery_budget(grocery_list[1:], budget)\n"
            "    all_lists += lists_without_current_item\n\n"
            "    return all_lists\n\n\n"
            "# === Example Test Cases ===\n"
            "items = [('eggs', 3), ('bread', 2), ('milk', 4), ('cheese', 6)]\n"
            "print(grocery_budget(items, 5))\n"
            "print(len(grocery_budget(items, 5)))  # -> 5 combinations\n"
        ),
        "time_complexity": "O(2^n)",
        "space_complexity": "O(2^n)",
        "complexity_type": "O(2^n)",
        "complexity_explanation": (
            "Explores all 2^n subsets of groceries by branching on whether to purchase each item within remaining budget. Runs in O(2^n) time and O(2^n) space."
        ),
    },
    {
        "id": "lining_up",
        "title": "138. lining up",
        "raw_title": "lining up",
        "category": "Exhaustive Recursion",
        "description": (
            "Write a function, lining_up, that takes in a list of people and a capacity number. "
            "We need to add people to the waitlist for a popular restaurant, but space is limited.\n\n"
            "The function should return a 2D list containing all the possible orders by which the people can line up. "
            "A valid line must be filled up exactly to the capacity."
        ),
        "examples": (
            "lining_up(['a', 'b', 'c'], 2) # -> 6 orderings: [['a', 'b'], ['b', 'a'], ['a', 'c'], ['c', 'a'], ['b', 'c'], ['c', 'b']]\n"
            "lining_up(['a', 'b'], 3)      # -> []\n"
            "lining_up(['a', 'b', 'c'], 0) # -> [[]]"
        ),
        "starter_code": (
            "def lining_up(people, capacity):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Exhaustive Recursive Permutations of Subsets (O(P(n, k))) ===\n"
            "def lining_up(people, capacity):\n"
            "    if capacity > len(people):\n"
            "        return []\n\n"
            "    if capacity == 0:\n"
            "        return [[]]\n\n"
            "    all_lines = []\n"
            "    current_person = people[0]\n"
            "    remaining_people = people[1:]\n\n"
            "    for line in lining_up(remaining_people, capacity - 1):\n"
            "        for i in range(0, len(line) + 1):\n"
            "            line_with_current = [*line[:i], current_person, *line[i:]]\n"
            "            all_lines.append(line_with_current)\n\n"
            "    for line_without_current in lining_up(remaining_people, capacity):\n"
            "        all_lines.append(line_without_current)\n\n"
            "    return all_lines\n\n\n"
            "# === Example Test Cases ===\n"
            "print(lining_up(['a', 'b', 'c'], 2))\n"
            "print(len(lining_up(['a', 'b', 'c'], 2)))  # -> 6\n"
        ),
        "time_complexity": "O(P(n, k))",
        "space_complexity": "O(P(n, k))",
        "complexity_type": "O(2^n)",
        "complexity_explanation": (
            "Generates all permutations of subsets of length capacity. Runs in O(P(n, k)) time and space."
        ),
    },
    {
        "id": "possible_paths",
        "title": "139. possible paths",
        "raw_title": "possible paths",
        "category": "Exhaustive Recursion",
        "description": (
            "Write a function, possible_paths, that takes in a graph adjacency list, a source node, and a destination node. "
            "The function should return a list containing all possible paths that travel between the source and destination.\n\n"
            "You can assume that the graph is a DAG (directed-acyclic-graph)."
        ),
        "examples": (
            "graph = {'a': ['b', 'c'], 'b': ['d'], 'c': ['d'], 'd': []}\n"
            "possible_paths(graph, 'a', 'd') # -> [['a', 'b', 'd'], ['a', 'c', 'd']]\n"
            "possible_paths(graph, 'd', 'd') # -> [['d']]"
        ),
        "starter_code": (
            "def possible_paths(graph, src, dst):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Exhaustive Recursive Path Traversal in DAG (O(2^V)) ===\n"
            "def traverse_paths(graph, src, dst):\n"
            "    if src == dst:\n"
            "        return [[src]]\n\n"
            "    paths = []\n"
            "    for neighbor in graph[src]:\n"
            "        neighbor_paths = traverse_paths(graph, neighbor, dst)\n"
            "        for neighbor_path in neighbor_paths:\n"
            "            neighbor_path.append(src)\n"
            "            paths.append(neighbor_path)\n"
            "    return paths\n\n"
            "def possible_paths(graph, src, dst):\n"
            "    paths = traverse_paths(graph, src, dst)\n"
            "    return [p[::-1] for p in paths]\n\n\n"
            "# === Example Test Cases ===\n"
            "graph = {'a': ['b', 'c'], 'b': ['d'], 'c': ['d'], 'd': []}\n"
            "print(possible_paths(graph, 'a', 'd'))  # -> [['a', 'b', 'd'], ['a', 'c', 'd']]\n"
        ),
        "time_complexity": "O(2^V)",
        "space_complexity": "O(2^V)",
        "complexity_type": "O(2^n)",
        "complexity_explanation": (
            "Recursively explores every distinct path in the DAG between source and destination. Runs in O(2^V) time in worst case."
        ),
    },
    {
        "id": "parenthetical_possibilities",
        "title": "140. parenthetical possibilities",
        "raw_title": "parenthetical possibilities",
        "category": "Exhaustive Recursion",
        "description": (
            "Write a function, parenthetical_possibilities, that takes in a string as an argument. "
            "The function should return an array containing all of the strings that could be generated by expanding all "
            "parentheses of the string into its possibilities.\n\n"
            "For example, the possibilities for 'x(mn)yz' are 'xmyz', 'xnyz'."
        ),
        "examples": (
            "parenthetical_possibilities('x(mn)yz')       # -> ['xmyz', 'xnyz']\n"
            "parenthetical_possibilities('(qr)st(uv)')     # -> ['qstu', 'qstv', 'rstu', 'rstv']\n"
            "parenthetical_possibilities('abc')            # -> ['abc']"
        ),
        "starter_code": (
            "def parenthetical_possibilities(s):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Exhaustive Recursive Parenthesis Expansion (O(m^k)) ===\n"
            "def get_options(s):\n"
            "    if s[0] == '(':\n"
            "        idx = s.index(')')\n"
            "        chars = s[1:idx]\n"
            "        remaining = s[idx + 1:]\n"
            "        return (remaining, chars)\n"
            "    else:\n"
            "        chars = s[0]\n"
            "        remaining = s[1:]\n"
            "        return (remaining, chars)\n\n"
            "def parenthetical_possibilities(s):\n"
            "    if len(s) == 0:\n"
            "        return ['']\n\n"
            "    remaining, chars = get_options(s)\n"
            "    suffixes = parenthetical_possibilities(remaining)\n"
            "    possibilities = []\n"
            "    for char in chars:\n"
            "        possibilities += [char + suffix for suffix in suffixes]\n"
            "    return possibilities\n\n\n"
            "# === Example Test Cases ===\n"
            "print(parenthetical_possibilities('x(mn)yz'))    # -> ['xmyz', 'xnyz']\n"
            "print(parenthetical_possibilities('(qr)st(uv)'))  # -> ['qstu', 'qstv', 'rstu', 'rstv']\n"
        ),
        "time_complexity": "O(m^k)",
        "space_complexity": "O(m^k)",
        "complexity_type": "O(2^n)",
        "complexity_explanation": (
            "Branches recursively on each choice within parenthetical groups. Runs in O(m^k) time and space where m is max options and k is groups count."
        ),
    },
    {
        "id": "substituting_synonyms",
        "title": "141. substituting synonyms",
        "raw_title": "substituting synonyms",
        "category": "Exhaustive Recursion",
        "description": (
            "Write a function, substituting_synonyms, that takes in a sentence and a dictionary as arguments. "
            "The dictionary contains words as keys whose values are arrays containing synonyms. "
            "The function should return an array containing all possible sentences that can be formed by substituting words of the sentence with their synonyms.\n\n"
            "You may return the possible sentences in any order, as long as you return all of them."
        ),
        "examples": (
            "sentence = 'follow the yellow brick road'\n"
            "synonyms = {'follow': ['chase', 'pursue'], 'yellow': ['gold', 'amber'], 'road': ['path', 'way']}\n"
            "substitute_synonyms(sentence, synonyms) # -> 8 sentences"
        ),
        "starter_code": (
            "def substituting_synonyms(sentence, synonyms):\n"
            "  pass # todo\n\n"
            "substitute_synonyms = substituting_synonyms\n"
        ),
        "solution_code": (
            "# === Exhaustive Recursive Word Replacement (O(s^w)) ===\n"
            "def generate(words, synonyms):\n"
            "    if len(words) == 0:\n"
            "        return [[]]\n\n"
            "    first_word = words[0]\n"
            "    remaining_words = words[1:]\n"
            "    subarrays = generate(remaining_words, synonyms)\n\n"
            "    if first_word in synonyms:\n"
            "        result = []\n"
            "        for synonym in synonyms[first_word]:\n"
            "            result += [[synonym, *subarray] for subarray in subarrays]\n"
            "        return result\n"
            "    else:\n"
            "        return [[first_word, *subarray] for subarray in subarrays]\n\n"
            "def substitute_synonyms(sentence, synonyms):\n"
            "    words = sentence.split(' ')\n"
            "    subarrays = generate(words, synonyms)\n"
            "    return [' '.join(subarray) for subarray in subarrays]\n\n"
            "substituting_synonyms = substitute_synonyms\n\n\n"
            "# === Example Test Cases ===\n"
            "sentence = 'follow the yellow brick road'\n"
            "synonyms = {'follow': ['chase', 'pursue'], 'yellow': ['gold', 'amber'], 'road': ['path', 'way']}\n"
            "print(len(substitute_synonyms(sentence, synonyms)))  # -> 8\n"
            "print(substitute_synonyms(sentence, synonyms)[0])\n"
        ),
        "time_complexity": "O(s^w)",
        "space_complexity": "O(s^w)",
        "complexity_type": "O(2^n)",
        "complexity_explanation": (
            "Recursively computes the Cartesian product of synonyms across each word in the sentence. Runs in O(s^w) time and space."
        ),
    },
    {
        "id": "knight_attack",
        "title": "142. knight attack",
        "raw_title": "knight attack",
        "category": "Graph II",
        "description": (
            "A knight and a pawn are on a chess board. Can you figure out the minimum number of moves required for the "
            "knight to travel to the same position of the pawn? On a single move, the knight can move in an 'L' shape: "
            "two spaces in any direction, then one space in a perpendicular direction (eight possible positions).\n\n"
            "Write a function, knight_attack, that takes in 5 arguments: n, kr, kc, pr, pc.\n"
            "- n = length of the chess board (n x n)\n"
            "- kr, kc = starting row and column of the knight\n"
            "- pr, pc = row and column of the pawn\n\n"
            "The function should return a number representing the minimum number of moves required for the knight to land on top "
            "of the pawn. Rows and columns are 0-indexed. If it is not possible to attack the pawn, return None."
        ),
        "examples": (
            "knight_attack(8, 1, 1, 2, 2) # -> 2\n"
            "knight_attack(8, 1, 1, 2, 3) # -> 1\n"
            "knight_attack(8, 0, 0, 7, 7) # -> 6\n"
            "knight_attack(3, 0, 0, 1, 1) # -> None"
        ),
        "starter_code": (
            "def knight_attack(n, kr, kc, pr, pc):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import deque\n\n\n"
            "# === Shortest Path via BFS on Chessboard (O(n^2)) ===\n"
            "def get_knight_moves(n, r, c):\n"
            "    positions = [\n"
            "        (r + 2, c + 1),\n"
            "        (r - 2, c + 1),\n"
            "        (r + 2, c - 1),\n"
            "        (r - 2, c - 1),\n"
            "        (r + 1, c + 2),\n"
            "        (r - 1, c + 2),\n"
            "        (r + 1, c - 2),\n"
            "        (r - 1, c - 2),\n"
            "    ]\n"
            "    inbounds_positions = []\n"
            "    for pos in positions:\n"
            "        new_row, new_col = pos\n"
            "        if 0 <= new_row < n and 0 <= new_col < n:\n"
            "            inbounds_positions.append(pos)\n"
            "    return inbounds_positions\n\n"
            "def knight_attack(n, kr, kc, pr, pc):\n"
            "    visited = set()\n"
            "    visited.add((kr, kc))\n"
            "    queue = deque([(kr, kc, 0)])\n"
            "    while len(queue) > 0:\n"
            "        r, c, step = queue.popleft()\n"
            "        if (r, c) == (pr, pc):\n"
            "            return step\n"
            "        neighbors = get_knight_moves(n, r, c)\n"
            "        for neighbor in neighbors:\n"
            "            neighbor_row, neighbor_col = neighbor\n"
            "            if neighbor not in visited:\n"
            "                visited.add(neighbor)\n"
            "                queue.append((neighbor_row, neighbor_col, step + 1))\n"
            "    return None\n\n\n"
            "# === Example Test Cases ===\n"
            "print(knight_attack(8, 1, 1, 2, 2))  # -> 2\n"
            "print(knight_attack(8, 1, 1, 2, 3))  # -> 1\n"
            "print(knight_attack(8, 0, 0, 7, 7))  # -> 6\n"
            "print(knight_attack(3, 0, 0, 1, 1))  # -> None\n"
        ),
        "time_complexity": "O(n^2)",
        "space_complexity": "O(n^2)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Explores chessboard positions using breadth-first search to find the shortest knight path. Runs in O(n^2) time and O(n^2) space."
        ),
    },
    {
        "id": "can_color",
        "title": "143. can color",
        "raw_title": "can color",
        "category": "Graph II",
        "description": (
            "Write a function, can_color, that takes in a dictionary representing the adjacency list of an undirected graph. "
            "The function should return a boolean indicating whether or not it is possible to color nodes of the graph using "
            "two colors in such a way that adjacent nodes are always different colors (i.e. checking if graph is bipartite)."
        ),
        "examples": (
            "can_color({'x': ['y'], 'y': ['x', 'z'], 'z': ['y']}) # -> True\n"
            "can_color({'q': ['r', 's'], 'r': ['q', 's'], 's': ['r', 'q']}) # -> False"
        ),
        "starter_code": (
            "def can_color(graph):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Bipartite Graph 2-Coloring via DFS (O(V + E)) ===\n"
            "def valid(graph, node, coloring, current_color):\n"
            "    if node in coloring:\n"
            "        return current_color == coloring[node]\n\n"
            "    coloring[node] = current_color\n\n"
            "    for neighbor in graph[node]:\n"
            "        if not valid(graph, neighbor, coloring, not current_color):\n"
            "            return False\n\n"
            "    return True\n\n"
            "def can_color(graph):\n"
            "    coloring = {}\n"
            "    for node in graph:\n"
            "        if node not in coloring:\n"
            "            if not valid(graph, node, coloring, False):\n"
            "                return False\n"
            "    return True\n\n\n"
            "# === Example Test Cases ===\n"
            "print(can_color({'x': ['y'], 'y': ['x', 'z'], 'z': ['y']})) # -> True\n"
            "print(can_color({'q': ['r', 's'], 'r': ['q', 's'], 's': ['r', 'q']})) # -> False\n"
        ),
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Performs depth-first search to 2-color all connected components while verifying no two adjacent nodes share a color. Runs in O(V + E) time and O(V) space."
        ),
    },
    {
        "id": "tolerant_teams",
        "title": "144. tolerant teams",
        "raw_title": "tolerant teams",
        "category": "Graph II",
        "description": (
            "Write a function, tolerant_teams, that takes in a list of rivalries as an argument. "
            "A rivalry is a pair of people who should not be placed on the same team. "
            "The function should return a boolean indicating whether or not it is possible to separate people into two teams, "
            "without rivals being on the same team. The two teams formed do not have to be the same size."
        ),
        "examples": (
            "tolerant_teams([('philip', 'seb'), ('raj', 'seb'), ('raj', 'philip')]) # -> False\n"
            "tolerant_teams([('philip', 'seb'), ('raj', 'seb'), ('jonathan', 'raj')]) # -> True\n"
            "tolerant_teams([]) # -> True"
        ),
        "starter_code": (
            "def tolerant_teams(rivalries):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Bipartite Rivalry Graph via 2-Coloring (O(e + n)) ===\n"
            "def build_graph(edges):\n"
            "    graph = {}\n"
            "    for edge in edges:\n"
            "        a, b = edge\n"
            "        if a not in graph:\n"
            "            graph[a] = []\n"
            "        if b not in graph:\n"
            "            graph[b] = []\n"
            "        graph[a].append(b)\n"
            "        graph[b].append(a)\n"
            "    return graph\n\n"
            "def is_bipartite(graph, node, coloring, current_color):\n"
            "    if node in coloring:\n"
            "        return coloring[node] == current_color\n\n"
            "    coloring[node] = current_color\n\n"
            "    for neighbor in graph[node]:\n"
            "        if not is_bipartite(graph, neighbor, coloring, not current_color):\n"
            "            return False\n\n"
            "    return True\n\n"
            "def tolerant_teams(rivalries):\n"
            "    graph = build_graph(rivalries)\n"
            "    coloring = {}\n"
            "    for node in graph:\n"
            "        if node not in coloring and not is_bipartite(graph, node, coloring, False):\n"
            "            return False\n"
            "    return True\n\n\n"
            "# === Example Test Cases ===\n"
            "print(tolerant_teams([('philip', 'seb'), ('raj', 'seb'), ('raj', 'philip')])) # -> False\n"
            "print(tolerant_teams([('philip', 'seb'), ('raj', 'seb'), ('jonathan', 'raj')])) # -> True\n"
        ),
        "time_complexity": "O(e + n)",
        "space_complexity": "O(e + n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Constructs the rivalry graph and determines whether it can be partitioned into two independent sets (bipartite 2-coloring). Runs in O(e + n) time and space."
        ),
    },
    {
        "id": "rare_routing",
        "title": "145. rare routing",
        "raw_title": "rare routing",
        "category": "Graph II",
        "description": (
            "Write a function, rare_routing, that takes in a number of cities (n) and a list of tuples where each tuple "
            "represents a direct road that connects a pair of cities. The function should return a boolean indicating whether "
            "or not there exists a unique route for every pair of cities (i.e. checking if the graph is a valid tree).\n\n"
            "Cities are numbered 0 to n - 1. All roads are two-way."
        ),
        "examples": (
            "rare_routing(4, [(0, 1), (0, 2), (0, 3)]) # -> True\n"
            "rare_routing(4, [(0, 1), (0, 2), (0, 3), (3, 2)]) # -> False (contains cycle)\n"
            "rare_routing(4, [(0, 1), (0, 2)]) # -> False (disconnected)"
        ),
        "starter_code": (
            "def rare_routing(n, roads):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Connected & Acyclic Tree Validation via DFS (O(V + E)) ===\n"
            "def make_graph(n, roads):\n"
            "    graph = {}\n"
            "    for city in range(n):\n"
            "        graph[city] = []\n"
            "    for road in roads:\n"
            "        a, b = road\n"
            "        graph[a].append(b)\n"
            "        graph[b].append(a)\n"
            "    return graph\n\n"
            "def validate(graph, node, visited, last_node):\n"
            "    if node in visited:\n"
            "        return False\n\n"
            "    visited.add(node)\n"
            "    for neighbor in graph[node]:\n"
            "        if neighbor != last_node and not validate(graph, neighbor, visited, node):\n"
            "            return False\n\n"
            "    return True\n\n"
            "def rare_routing(n, roads):\n"
            "    graph = make_graph(n, roads)\n"
            "    visited = set()\n"
            "    valid = validate(graph, 0, visited, None)\n"
            "    return valid and len(visited) == n\n\n\n"
            "# === Example Test Cases ===\n"
            "print(rare_routing(4, [(0, 1), (0, 2), (0, 3)])) # -> True\n"
            "print(rare_routing(4, [(0, 1), (0, 2), (0, 3), (3, 2)])) # -> False\n"
            "print(rare_routing(4, [(0, 1), (0, 2)])) # -> False\n"
        ),
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V + E)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Traverses the road network with DFS to verify connectivity (visits all n nodes) and acyclicity (no back-edges). Runs in O(V + E) time and space."
        ),
    },
    {
        "id": "topological_order",
        "title": "146. topological order",
        "raw_title": "topological order",
        "category": "Graph II",
        "description": (
            "Write a function, topological_order, that takes in a dictionary representing the adjacency list for a "
            "directed-acyclic graph (DAG). The function should return a list containing the topological order of the graph.\n\n"
            "The topological ordering of a graph is a sequence where 'parent nodes' appear before their 'children' within the sequence."
        ),
        "examples": (
            "graph = {'a': ['f'], 'b': ['d'], 'c': ['a', 'f'], 'd': ['e'], 'e': [], 'f': ['b', 'e']}\n"
            "topological_order(graph) # -> ['c', 'a', 'f', 'b', 'd', 'e']"
        ),
        "starter_code": (
            "def topological_order(graph):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Kahn's Algorithm for Topological Sort (O(V + E)) ===\n"
            "def topological_order(graph):\n"
            "    num_parents = {}\n"
            "    for node in graph:\n"
            "        num_parents[node] = 0\n\n"
            "    for node in graph:\n"
            "        for child in graph[node]:\n"
            "            num_parents[child] += 1\n\n"
            "    ready = [node for node in graph if num_parents[node] == 0]\n"
            "    order = []\n"
            "    while ready:\n"
            "        node = ready.pop()\n"
            "        order.append(node)\n"
            "        for child in graph[node]:\n"
            "            num_parents[child] -= 1\n"
            "            if num_parents[child] == 0:\n"
            "                ready.append(child)\n\n"
            "    return order\n\n\n"
            "# === Example Test Cases ===\n"
            "graph = {'a': ['f'], 'b': ['d'], 'c': ['a', 'f'], 'd': ['e'], 'e': [], 'f': ['b', 'e']}\n"
            "print(topological_order(graph))  # -> ['c', 'a', 'f', 'b', 'd', 'e']\n"
        ),
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Computes in-degrees for each vertex and processes zero-in-degree nodes in order via Kahn's algorithm. Runs in O(V + E) time and O(V) space."
        ),
    },
    {
        "id": "safe_cracking",
        "title": "147. safe cracking",
        "raw_title": "safe cracking",
        "category": "Graph II",
        "description": (
            "Oh-no! You forgot the number combination that unlocks your safe. Luckily, you wrote down a bunch of hints. "
            "Each hint is a pair of numbers 'x, y' that indicates you must enter digit 'x' before 'y'.\n\n"
            "The keypad on the safe has digits 0-9. Hints generate exactly one working combination and digits occur at most once.\n\n"
            "Write a function, safe_cracking, that takes in a list of hints as an argument and determines the combination string."
        ),
        "examples": (
            "hints = [(7, 1), (1, 8), (2, 6), (8, 6), (2, 5), (6, 5), (3, 4), (5, 4), (7, 3)]\n"
            "safe_cracking(hints) # -> '27318654' (or valid topological string)"
        ),
        "starter_code": (
            "def safe_cracking(hints):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Dependency Resolution via Topological Order (O(V + E)) ===\n"
            "def build_graph(edges):\n"
            "    graph = {}\n"
            "    for edge in edges:\n"
            "        a, b = edge\n"
            "        if a not in graph:\n"
            "            graph[a] = []\n"
            "        if b not in graph:\n"
            "            graph[b] = []\n"
            "        graph[a].append(b)\n"
            "    return graph\n\n"
            "def topological_order(graph):\n"
            "    num_parents = {}\n"
            "    for node in graph:\n"
            "        num_parents[node] = 0\n\n"
            "    for node in graph:\n"
            "        for child in graph[node]:\n"
            "            num_parents[child] += 1\n\n"
            "    ready = [node for node in graph if num_parents[node] == 0]\n"
            "    order = ''\n"
            "    while ready:\n"
            "        node = ready.pop()\n"
            "        order += str(node)\n"
            "        for child in graph[node]:\n"
            "            num_parents[child] -= 1\n"
            "            if num_parents[child] == 0:\n"
            "                ready.append(child)\n\n"
            "    return order\n\n"
            "def safe_cracking(hints):\n"
            "    graph = build_graph(hints)\n"
            "    return topological_order(graph)\n\n\n"
            "# === Example Test Cases ===\n"
            "hints = [(7, 1), (1, 8), (2, 6), (8, 6), (2, 5), (6, 5), (3, 4), (5, 4), (7, 3)]\n"
            "print(safe_cracking(hints))\n"
        ),
        "time_complexity": "O(V + E)",
        "space_complexity": "O(V + E)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Builds a DAG from pairwise order constraints and computes the unique topological sequence of digits. Runs in O(V + E) time and space."
        ),
    },
    {
        "id": "string_search",
        "title": "148. string search",
        "raw_title": "string search",
        "category": "Graph II",
        "description": (
            "Write a function, string_search, that takes in a grid of letters and a string as arguments. "
            "The function should return a boolean indicating whether or not the string can be found in the grid as a path "
            "by connecting horizontal or vertical positions. The path can begin at any position, but you cannot reuse a position "
            "more than once in the path.\n\n"
            "You can assume that all letters are lowercase and alphabetic."
        ),
        "examples": (
            "grid = [['a', 'b', 'a'], ['t', 'x', 'x'], ['x', 'x', 'x']]\n"
            "string_search(grid, 'bat') # -> True\n"
            "string_search(grid, 'tab') # -> True\n"
            "string_search(grid, 'zoo') # -> False"
        ),
        "starter_code": (
            "def string_search(grid, s):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === 2D Grid Word Search via Backtracking DFS (O(r * c * 3^L)) ===\n"
            "def dfs(grid, r, c, s):\n"
            "    if s == '':\n"
            "        return True\n\n"
            "    row_inbounds = 0 <= r < len(grid)\n"
            "    col_inbounds = 0 <= c < len(grid[0])\n"
            "    if not row_inbounds or not col_inbounds:\n"
            "        return False\n\n"
            "    char = grid[r][c]\n"
            "    if char != s[0]:\n"
            "        return False\n\n"
            "    suffix = s[1:]\n"
            "    grid[r][c] = '*'\n"
            "    result = (\n"
            "        dfs(grid, r + 1, c, suffix)\n"
            "        or dfs(grid, r - 1, c, suffix)\n"
            "        or dfs(grid, r, c + 1, suffix)\n"
            "        or dfs(grid, r, c - 1, suffix)\n"
            "    )\n"
            "    grid[r][c] = char\n"
            "    return result\n\n"
            "def string_search(grid, s):\n"
            "    for r in range(len(grid)):\n"
            "        for c in range(len(grid[0])):\n"
            "            if dfs(grid, r, c, s):\n"
            "                return True\n"
            "    return False\n\n\n"
            "# === Example Test Cases ===\n"
            "grid = [['a', 'b', 'a'], ['t', 'x', 'x'], ['x', 'x', 'x']]\n"
            "print(string_search(grid, 'bat'))  # -> True\n"
            "print(string_search(grid, 'tab'))  # -> True\n"
            "print(string_search(grid, 'zoo'))  # -> False\n"
        ),
        "time_complexity": "O(r * c * 3^L)",
        "space_complexity": "O(L)",
        "complexity_type": "O(2^n)",
        "complexity_explanation": (
            "Explores all potential word paths starting from each cell using backtracking DFS up to length L. Runs in O(r * c * 3^L) time and O(L) space."
        ),
    },
    {
        "id": "union_find_code_i",
        "title": "149. union-find code I",
        "raw_title": "union-find code I",
        "category": "Graph II",
        "description": (
            "Write a function, count_components, that takes in a number of nodes (n) and a list of edges for an undirected graph. "
            "In the graph, nodes are labeled from 0 to n - 1. The function should return the number of connected components in the given graph.\n\n"
            "This problem serves as foundational practice for implementing the basic Union-Find (Disjoint Set) algorithm for graphs."
        ),
        "examples": (
            "count_components(5, [(0, 1), (1, 2), (3, 4)]) # -> 2\n"
            "count_components(4, [])                         # -> 4\n"
            "count_components(3, [(0, 1), (1, 2), (2, 0)]) # -> 1"
        ),
        "starter_code": (
            "def count_components(n, edges):\n"
            "  pass # todo\n\n"
            "union_find_code_i = count_components\n"
        ),
        "solution_code": (
            "# === Basic Disjoint-Set Union-Find (O(e * n)) ===\n"
            "def find(roots, node):\n"
            "    if node == roots[node]:\n"
            "        return node\n"
            "    return find(roots, roots[node])\n\n"
            "def union(roots, node_a, node_b):\n"
            "    root_a = find(roots, node_a)\n"
            "    root_b = find(roots, node_b)\n"
            "    roots[root_b] = root_a\n\n"
            "def count_components(n, edges):\n"
            "    roots = [i for i in range(0, n)]\n\n"
            "    for edge in edges:\n"
            "        node_a, node_b = edge\n"
            "        union(roots, node_a, node_b)\n\n"
            "    count = 0\n"
            "    for i in range(0, len(roots)):\n"
            "        if i == roots[i]:\n"
            "            count += 1\n\n"
            "    return count\n\n"
            "union_find_code_i = count_components\n\n\n"
            "# === Example Test Cases ===\n"
            "print(count_components(5, [(0, 1), (1, 2), (3, 4)])) # -> 2\n"
            "print(count_components(4, []))                         # -> 4\n"
            "print(count_components(3, [(0, 1), (1, 2), (2, 0)])) # -> 1\n"
        ),
        "time_complexity": "O(e * n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Basic union-find without path compression. Each find/union operation can take O(n) in worst-case degenerate trees. Runs in O(e * n) time and O(n) space."
        ),
    },
    {
        "id": "union_find_code_ii",
        "title": "150. union-find code II",
        "raw_title": "union-find code II",
        "category": "Graph II",
        "description": (
            "Write a function, count_components, that takes in a number of nodes (n) and a list of edges for an undirected graph. "
            "In the graph, nodes are labeled from 0 to n - 1. The function should return the number of connected components in the given graph.\n\n"
            "Solve this by implementing the complete, optimized Union-Find (Disjoint Set) algorithm with union-by-size and path compression."
        ),
        "examples": (
            "count_components(5, [(0, 1), (1, 2), (3, 4)]) # -> 2\n"
            "count_components(4, [])                         # -> 4\n"
            "count_components(3, [(0, 1), (1, 2), (2, 0)]) # -> 1"
        ),
        "starter_code": (
            "def count_components(n, edges):\n"
            "  pass # todo\n\n"
            "countComponents = count_components\n"
            "union_find_code_ii = count_components\n"
        ),
        "solution_code": (
            "# === Optimized Union-Find with Path Compression & Union by Size (O(e * alpha(n))) ===\n"
            "def find(roots, node):\n"
            "    if node == roots[node]:\n"
            "        return node\n"
            "    found = find(roots, roots[node])\n"
            "    roots[node] = found\n"
            "    return found\n\n"
            "def union(roots, sizes, node_a, node_b):\n"
            "    root_a = find(roots, node_a)\n"
            "    root_b = find(roots, node_b)\n"
            "    if root_a == root_b:\n"
            "        return\n\n"
            "    if sizes[root_a] >= sizes[root_b]:\n"
            "        roots[root_b] = root_a\n"
            "        sizes[root_a] += sizes[root_b]\n"
            "    else:\n"
            "        roots[root_a] = root_b\n"
            "        sizes[root_b] += sizes[root_a]\n\n"
            "def count_components(n, edges):\n"
            "    roots = [i for i in range(0, n)]\n"
            "    sizes = [1 for i in range(0, n)]\n\n"
            "    for edge in edges:\n"
            "        node_a, node_b = edge\n"
            "        union(roots, sizes, node_a, node_b)\n\n"
            "    count = 0\n"
            "    for i in range(0, len(roots)):\n"
            "        if i == roots[i]:\n"
            "            count += 1\n\n"
            "    return count\n\n"
            "countComponents = count_components\n"
            "union_find_code_ii = count_components\n\n\n"
            "# === Example Test Cases ===\n"
            "print(count_components(5, [(0, 1), (1, 2), (3, 4)])) # -> 2\n"
            "print(count_components(4, []))                         # -> 4\n"
            "print(count_components(3, [(0, 1), (1, 2), (2, 0)])) # -> 1\n"
        ),
        "time_complexity": "O(e * alpha(n))",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Complete disjoint-set union-find with path compression and union-by-size. Achieves nearly linear O(e * alpha(n)) amortized time and O(n) space."
        ),
    },
    {
        "id": "province_sizes",
        "title": "151. province sizes",
        "raw_title": "province sizes",
        "category": "Graph II",
        "description": (
            "Write a function, province_sizes, that takes in a number of cities n and a list of roads which connect cities. "
            "Roads can be traveled in both directions. Cities are named from 0 to n - 1.\n\n"
            "A 'province' is a group of 1 or more cities connected by roads. The 'size' of a province is the number of cities in it.\n\n"
            "Your function should return a list containing the sizes of the provinces in any order using Union-Find."
        ),
        "examples": (
            "province_sizes(4, [(0, 1), (1, 2), (0, 2)]) # -> [3, 1] (or [1, 3])\n"
            "province_sizes(3, [(0, 1), (1, 2)])          # -> [3]\n"
            "province_sizes(4, [])                         # -> [1, 1, 1, 1]"
        ),
        "starter_code": (
            "def province_sizes(n, roads):\n"
            "  pass # todo\n\n"
            "provinceSizes = province_sizes\n"
        ),
        "solution_code": (
            "# === Component Sizes via Union-Find (O(r * alpha(n))) ===\n"
            "def find(roots, node):\n"
            "    if node == roots[node]:\n"
            "        return node\n"
            "    found = find(roots, roots[node])\n"
            "    roots[node] = found\n"
            "    return found\n\n"
            "def union(roots, sizes, node_a, node_b):\n"
            "    root_a = find(roots, node_a)\n"
            "    root_b = find(roots, node_b)\n"
            "    if root_a == root_b:\n"
            "        return\n\n"
            "    if sizes[root_a] >= sizes[root_b]:\n"
            "        roots[root_b] = root_a\n"
            "        sizes[root_a] += sizes[root_b]\n"
            "    else:\n"
            "        roots[root_a] = root_b\n"
            "        sizes[root_b] += sizes[root_a]\n\n"
            "def province_sizes(n, roads):\n"
            "    roots = [i for i in range(0, n)]\n"
            "    sizes = [1 for i in range(0, n)]\n\n"
            "    for road in roads:\n"
            "        a, b = road\n"
            "        union(roots, sizes, a, b)\n\n"
            "    result = []\n"
            "    for i in range(0, n):\n"
            "        if i == roots[i]:\n"
            "            result.append(sizes[i])\n\n"
            "    return result\n\n"
            "provinceSizes = province_sizes\n\n\n"
            "# === Example Test Cases ===\n"
            "print(sorted(province_sizes(4, [(0, 1), (1, 2), (0, 2)]))) # -> [1, 3]\n"
            "print(province_sizes(3, [(0, 1), (1, 2)]))                 # -> [3]\n"
        ),
        "time_complexity": "O(r * alpha(n))",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Uses Union-Find with path compression and union-by-size to aggregate component sizes across all roads. Runs in O(r * alpha(n)) time and O(n) space."
        ),
    },
    {
        "id": "extra_cable",
        "title": "152. extra cable",
        "raw_title": "extra cable",
        "category": "Graph II",
        "description": (
            "You are given a network of computers connected by bidirectional cables. The network was originally fully-connected "
            "and minimal (a spanning tree), but exactly one extra cable was added, introducing a cycle.\n\n"
            "Write a function, extra_cable, that takes in num_computers and a list of cables, and returns a redundant cable that "
            "can be safely removed while ensuring the network remains fully-connected and minimal."
        ),
        "examples": (
            "cables = [(0, 1), (1, 2), (2, 4), (3, 1), (3, 2)]\n"
            "extra_cable(5, cables) # -> (3, 2) (or redundant cable creating cycle)"
        ),
        "starter_code": (
            "def extra_cable(num_computers, cables):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Redundant Connection / Cycle Detection via Union-Find (O(c * alpha(n))) ===\n"
            "def find(roots, node):\n"
            "    if node == roots[node]:\n"
            "        return node\n"
            "    found = find(roots, roots[node])\n"
            "    roots[node] = found\n"
            "    return found\n\n"
            "def union(roots, sizes, node_a, node_b):\n"
            "    root_a = find(roots, node_a)\n"
            "    root_b = find(roots, node_b)\n"
            "    if root_a == root_b:\n"
            "        return False\n\n"
            "    if sizes[root_a] >= sizes[root_b]:\n"
            "        roots[root_b] = root_a\n"
            "        sizes[root_a] += sizes[root_b]\n"
            "    else:\n"
            "        roots[root_a] = root_b\n"
            "        sizes[root_b] += sizes[root_a]\n\n"
            "    return True\n\n"
            "def extra_cable(num_computers, cables):\n"
            "    roots = [i for i in range(0, num_computers)]\n"
            "    sizes = [1 for i in range(0, num_computers)]\n\n"
            "    for cable in cables:\n"
            "        a, b = cable\n"
            "        if not union(roots, sizes, a, b):\n"
            "            return cable\n\n"
            "    return None\n\n\n"
            "# === Example Test Cases ===\n"
            "cables = [(0, 1), (1, 2), (2, 4), (3, 1), (3, 2)]\n"
            "print(extra_cable(5, cables))  # -> (3, 2)\n"
        ),
        "time_complexity": "O(c * alpha(n))",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Iterates through cables and identifies the first edge connecting two already-connected vertices using Union-Find. Runs in O(c * alpha(n)) time and O(n) space."
        ),
    },
    {
        "id": "weighted_graph_min_path",
        "title": "153. weighted graph min path",
        "raw_title": "weighted graph min path",
        "category": "Graph II",
        "description": (
            "Write a function, weighted_graph_min_path, that takes in the adjacency list for a weighted graph and two nodes, "
            "src and dst. The function should return the minimum cost path that travels from src to dst.\n\n"
            "The cost of a path is the sum of the weights of edges traveled. All edge weights are non-negative numbers, "
            "and there is at least one path between src and dst."
        ),
        "examples": (
            "graph = {'a': {'b': 3, 'c': 2}, 'b': {'d': 4}, 'c': {'d': 1}, 'd': {}}\n"
            "weighted_graph_min_path(graph, 'a', 'd') # -> 3 (a -> c -> d: 2 + 1)"
        ),
        "starter_code": (
            "def weighted_graph_min_path(graph, src, dst):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Backtracking DFS for Min-Weight Path (O(V!)) ===\n"
            "def min_path(graph, src, dst, visited):\n"
            "    if src == dst:\n"
            "        return 0\n\n"
            "    if src in visited:\n"
            "        return float('inf')\n\n"
            "    visited.add(src)\n"
            "    min_cost = float('inf')\n\n"
            "    for neighbor in graph[src]:\n"
            "        cost = graph[src][neighbor]\n"
            "        total_cost = cost + min_path(graph, neighbor, dst, visited)\n"
            "        min_cost = min(min_cost, total_cost)\n\n"
            "    visited.remove(src)\n"
            "    return min_cost\n\n"
            "def weighted_graph_min_path(graph, src, dst):\n"
            "    return min_path(graph, src, dst, set())\n\n\n"
            "# === Example Test Cases ===\n"
            "graph = {'a': {'b': 3, 'c': 2}, 'b': {'d': 4}, 'c': {'d': 1}, 'd': {}}\n"
            "print(weighted_graph_min_path(graph, 'a', 'd'))  # -> 3\n"
        ),
        "time_complexity": "O(V!)",
        "space_complexity": "O(V)",
        "complexity_type": "O(2^n)",
        "complexity_explanation": (
            "Explores all simple paths from source to destination using backtracking DFS. Runs in O(V!) time in worst case and O(V) space."
        ),
    },
    {
        "id": "lowest_toll",
        "title": "154. lowest toll",
        "raw_title": "lowest toll",
        "category": "Graph II",
        "description": (
            "You are given the tolls for different highways. Each highway connects a pair of cities and has a particular cost. "
            "Each highway toll is a triplet (cityA, cityB, cost) and can be traveled in either direction.\n\n"
            "Write a function, lowest_toll, that takes in highway tolls and two cities, and returns the lowest cost required "
            "to travel between the two cities."
        ),
        "examples": (
            "tolls = [('a', 'b', 3), ('a', 'c', 2), ('c', 'd', 1), ('b', 'd', 4)]\n"
            "lowest_toll(tolls, 'a', 'd') # -> 3"
        ),
        "starter_code": (
            "def lowest_toll(highway_tolls, start_city, end_city):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Min-Cost Highway Path Traversal (O(V!)) ===\n"
            "def min_path(graph, src, dst, visited):\n"
            "    if src == dst:\n"
            "        return 0\n\n"
            "    if src in visited:\n"
            "        return float('inf')\n\n"
            "    visited.add(src)\n"
            "    min_cost = float('inf')\n\n"
            "    for neighbor in graph[src]:\n"
            "        cost = graph[src][neighbor]\n"
            "        total_cost = cost + min_path(graph, neighbor, dst, visited)\n"
            "        if total_cost < min_cost:\n"
            "            min_cost = total_cost\n\n"
            "    visited.remove(src)\n"
            "    return min_cost\n\n"
            "def lowest_toll(highway_tolls, start_city, end_city):\n"
            "    graph = {}\n"
            "    for city_a, city_b, cost in highway_tolls:\n"
            "        if city_a not in graph:\n"
            "            graph[city_a] = {}\n"
            "        if city_b not in graph:\n"
            "            graph[city_b] = {}\n"
            "        graph[city_a][city_b] = cost\n"
            "        graph[city_b][city_a] = cost\n\n"
            "    return min_path(graph, start_city, end_city, set())\n\n\n"
            "# === Example Test Cases ===\n"
            "tolls = [('a', 'b', 3), ('a', 'c', 2), ('c', 'd', 1), ('b', 'd', 4)]\n"
            "print(lowest_toll(tolls, 'a', 'd'))  # -> 3\n"
        ),
        "time_complexity": "O(V!)",
        "space_complexity": "O(V)",
        "complexity_type": "O(2^n)",
        "complexity_explanation": (
            "Builds a weighted bidirectional graph and searches for the minimum total cost path using backtracking DFS. Runs in O(V!) time and O(V) space."
        ),
    },
    {
        "id": "prefix_product",
        "title": "155. prefix product",
        "raw_title": "prefix product",
        "category": "Mixed Recall",
        "description": (
            "Write a function, prefix_product, that takes in a list of numbers. The function should return a new list of the "
            "same length where each element contains the running product up to that index of the original list.\n\n"
            "For example, result[i] = numbers[0] * numbers[1] * ... * numbers[i]. The input list is non-empty."
        ),
        "examples": (
            "prefix_product([1, 2, 3, 4]) # -> [1, 2, 6, 24]\n"
            "prefix_product([2, 5, 2])    # -> [2, 10, 20]"
        ),
        "starter_code": (
            "def prefix_product(numbers):\n"
            "  pass # todo\n\n"
            "prefixProduct = prefix_product\n"
        ),
        "solution_code": (
            "# === Running Prefix Product (O(n)) ===\n"
            "def prefix_product(numbers):\n"
            "    total = 1\n"
            "    result = []\n"
            "    for num in numbers:\n"
            "        total *= num\n"
            "        result.append(total)\n"
            "    return result\n\n"
            "prefixProduct = prefix_product\n\n\n"
            "# === Example Test Cases ===\n"
            "print(prefix_product([1, 2, 3, 4])) # -> [1, 2, 6, 24]\n"
            "print(prefix_product([2, 5, 2]))    # -> [2, 10, 20]\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Iterates through the list of n numbers accumulating the running product. Runs in O(n) time and O(n) space."
        ),
    },
    {
        "id": "leaf_layers",
        "title": "156. leaf layers",
        "raw_title": "leaf layers",
        "category": "Mixed Recall",
        "description": (
            "Write a function, leaf_layers, that takes in the root of a binary tree. The function should return a 2D list where "
            "each sublist represents a 'leaf layer' of the tree.\n\n"
            "To get a leaf layer, take all leaf nodes in tree. Then, conceptually 'remove' them from the tree. This will create "
            "new 'leaves'. Repeat this process until the tree is empty."
        ),
        "examples": (
            "# Tree: a -> b, c; b -> d, e; c -> f\n"
            "leaf_layers(a) # -> [['d', 'e', 'f'], ['b', 'c'], ['a']]"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def leaf_layers(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n\n"
            "# === Bottom-Up Node Height Traversal (O(n)) ===\n"
            "def traverse(root, layers):\n"
            "    if root is None:\n"
            "        return -1\n\n"
            "    left_height = traverse(root.left, layers)\n"
            "    right_height = traverse(root.right, layers)\n"
            "    height = 1 + max(left_height, right_height)\n\n"
            "    if len(layers) == height:\n"
            "        layers.append([])\n\n"
            "    layers[height].append(root.val)\n"
            "    return height\n\n"
            "def leaf_layers(root):\n"
            "    layers = []\n"
            "    traverse(root, layers)\n"
            "    return layers\n\n\n"
            "# === Example Test Cases ===\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "d = Node('d')\n"
            "e = Node('e')\n"
            "f = Node('f')\n"
            "a.left = b; a.right = c; b.left = d; b.right = e; c.right = f\n"
            "print(leaf_layers(a))  # -> [['d', 'e', 'f'], ['b', 'c'], ['a']]\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Performs post-order traversal computing node heights from leaves upward to group into layers. Runs in O(n) time and O(n) space."
        ),
    },
    {
        "id": "max_increasing_subseq",
        "title": "157. max increasing subseq",
        "raw_title": "max increasing subseq",
        "category": "Mixed Recall",
        "description": (
            "Write a function, max_increasing_subseq, that takes in a list of numbers as an argument. The function should return "
            "the length of the longest subsequence of strictly increasing numbers.\n\n"
            "A subsequence of a list can be created by deleting any items of the list, while maintaining the relative order of items."
        ),
        "examples": (
            "max_increasing_subseq([4, 18, 20, 10, 12, 15, 19]) # -> 5 ([4, 10, 12, 15, 19])\n"
            "max_increasing_subseq([1, 2, 3])                   # -> 3"
        ),
        "starter_code": (
            "def max_increasing_subseq(numbers):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Longest Increasing Subsequence with Memoization (O(n^2)) ===\n"
            "def _max_increasing_subseq(numbers, i, previous, memo):\n"
            "    key = (i, previous)\n"
            "    if key in memo:\n"
            "        return memo[key]\n\n"
            "    if i == len(numbers):\n"
            "        return 0\n\n"
            "    current = numbers[i]\n"
            "    options = []\n"
            "    dont_take_current = _max_increasing_subseq(numbers, i + 1, previous, memo)\n"
            "    options.append(dont_take_current)\n\n"
            "    if current > previous:\n"
            "        take_current = 1 + _max_increasing_subseq(numbers, i + 1, current, memo)\n"
            "        options.append(take_current)\n\n"
            "    memo[key] = max(options)\n"
            "    return memo[key]\n\n"
            "def max_increasing_subseq(numbers):\n"
            "    return _max_increasing_subseq(numbers, 0, float('-inf'), {})\n\n\n"
            "# === Example Test Cases ===\n"
            "print(max_increasing_subseq([4, 18, 20, 10, 12, 15, 19])) # -> 5\n"
            "print(max_increasing_subseq([1, 2, 3]))                   # -> 3\n"
        ),
        "time_complexity": "O(n^2)",
        "space_complexity": "O(n^2)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Dynamic programming branching on taking or skipping each element, memoized on (index, previous_value). Runs in O(n^2) time and space."
        ),
    },
    {
        "id": "knightly_number",
        "title": "158. knightly number",
        "raw_title": "knightly number",
        "category": "Mixed Recall",
        "description": (
            "A knight is on a chess board. Can you figure out the total number of ways the knight can move to a target position "
            "in exactly m moves? A knight moves in standard 'L' shapes (eight possible positions).\n\n"
            "Write a function, knightly_number, that takes in 6 arguments: n, m, kr, kc, pr, pc.\n"
            "- n = length of the chess board (n x n, 0-indexed)\n"
            "- m = exact number of moves to use\n"
            "- kr, kc = starting coordinates of the knight\n"
            "- pr, pc = target coordinates\n\n"
            "The function should return the number of unique paths the knight can travel to reach target in exactly m moves."
        ),
        "examples": (
            "knightly_number(8, 2, 4, 4, 5, 5) # -> 2\n"
            "knightly_number(8, 2, 7, 7, 5, 6) # -> 1"
        ),
        "starter_code": (
            "def knightly_number(n, m, kr, kc, pr, pc):\n"
            "  pass # todo\n\n"
            "knightlyNumber = knightly_number\n"
        ),
        "solution_code": (
            "# === Knight Moves Count via DP with Memoization (O(m * n^2)) ===\n"
            "def _knightly_number(n, m, kr, kc, pr, pc, memo):\n"
            "    key = (m, kr, kc)\n"
            "    if key in memo:\n"
            "        return memo[key]\n\n"
            "    if kr < 0 or kr >= n or kc < 0 or kc >= n:\n"
            "        return 0\n\n"
            "    if m == 0:\n"
            "        return 1 if (kr, kc) == (pr, pc) else 0\n\n"
            "    neighbors = [\n"
            "        (kr + 2, kc + 1),\n"
            "        (kr - 2, kc + 1),\n"
            "        (kr + 2, kc - 1),\n"
            "        (kr - 2, kc - 1),\n"
            "        (kr + 1, kc + 2),\n"
            "        (kr - 1, kc + 2),\n"
            "        (kr + 1, kc - 2),\n"
            "        (kr - 1, kc - 2),\n"
            "    ]\n\n"
            "    count = 0\n"
            "    for neighbor_row, neighbor_col in neighbors:\n"
            "        count += _knightly_number(n, m - 1, neighbor_row, neighbor_col, pr, pc, memo)\n\n"
            "    memo[key] = count\n"
            "    return count\n\n"
            "def knightly_number(n, m, kr, kc, pr, pc):\n"
            "    return _knightly_number(n, m, kr, kc, pr, pc, {})\n\n"
            "knightlyNumber = knightly_number\n\n\n"
            "# === Example Test Cases ===\n"
            "print(knightly_number(8, 2, 4, 4, 5, 5)) # -> 2\n"
        ),
        "time_complexity": "O(m * n^2)",
        "space_complexity": "O(m * n^2)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Recursively counts valid knight paths bounded by m moves using memoization on (moves_left, row, col). Runs in O(m * n^2) time and space."
        ),
    },
    {
        "id": "all_trips",
        "title": "159. all trips",
        "raw_title": "all trips",
        "category": "Mixed Recall",
        "description": (
            "You are given a list of bus routes, a starting station, and an ending station. A bus route is a pair of two stations "
            "(a, b) such that the bus travels from a to b, but not from b to a.\n\n"
            "Write a function, all_trips, that returns a list containing all possible trips that travel from start to end station. "
            "You can assume that there are no cycles in the bus routes (DAG)."
        ),
        "examples": (
            "routes = [('a', 'b'), ('b', 'c'), ('a', 'c')]\n"
            "all_trips(routes, 'a', 'c') # -> [['a', 'b', 'c'], ['a', 'c']]"
        ),
        "starter_code": (
            "def all_trips(routes, start_station, end_station):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Exhaustive Path Search in DAG (O(2^V)) ===\n"
            "def get_paths(graph, src, dst):\n"
            "    if src == dst:\n"
            "        return [[src]]\n\n"
            "    all_paths = []\n"
            "    for neighbor in graph[src]:\n"
            "        neighbor_paths = get_paths(graph, neighbor, dst)\n"
            "        for neighbor_path in neighbor_paths:\n"
            "            neighbor_path.append(src)\n"
            "            all_paths.append(neighbor_path)\n"
            "    return all_paths\n\n"
            "def build_graph(edges):\n"
            "    graph = {}\n"
            "    for edge in edges:\n"
            "        a, b = edge\n"
            "        if a not in graph:\n"
            "            graph[a] = []\n"
            "        if b not in graph:\n"
            "            graph[b] = []\n"
            "        graph[a].append(b)\n"
            "    return graph\n\n"
            "def all_trips(routes, start_station, end_station):\n"
            "    graph = build_graph(routes)\n"
            "    paths = get_paths(graph, start_station, end_station)\n"
            "    return [path[::-1] for path in paths]\n\n\n"
            "# === Example Test Cases ===\n"
            "routes = [('a', 'b'), ('b', 'c'), ('a', 'c')]\n"
            "print(all_trips(routes, 'a', 'c'))  # -> [['a', 'b', 'c'], ['a', 'c']]\n"
        ),
        "time_complexity": "O(2^V)",
        "space_complexity": "O(2^V)",
        "complexity_type": "O(2^n)",
        "complexity_explanation": (
            "Recursively explores all possible trips from starting station to ending station in a DAG. Runs in O(2^V) time in worst case."
        ),
    },
    {
        "id": "has_path_sum",
        "title": "160. has path sum",
        "raw_title": "has path sum",
        "category": "Mixed Recall",
        "description": (
            "Write a function, has_path_sum, that takes in the root of a binary tree and a target number. "
            "The function should return a boolean indicating whether or not there is a path through the tree that sums to the target.\n\n"
            "A path must begin at the root and end at a leaf node."
        ),
        "examples": (
            "# Tree: 5 -> 4, 8; 4 -> 11\n"
            "has_path_sum(root, 20) # -> True (5 + 4 + 11 = 20)\n"
            "has_path_sum(root, 100) # -> False"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def has_path_sum(root, target):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n\n"
            "# === Root-to-Leaf Path Sum Verification (O(n)) ===\n"
            "def has_path_sum(root, target):\n"
            "    if root is None:\n"
            "        return False\n\n"
            "    if root.left is None and root.right is None and root.val == target:\n"
            "        return True\n\n"
            "    return has_path_sum(root.left, target - root.val) or has_path_sum(root.right, target - root.val)\n\n\n"
            "# === Example Test Cases ===\n"
            "a = Node(5)\n"
            "b = Node(4)\n"
            "c = Node(8)\n"
            "d = Node(11)\n"
            "a.left = b; a.right = c; b.left = d\n"
            "print(has_path_sum(a, 20))  # -> True\n"
            "print(has_path_sum(a, 100)) # -> False\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(h)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Traverses the tree to leaf nodes subtracting values from target. Runs in O(n) time and O(h) space where h is tree height."
        ),
    },
    {
        "id": "knapsack",
        "title": "161. knapsack",
        "raw_title": "knapsack",
        "category": "Mixed Recall",
        "description": (
            "Write a function, knapsack, that takes in a list of item values, a list of item weights, and a weight limit. "
            "The i-th item has a value of values[i] and a weight of weights[i].\n\n"
            "Your job is to pick items to pack into your knapsack so that its total weight does not exceed the limit and the value "
            "of the items is maximized. You may either take an item once or not at all. Return the maximum total value."
        ),
        "examples": (
            "knapsack([1, 6, 10, 16], [1, 2, 3, 5], 7) # -> 22 (items 6 + 16)\n"
            "knapsack([1, 2, 3], [1, 2, 3], 0)         # -> 0"
        ),
        "starter_code": (
            "def knapsack(values, weights, weight_limit):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === 0/1 Knapsack Dynamic Programming (O(n * w)) ===\n"
            "def _knapsack(values, weights, weight_limit, i, memo):\n"
            "    if weight_limit < 0:\n"
            "        return -float('inf')\n\n"
            "    if i == len(values):\n"
            "        return 0\n\n"
            "    key = (weight_limit, i)\n"
            "    if key in memo:\n"
            "        return memo[key]\n\n"
            "    memo[key] = max(\n"
            "        values[i] + _knapsack(values, weights, weight_limit - weights[i], i + 1, memo),\n"
            "        _knapsack(values, weights, weight_limit, i + 1, memo)\n"
            "    )\n"
            "    return memo[key]\n\n"
            "def knapsack(values, weights, weight_limit):\n"
            "    return _knapsack(values, weights, weight_limit, 0, {})\n\n\n"
            "# === Example Test Cases ===\n"
            "print(knapsack([1, 6, 10, 16], [1, 2, 3, 5], 7)) # -> 22\n"
            "print(knapsack([1, 2, 3], [1, 2, 3], 0))         # -> 0\n"
        ),
        "time_complexity": "O(n * w)",
        "space_complexity": "O(n * w)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Classical 0/1 knapsack dynamic programming with memoization on (weight_limit, item_index). Runs in O(n * w) time and space."
        ),
    },
    {
        "id": "virus_spread",
        "title": "162. virus spread",
        "raw_title": "virus spread",
        "category": "Mixed Recall",
        "description": (
            "Oh no! There is a computer virus going around in our data center. The virus spreads to adjacent computers.\n\n"
            "Write a function, virus_spread, that takes in a grid. In the grid, 0's are empty spaces, 1's are clean computers, "
            "and 2's are infected computers. Every hour, the virus spreads from infected computers to immediately adjacent clean "
            "computers (up, down, left, right).\n\n"
            "The function should return the number of hours it will take for all computers to be infected. "
            "If it is impossible for all computers to become infected, return -1."
        ),
        "examples": (
            "grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]\n"
            "virus_spread(grid) # -> 4\n"
            "grid2 = [[2, 1, 1], [0, 1, 1], [1, 0, 1]]\n"
            "virus_spread(grid2) # -> -1"
        ),
        "starter_code": (
            "def virus_spread(grid):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import deque\n\n\n"
            "# === Multi-Source Breadth-First Search (O(r * c)) ===\n"
            "def virus_spread(grid):\n"
            "    clean_computers = 0\n"
            "    queue = deque([])\n"
            "    visited = set()\n"
            "    for r in range(0, len(grid)):\n"
            "        for c in range(0, len(grid[0])):\n"
            "            if grid[r][c] == 1:\n"
            "                clean_computers += 1\n"
            "            elif grid[r][c] == 2:\n"
            "                visited.add((r, c))\n"
            "                queue.append((r, c, 0))\n\n"
            "    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]\n"
            "    max_t = 0\n"
            "    while queue:\n"
            "        r, c, t = queue.popleft()\n"
            "        max_t = t\n"
            "        for delta in deltas:\n"
            "            delta_r, delta_c = delta\n"
            "            neighbor_r = r + delta_r\n"
            "            neighbor_c = c + delta_c\n"
            "            neighbor_pos = (neighbor_r, neighbor_c)\n"
            "            if 0 <= neighbor_r < len(grid) and 0 <= neighbor_c < len(grid[0]) and grid[neighbor_r][neighbor_c] != 0 and neighbor_pos not in visited:\n"
            "                clean_computers -= 1\n"
            "                visited.add(neighbor_pos)\n"
            "                queue.append((*neighbor_pos, t + 1))\n\n"
            "    if clean_computers > 0:\n"
            "        return -1\n"
            "    else:\n"
            "        return max_t\n\n\n"
            "# === Example Test Cases ===\n"
            "grid = [[2, 1, 1], [1, 1, 0], [0, 1, 1]]\n"
            "print(virus_spread(grid))  # -> 4\n"
        ),
        "time_complexity": "O(r * c)",
        "space_complexity": "O(r * c)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Multi-source breadth-first search across all cells of the grid tracking infection levels per hour. Runs in O(r * c) time and space."
        ),
    },
    {
        "id": "positioning_plants",
        "title": "163. positioning plants",
        "raw_title": "positioning plants",
        "category": "Mixed Recall",
        "description": (
            "You've been hired to plant flowers in a garden with n different positions. There are m different flower types. "
            "Prices vary depending on which position they are planted. Never plant two of the same flower type right next to each other.\n\n"
            "Write a function, positioning_plants, that takes in a 2D list of dimensions n * m where costs[i][j] represents the cost of "
            "planting flower type j at position i. Return the minimum cost of planting flowers without adjacent identical types."
        ),
        "examples": (
            "costs = [[4, 3, 7], [6, 1, 9], [2, 5, 3]]\n"
            "positioning_plants(costs) # -> 7 (3 + 1 + 3 = 7)"
        ),
        "starter_code": (
            "def positioning_plants(costs):\n"
            "  pass # todo\n\n"
            "positioningPlants = positioning_plants\n"
        ),
        "solution_code": (
            "# === Dynamic Programming with Memoization (O(n * m)) ===\n"
            "def _positioning_plants(costs, pos, last_plant, memo):\n"
            "    key = (pos, last_plant)\n"
            "    if key in memo:\n"
            "        return memo[key]\n\n"
            "    if pos == len(costs):\n"
            "        return 0\n\n"
            "    min_cost = float('inf')\n"
            "    for plant, cost in enumerate(costs[pos]):\n"
            "        if plant != last_plant:\n"
            "            candidate = cost + _positioning_plants(costs, pos + 1, plant, memo)\n"
            "            min_cost = min(candidate, min_cost)\n\n"
            "    memo[key] = min_cost\n"
            "    return min_cost\n\n"
            "def positioning_plants(costs):\n"
            "    return _positioning_plants(costs, 0, None, {})\n\n"
            "positioningPlants = positioning_plants\n\n\n"
            "# === Example Test Cases ===\n"
            "costs = [[4, 3, 7], [6, 1, 9], [2, 5, 3]]\n"
            "print(positioning_plants(costs))  # -> 7\n"
        ),
        "time_complexity": "O(n * m)",
        "space_complexity": "O(n * m)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Dynamic programming with memoization on (position, last_plant_type) choosing the minimum cost flower. Runs in O(n * m) time and space."
        ),
    },
    {
        "id": "flatten_tree",
        "title": "164. flatten tree",
        "raw_title": "flatten tree",
        "category": "Mixed Recall",
        "description": (
            "Write a function, flatten_tree, that takes in the root of a binary tree. The function should modify the binary tree "
            "by flattening it into a 'linked-list' using the same tree nodes.\n\n"
            "In the resulting linked list, left pointers should be null and right pointers should point to the next node in preorder. "
            "Your function should return the root/head of the list."
        ),
        "examples": (
            "# Tree: a -> b, c; b -> d, e; c -> f\n"
            "# Flattened right pointers: a -> b -> d -> e -> c -> f\n"
            "flatten_tree(a) # -> root a with linked list structure"
        ),
        "starter_code": (
            "class Node:\n"
            "  def __init__(self, val):\n"
            "    self.val = val\n"
            "    self.left = None\n"
            "    self.right = None\n\n"
            "def flatten_tree(root):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "class Node:\n"
            "    def __init__(self, val):\n"
            "        self.val = val\n"
            "        self.left = None\n"
            "        self.right = None\n\n\n"
            "# === In-Place Preorder Flattening with Stack (O(n)) ===\n"
            "def flatten_tree(root):\n"
            "    prev = None\n"
            "    stack = [root]\n"
            "    while stack:\n"
            "        current = stack.pop()\n"
            "        if prev is not None:\n"
            "            prev.right = current\n"
            "        prev = current\n\n"
            "        if current.right is not None:\n"
            "            stack.append(current.right)\n"
            "        if current.left is not None:\n"
            "            stack.append(current.left)\n\n"
            "        current.left = None\n"
            "        current.right = None\n\n"
            "    return root\n\n\n"
            "# === Example Test Cases ===\n"
            "a = Node('a')\n"
            "b = Node('b')\n"
            "c = Node('c')\n"
            "a.left = b; a.right = c\n"
            "flat = flatten_tree(a)\n"
            "print(flat.val, '->', flat.right.val, '->', flat.right.right.val) # -> a -> b -> c\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Iterative preorder traversal using a stack to rewire right pointers in-place into a linked list. Runs in O(n) time and O(n) space."
        ),
    },
    {
        "id": "best_house_build",
        "title": "165. best house build",
        "raw_title": "best house build",
        "category": "Mixed Recall",
        "description": (
            "You are building a new house in the neighborhood and want to choose an empty location so that the house is as close "
            "as possible to all other houses.\n\n"
            "Write a function, best_house_build, that takes in a grid. In the grid, 0's are empty spaces, 1's are houses, and 2's are trees. "
            "Find an empty space with the shortest total travel distance to all houses. You cannot pass through houses or trees.\n\n"
            "Return the shortest total travel distance, or -1 if no empty space can reach all houses."
        ),
        "examples": (
            "grid = [[1, 0, 2, 0, 1], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0]]\n"
            "best_house_build(grid) # -> 7"
        ),
        "starter_code": (
            "def best_house_build(grid):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "from collections import deque, defaultdict\n\n\n"
            "# === Multi-Source Breadth-First Search from Houses (O(h * r * c)) ===\n"
            "def best_house_build(grid):\n"
            "    queue = deque()\n"
            "    visited = defaultdict(set)\n"
            "    total_distance = defaultdict(int)\n"
            "    for r in range(len(grid)):\n"
            "        for c in range(len(grid[0])):\n"
            "            if grid[r][c] == 1:\n"
            "                queue.append(((r, c, 0), (r, c)))\n"
            "                visited[(r, c)].add((r, c))\n\n"
            "    num_houses = len(queue)\n"
            "    deltas = [(1, 0), (0, 1), (-1, 0), (0, -1)]\n"
            "    while len(queue):\n"
            "        pos, src = queue.popleft()\n"
            "        r, c, dist = pos\n"
            "        for delta in deltas:\n"
            "            delta_r, delta_c = delta\n"
            "            new_r = r + delta_r\n"
            "            new_c = c + delta_c\n"
            "            new_pos = (new_r, new_c)\n"
            "            r_inbounds = 0 <= new_r < len(grid)\n"
            "            c_inbounds = 0 <= new_c < len(grid[0])\n"
            "            if r_inbounds and c_inbounds and src not in visited[new_pos] and grid[new_r][new_c] == 0:\n"
            "                visited[new_pos].add(src)\n"
            "                queue.append(((new_r, new_c, dist + 1), src))\n"
            "                total_distance[new_pos] += dist + 1\n\n"
            "    min_dist = float('inf')\n"
            "    for pos in visited:\n"
            "        if len(visited[pos]) == num_houses:\n"
            "            if total_distance[pos] > 0 and total_distance[pos] < min_dist:\n"
            "                min_dist = total_distance[pos]\n"
            "    return min_dist if min_dist != float('inf') else -1\n\n\n"
            "# === Example Test Cases ===\n"
            "grid = [[1, 0, 2, 0, 1], [0, 0, 0, 0, 0], [0, 0, 1, 0, 0]]\n"
            "print(best_house_build(grid))  # -> 7\n"
        ),
        "time_complexity": "O(h * r * c)",
        "space_complexity": "O(h * r * c)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Multi-source BFS from all house positions accumulating distance sums to each reachable empty space. Runs in O(h * r * c) time and space."
        ),
    },
    {
        "id": "breaking_boundaries",
        "title": "166. breaking boundaries",
        "raw_title": "breaking boundaries",
        "category": "Mixed Recall",
        "description": (
            "Write a function, breaking_boundaries, that takes in 5 arguments: m (rows), n (cols), k (max moves), r (start row), c (start col).\n\n"
            "Say you were situated in an m * n grid. In how many different ways could you move out of bounds if you could take at most k moves? "
            "A single move is 1 step up, down, left, or right. During a path you may revisit positions."
        ),
        "examples": (
            "breaking_boundaries(3, 4, 2, 0, 0) # -> 4 (left, up, right-up, down-left)\n"
            "breaking_boundaries(2, 2, 2, 0, 0) # -> 6"
        ),
        "starter_code": (
            "def breaking_boundaries(m, n, k, r, c):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === 4-Directional Out-of-Bounds DP with Memoization (O(m * n * k)) ===\n"
            "def _breaking_boundaries(m, n, k, r, c, memo):\n"
            "    key = (k, r, c)\n"
            "    if key in memo:\n"
            "        return memo[key]\n\n"
            "    row_inbounds = 0 <= r < m\n"
            "    col_inbounds = 0 <= c < n\n"
            "    if not row_inbounds or not col_inbounds:\n"
            "        return 1\n\n"
            "    if k == 0:\n"
            "        return 0\n\n"
            "    count = 0\n"
            "    deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]\n"
            "    for delta in deltas:\n"
            "        d_row, d_col = delta\n"
            "        count += _breaking_boundaries(m, n, k - 1, r + d_row, c + d_col, memo)\n\n"
            "    memo[key] = count\n"
            "    return count\n\n"
            "def breaking_boundaries(m, n, k, r, c):\n"
            "    return _breaking_boundaries(m, n, k, r, c, {})\n\n\n"
            "# === Example Test Cases ===\n"
            "print(breaking_boundaries(3, 4, 2, 0, 0)) # -> 4\n"
            "print(breaking_boundaries(2, 2, 2, 0, 0)) # -> 6\n"
        ),
        "time_complexity": "O(m * n * k)",
        "space_complexity": "O(m * n * k)",
        "complexity_type": "O(n^2)",
        "complexity_explanation": (
            "Dynamic programming with memoization across (remaining_moves, row, col) counting paths stepping outside boundary. Runs in O(m * n * k) time and space."
        ),
    },
    {
        "id": "token_replace",
        "title": "167. token replace",
        "raw_title": "token replace",
        "category": "Mixed Recall",
        "description": (
            "Write a function, token_replace, that takes in a dictionary of tokens and a string. "
            "The function should return a new string where tokens are replaced from left to right.\n\n"
            "Tokens are enclosed in a pair of '$'. The input string is properly formatted and '$' is not used except to enclose a token."
        ),
        "examples": (
            "tokens = {'$second$': 'beta', '$first$': 'alpha', '$third$': 'gamma'}\n"
            "token_replace('$first$second$third$', tokens) # -> 'alphasecondgamma'"
        ),
        "starter_code": (
            "def token_replace(s, tokens):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Two-Pointer Token Replacement (O(n)) ===\n"
            "def token_replace(s, tokens):\n"
            "    output = []\n"
            "    i = 0\n"
            "    j = 1\n"
            "    while i < len(s):\n"
            "        if s[i] != '$':\n"
            "            output.append(s[i])\n"
            "            i += 1\n"
            "            j = i + 1\n"
            "        elif s[j] != '$':\n"
            "            j += 1\n"
            "        else:\n"
            "            key = s[i: j + 1]\n"
            "            output.append(tokens[key])\n"
            "            i = j + 1\n"
            "            j = i + 1\n"
            "    return ''.join(output)\n\n\n"
            "# === Example Test Cases ===\n"
            "tokens = {'$second$': 'beta', '$first$': 'alpha', '$third$': 'gamma'}\n"
            "print(token_replace('$first$second$third$', tokens)) # -> 'alphasecondgamma'\n"
        ),
        "time_complexity": "O(n)",
        "space_complexity": "O(n)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Scans the string with two pointers extracting and replacing delimited tokens from the dictionary. Runs in O(n) time and O(n) space."
        ),
    },
    {
        "id": "token_transform",
        "title": "168. token transform",
        "raw_title": "token transform",
        "category": "Mixed Recall",
        "description": (
            "Write a function, token_transform, that takes in a dictionary of tokens and a string. "
            "In the dictionary, the replacement values for a token may reference other tokens.\n\n"
            "The function should return a new string where tokens are replaced with their fully evaluated string values. "
            "You may assume there are no circular token dependencies."
        ),
        "examples": (
            "tokens = {'$0$': '$1$', '$1$': '$2$', '$2$': 'success'}\n"
            "token_transform('Result: $0$', tokens) # -> 'Result: success'"
        ),
        "starter_code": (
            "def token_transform(s, tokens):\n"
            "  pass # todo\n"
        ),
        "solution_code": (
            "# === Recursive Token Expansion with Memoization (O(n * d)) ===\n"
            "def token_transform(s, tokens):\n"
            "    output = []\n"
            "    i = 0\n"
            "    j = 1\n"
            "    while i < len(s):\n"
            "        if s[i] != '$':\n"
            "            output.append(s[i])\n"
            "            i += 1\n"
            "            j = i + 1\n"
            "        elif s[j] != '$':\n"
            "            j += 1\n"
            "        else:\n"
            "            key = s[i:j + 1]\n"
            "            value = tokens[key]\n"
            "            evaluated_value = token_transform(value, tokens)\n"
            "            tokens[key] = evaluated_value\n"
            "            output.append(evaluated_value)\n"
            "            i = j + 1\n"
            "            j = i + 1\n"
            "    return ''.join(output)\n\n\n"
            "# === Example Test Cases ===\n"
            "tokens = {'$0$': '$1$', '$1$': '$2$', '$2$': 'success'}\n"
            "print(token_transform('Result: $0$', tokens)) # -> 'Result: success'\n"
        ),
        "time_complexity": "O(n * d)",
        "space_complexity": "O(n * d)",
        "complexity_type": "O(n)",
        "complexity_explanation": (
            "Recursively resolves and memoizes nested token definitions across reference chains. Runs in O(n * d) time and space where d is dependency depth."
        ),
    },
]


# ==========================================================
# Aesthetic Big-O Complexity Graph Widget
# ==========================================================
class BigOGraphWidget(QWidget):
    """
    Renders an aesthetic vector comparison chart of standard Big-O curves,
    highlighting the active problem's time complexity.
    """
    def __init__(self, highlight_id="O(n)", theme=DARK_THEME, parent=None):
        super().__init__(parent)
        self.highlight_id = highlight_id
        self.current_theme = theme
        self.setMinimumHeight(290)
        self.setMaximumHeight(330)
        self.setMaximumWidth(700)

        # Standard complexity curves definition
        self.curves = [
            {
                "id": "O(1)",
                "label": "O(1) - Constant",
                "tag": "Excellent",
                "color": QColor("#10b981"),  # Emerald Green
                "fn": lambda t: 0.05,
            },
            {
                "id": "O(log n)",
                "label": "O(log n) - Logarithmic",
                "tag": "Good",
                "color": QColor("#06b6d4"),  # Cyan
                "fn": lambda t: 0.22 * (math.log(1 + 15 * t) / math.log(16)),
            },
            {
                "id": "O(sqrt(n))",
                "label": "O(√n) - Sublinear",
                "tag": "Good",
                "color": QColor("#38bdf8"),  # Sky Blue
                "fn": lambda t: 0.36 * math.sqrt(t),
            },
            {
                "id": "O(n)",
                "label": "O(n) - Linear",
                "tag": "Fair",
                "color": QColor("#eab308"),  # Amber / Yellow
                "fn": lambda t: 0.54 * t,
            },
            {
                "id": "O(n log n)",
                "label": "O(n log n) - Linearithmic",
                "tag": "Moderate",
                "color": QColor("#f97316"),  # Orange
                "fn": lambda t: 0.76 * t * (math.log(1 + 7 * t) / math.log(8)),
            },
            {
                "id": "O(n^2)",
                "label": "O(n²) - Quadratic",
                "tag": "Horrible",
                "color": QColor("#ef4444"),  # Red
                "fn": lambda t: 0.96 * (t ** 2),
            },
            {
                "id": "O(2^n)",
                "label": "O(2ⁿ) - Exponential",
                "tag": "Infeasible",
                "color": QColor("#dc2626"),  # Crimson
                "fn": lambda t: min(1.0, 0.06 * (2 ** (4.5 * t) - 1)),
            },
        ]

    def set_highlight(self, highlight_id):
        self.highlight_id = highlight_id
        self.update()

    def apply_theme(self, theme):
        self.current_theme = theme
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setRenderHint(QPainter.RenderHint.TextAntialiasing)

        w = self.width()
        h = self.height()
        is_dark = self.current_theme.get("name", "dark") == "dark"

        # 1. Background card fill with rounded rect & subtle border
        card_rect = QRectF(0.5, 0.5, w - 1.0, h - 1.0)
        bg_color = QColor(self.current_theme.get("table_bg", "#141416"))
        border_color = QColor(self.current_theme.get("border_color", "#27272a"))
        painter.setPen(QPen(border_color, 1))
        painter.setBrush(QBrush(bg_color))
        painter.drawRoundedRect(card_rect, 8, 8)

        # Plot boundaries
        x0 = 55
        y0 = h - 36
        plot_w = w - 165
        plot_h = h - 68

        # 2. Horizontal Complexity Tier Zones (Subtle heat map backdrop)
        # Zone 1: Safe / Optimal (0 - 30% of height)
        opt_y = y0 - 0.30 * plot_h
        opt_h = 0.30 * plot_h
        painter.fillRect(QRectF(x0, opt_y, plot_w, opt_h), QColor(16, 185, 129, 12 if is_dark else 18))

        # Zone 2: Fair / Moderate (30% - 65% of height)
        fair_y = y0 - 0.65 * plot_h
        fair_h = 0.35 * plot_h
        painter.fillRect(QRectF(x0, fair_y, plot_w, fair_h), QColor(234, 179, 8, 10 if is_dark else 15))

        # Zone 3: Danger / Horrible (65% - 100% of height)
        bad_y = y0 - plot_h
        bad_h = 0.35 * plot_h
        painter.fillRect(QRectF(x0, bad_y, plot_w, bad_h), QColor(239, 68, 68, 12 if is_dark else 18))

        # Zone faint watermark labels inside the plot
        painter.setFont(QFont("SF Pro Text", 8, QFont.Weight.Bold))
        painter.setPen(QPen(QColor(239, 68, 68, 65 if is_dark else 85)))
        painter.drawText(x0 + 14, int(bad_y + 16), "HIGH COMPLEXITY ZONE")

        painter.setPen(QPen(QColor(234, 179, 8, 60 if is_dark else 80)))
        painter.drawText(x0 + 14, int(fair_y + 16), "MODERATE COMPLEXITY ZONE")

        painter.setPen(QPen(QColor(16, 185, 129, 65 if is_dark else 85)))
        painter.drawText(x0 + 14, int(opt_y + 16), "OPTIMAL / SCALABLE ZONE")

        # 3. Subtle Grid Lines (Zone boundaries and vertical partitions)
        grid_pen = QPen(QColor(255, 255, 255, 20) if is_dark else QColor(0, 0, 0, 20), 1, Qt.PenStyle.DashLine)
        painter.setPen(grid_pen)
        painter.drawLine(x0, int(opt_y), x0 + plot_w, int(opt_y))
        painter.drawLine(x0, int(fair_y), x0 + plot_w, int(fair_y))
        for step in (0.25, 0.5, 0.75):
            gx = int(x0 + step * plot_w)
            painter.drawLine(gx, y0, gx, y0 - plot_h)

        # 4. Axes
        axis_pen = QPen(border_color, 1.5)
        painter.setPen(axis_pen)
        painter.drawLine(x0, y0, x0 + plot_w + 10, y0)
        painter.drawLine(x0, y0, x0, y0 - plot_h - 10)

        # Arrowheads
        painter.setBrush(QBrush(border_color))
        arrow_x = [QPointF(x0 + plot_w + 15, y0), QPointF(x0 + plot_w + 8, y0 - 4), QPointF(x0 + plot_w + 8, y0 + 4)]
        painter.drawPolygon(arrow_x)
        arrow_y = [QPointF(x0, y0 - plot_h - 15), QPointF(x0 - 4, y0 - plot_h - 8), QPointF(x0 + 4, y0 - plot_h - 8)]
        painter.drawPolygon(arrow_y)

        # Axis Labels
        painter.setFont(QFont("SF Pro Text", 9, QFont.Weight.Medium))
        painter.setPen(QPen(QColor(self.current_theme.get("table_header_text", "#71717a"))))
        painter.drawText(x0 + plot_w - 70, y0 + 22, "Elements (n) →")

        painter.save()
        painter.translate(x0 - 32, y0 - plot_h // 2 + 30)
        painter.rotate(-90)
        painter.drawText(0, 0, "Operations (Time) →")
        painter.restore()

        # 5. Draw Curves (Store endpoints for collision-free label placement)
        highlighted_curve = None
        end_labels = []

        for curve in self.curves:
            if curve["id"] == self.highlight_id:
                highlighted_curve = curve
                continue

            path = QPainterPath()
            path.moveTo(x0, y0)
            steps = 50
            last_pt = QPointF(x0, y0)
            for i in range(1, steps + 1):
                t = i / float(steps)
                val = curve["fn"](t)
                px = x0 + t * plot_w
                py = y0 - min(1.0, val) * plot_h
                path.lineTo(px, py)
                last_pt = QPointF(px, py)

            c_color = QColor(curve["color"])
            c_color.setAlpha(60 if is_dark else 80)
            painter.setPen(QPen(c_color, 1.6, Qt.PenStyle.DashLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawPath(path)

            lbl_color = QColor(curve["color"])
            lbl_color.setAlpha(125 if is_dark else 155)
            end_labels.append({
                "y": last_pt.y() + 4,
                "x": last_pt.x() + 8,
                "color": lbl_color,
                "text": curve["label"].split(" - ")[0],
                "font": QFont("SF Pro Text", 9),
                "is_active": False,
            })

        # 6. Draw Active / Highlighted Curve with Neon Glow & Gradient Fill
        if highlighted_curve:
            h_path = QPainterPath()
            h_path.moveTo(x0, y0)
            fill_path = QPainterPath()
            fill_path.moveTo(x0, y0)

            steps = 60
            last_pt = QPointF(x0, y0)
            marker_pt = QPointF(x0, y0)

            for i in range(1, steps + 1):
                t = i / float(steps)
                val = highlighted_curve["fn"](t)
                px = x0 + t * plot_w
                py = y0 - min(1.0, val) * plot_h
                h_path.lineTo(px, py)
                fill_path.lineTo(px, py)
                last_pt = QPointF(px, py)
                if i == int(steps * 0.70):
                    marker_pt = QPointF(px, py)

            fill_path.lineTo(last_pt.x(), y0)
            fill_path.lineTo(x0, y0)
            fill_path.closeSubpath()

            # Luminous Area Fill under curve
            fill_grad = QLinearGradient(x0, y0 - plot_h, x0, y0)
            c_top = QColor(highlighted_curve["color"])
            c_top.setAlpha(60 if is_dark else 75)
            c_bot = QColor(highlighted_curve["color"])
            c_bot.setAlpha(4)
            fill_grad.setColorAt(0.0, c_top)
            fill_grad.setColorAt(1.0, c_bot)
            painter.fillPath(fill_path, fill_grad)

            # Glow Layer 1 (Wide diffuse neon glow)
            glow1 = QColor(highlighted_curve["color"])
            glow1.setAlpha(32 if is_dark else 45)
            painter.setPen(QPen(glow1, 10, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawPath(h_path)

            # Glow Layer 2 (Medium neon glow)
            glow2 = QColor(highlighted_curve["color"])
            glow2.setAlpha(70 if is_dark else 85)
            painter.setPen(QPen(glow2, 5, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawPath(h_path)

            # Layer 3 (Vibrant crisp core stroke)
            core_pen = QColor(highlighted_curve["color"])
            painter.setPen(QPen(core_pen, 2.8, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin))
            painter.drawPath(h_path)

            end_labels.append({
                "y": last_pt.y() + 4,
                "x": last_pt.x() + 8,
                "color": core_pen,
                "text": highlighted_curve["label"],
                "font": QFont("SF Pro Text", 10, QFont.Weight.Bold),
                "is_active": True,
            })

            # Beacon Target Point
            halo_color = QColor(highlighted_curve["color"])
            halo_color.setAlpha(60 if is_dark else 80)
            painter.setBrush(QBrush(halo_color))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawEllipse(marker_pt, 10, 10)

            painter.setBrush(QBrush(core_pen))
            painter.drawEllipse(marker_pt, 6, 6)

            painter.setBrush(QBrush(QColor("#ffffff")))
            painter.drawEllipse(marker_pt, 3, 3)

            # Floating Callout Pill Badge: "★ Current: O(...)"
            callout_text = f"★ Current: {highlighted_curve['label'].split(' - ')[0]}"
            painter.setFont(QFont("SF Pro Text", 9, QFont.Weight.Bold))
            fm = painter.fontMetrics()
            tw = fm.horizontalAdvance(callout_text) + 18
            th = 22

            cx = max(x0 + 8.0, min(float(w - tw - 20), marker_pt.x() - tw / 2.0))
            cy = max(10.0, marker_pt.y() - 34.0)

            bubble_rect = QRectF(cx, cy, tw, th)
            painter.setBrush(QBrush(core_pen))
            painter.setPen(QPen(QColor(255, 255, 255, 120), 1))
            painter.drawRoundedRect(bubble_rect, 6, 6)

            text_color = QColor("#ffffff" if is_dark or highlighted_curve["id"] != "O(n)" else "#18181b")
            painter.setPen(QPen(text_color))
            painter.drawText(bubble_rect, Qt.AlignmentFlag.AlignCenter, callout_text)

        # 7. Render Collision-Free End Labels
        end_labels.sort(key=lambda item: item["y"])
        min_spacing = 15
        for i in range(1, len(end_labels)):
            if end_labels[i]["y"] - end_labels[i-1]["y"] < min_spacing:
                end_labels[i]["y"] = end_labels[i-1]["y"] + min_spacing

        for lbl in end_labels:
            painter.setFont(lbl["font"])
            painter.setPen(QPen(lbl["color"]))
            painter.drawText(int(lbl["x"]), int(lbl["y"]), lbl["text"])

        painter.end()


# ==========================================================
# Big-O Complexity Dialog Window
# ==========================================================
class BigOComplexityDialog(QDialog):
    """
    Modal dialog illustrating where the current problem's time complexity
    falls on the Big-O scale with an intuitive vector graph and color legend.
    """
    def __init__(self, parent=None, problem=None, theme=DARK_THEME):
        super().__init__(parent)
        self.problem = problem or {}
        self.current_theme = theme
        self.setWindowTitle("Big-O Complexity Guide")
        self.resize(720, 560)
        self.setMinimumSize(620, 480)

        # Outer root layout: centers content if maximized or expanded
        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(18, 18, 18, 18)
        root_layout.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignTop)

        # Centered container with max width constraint
        self.container = QWidget()
        self.container.setMaximumWidth(700)
        layout = QVBoxLayout(self.container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(14)
        root_layout.addWidget(self.container)

        # 1. Header Card with Problem Complexity Info
        self.header_card = QFrame()
        self.header_card.setObjectName("headerCard")
        card_layout = QVBoxLayout(self.header_card)
        card_layout.setContentsMargins(16, 14, 16, 14)
        card_layout.setSpacing(10)

        # Title row
        title_row = QHBoxLayout()
        title_row.setSpacing(10)
        prob_name = self.problem.get("title", "Practice Problem")
        self.title_label = QLabel(f"Complexity Analysis • {prob_name}")
        self.title_label.setFont(QFont("SF Pro Display", 13, QFont.Weight.Bold))
        title_row.addWidget(self.title_label)
        title_row.addStretch()

        # Badges with Monotone Vector Icons
        t_comp = self.problem.get("time_complexity", "O(n)")
        s_comp = self.problem.get("space_complexity", "O(1)")

        # Time Pill
        self.time_pill = QFrame()
        self.time_pill.setObjectName("dialogTimePill")
        time_pill_l = QHBoxLayout(self.time_pill)
        time_pill_l.setContentsMargins(10, 5, 12, 5)
        time_pill_l.setSpacing(6)

        self.time_icon = QLabel()
        self.time_icon.setFixedSize(14, 14)
        self.time_icon.setScaledContents(True)
        time_pill_l.addWidget(self.time_icon)

        self.time_label = QLabel(f"Time: {t_comp}")
        self.time_label.setFont(QFont("SF Pro Text", 11, QFont.Weight.Bold))
        time_pill_l.addWidget(self.time_label)
        title_row.addWidget(self.time_pill)

        # Space Pill
        self.space_pill = QFrame()
        self.space_pill.setObjectName("dialogSpacePill")
        space_pill_l = QHBoxLayout(self.space_pill)
        space_pill_l.setContentsMargins(10, 5, 12, 5)
        space_pill_l.setSpacing(6)

        self.space_icon = QLabel()
        self.space_icon.setFixedSize(14, 14)
        self.space_icon.setScaledContents(True)
        space_pill_l.addWidget(self.space_icon)

        self.space_label = QLabel(f"Space: {s_comp}")
        self.space_label.setFont(QFont("SF Pro Text", 11, QFont.Weight.Bold))
        space_pill_l.addWidget(self.space_label)
        title_row.addWidget(self.space_pill)

        card_layout.addLayout(title_row)

        # Explanation text with comfortable line spacing and padding
        expl = self.problem.get(
            "complexity_explanation",
            "Calculates the asymptotic growth rate of execution time and auxiliary memory."
        )
        self.expl_label = QLabel(expl)
        self.expl_label.setFont(QFont("SF Pro Text", 11))
        self.expl_label.setWordWrap(True)
        card_layout.addWidget(self.expl_label)

        layout.addWidget(self.header_card)

        # 2. Graph Vector Canvas (Centered, max width 700px)
        highlight_key = self.problem.get("complexity_type", "O(n)")
        self.graph = BigOGraphWidget(highlight_id=highlight_key, theme=self.current_theme)
        layout.addWidget(self.graph)

        # 3. Legend Rating Spectrum Chips
        legend_row = QHBoxLayout()
        legend_row.setSpacing(8)

        chips_data = [
            ("O(1)", "Constant", "#10b981"),
            ("O(log n)", "Logarithmic", "#06b6d4"),
            ("O(n)", "Linear", "#eab308"),
            ("O(n log n)", "Linearithmic", "#f97316"),
            ("O(n²)", "Quadratic", "#ef4444"),
            ("O(2ⁿ)", "Exponential", "#dc2626"),
        ]

        active_id = self.problem.get("complexity_type", "O(n)")
        self.legend_chips = []
        for cid, cname, col in chips_data:
            is_active = (cid == active_id) or (cid == "O(n²)" and active_id == "O(n^2)") or (cid == "O(2ⁿ)" and active_id == "O(2^n)")
            chip = QLabel(f"● {cid}\n{cname}")
            chip.setFont(QFont("SF Pro Text", 9, QFont.Weight.Bold if is_active else QFont.Weight.Normal))
            chip.setAlignment(Qt.AlignmentFlag.AlignCenter)
            border_style = f"2px solid {col}" if is_active else "1px solid rgba(120, 120, 120, 0.25)"
            bg_style = "rgba(255, 255, 255, 0.09)" if is_active else "transparent"
            chip.setStyleSheet(f"""
                QLabel {{
                    border: {border_style};
                    background-color: {bg_style};
                    border-radius: 6px;
                    padding: 6px 6px;
                    color: {col};
                }}
            """)
            legend_row.addWidget(chip)
            self.legend_chips.append(chip)

        layout.addLayout(legend_row)

        # 4. Bottom Controls: Close Button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.close_btn = QPushButton("Got it")
        self.close_btn.setFont(QFont("SF Pro Text", 11, QFont.Weight.Bold))
        self.close_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.close_btn.setStyleSheet("""
            QPushButton {
                background-color: #2563eb;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 7px 22px;
            }
            QPushButton:hover {
                background-color: #1d4ed8;
            }
        """)
        self.close_btn.clicked.connect(self.accept)
        btn_layout.addWidget(self.close_btn)
        layout.addLayout(btn_layout)

        self.apply_theme(self.current_theme)

    def apply_theme(self, theme):
        self.current_theme = theme
        self.graph.apply_theme(theme)

        # High quality monotone SVG icons
        icon_color = theme.get("btn_clear_text", "#d4d4d8")
        self.time_icon.setPixmap(render_svg_pixmap(TIME_SVG, size=14, color=icon_color))
        self.space_icon.setPixmap(render_svg_pixmap(SPACE_SVG, size=14, color=icon_color))

        pill_style = f"""
            background-color: {theme['btn_clear_bg']};
            border: 1px solid {theme['btn_clear_border']};
            border-radius: 6px;
        """
        self.time_pill.setStyleSheet(pill_style)
        self.space_pill.setStyleSheet(pill_style)
        self.time_label.setStyleSheet(f"color: {theme['brand_color']}; font-weight: 600;")
        self.space_label.setStyleSheet(f"color: {theme['brand_color']}; font-weight: 600;")

        self.setStyleSheet(f"""
            QDialog {{
                background-color: {theme['window_bg']};
                color: {theme['brand_color']};
            }}
            QFrame#headerCard {{
                background-color: {theme['table_bg']};
                border: 1px solid {theme['border_color']};
                border-radius: 8px;
            }}
        """)
        self.title_label.setStyleSheet(f"color: {theme['brand_color']};")
        self.expl_label.setStyleSheet(f"color: {theme['table_text']};")


# ==========================================================
# Problem Description View (Right Panel Tab 1)
# ==========================================================
class ProblemDescriptionWidget(QWidget):
    def __init__(self, parent=None, theme=DARK_THEME):
        super().__init__(parent)
        self.setObjectName("problemDescriptionWidget")
        self.setAutoFillBackground(True)
        self.current_theme = theme

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setFrameShape(QFrame.Shape.NoFrame)

        self.container = QWidget()
        self.container.setObjectName("problemDescriptionContainer")
        self.container.setAutoFillBackground(True)
        self.container_layout = QVBoxLayout(self.container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(12)
        self.scroll.setWidget(self.container)

        # Title
        self.title_label = QLabel()
        self.title_label.setFont(QFont("SF Pro Display", 15, QFont.Weight.Bold))
        self.title_label.setWordWrap(True)
        self.container_layout.addWidget(self.title_label)

        # Badge Pill
        self.badge_label = QLabel("Practice Problem")
        self.badge_label.setFont(QFont("SF Pro Text", 10, QFont.Weight.Bold))
        self.badge_label.setStyleSheet("""
            background-color: #0284c7;
            color: #ffffff;
            border-radius: 6px;
            padding: 4px 10px;
            font-weight: 600;
        """)
        self.container_layout.addWidget(self.badge_label, alignment=Qt.AlignmentFlag.AlignLeft)

        # Description
        self.desc_label = QLabel()
        self.desc_label.setFont(QFont("SF Pro Text", 12))
        self.desc_label.setWordWrap(True)
        self.container_layout.addWidget(self.desc_label)

        # Examples Header
        self.examples_header = QLabel("Example Test Cases")
        self.examples_header.setFont(QFont("SF Pro Display", 12, QFont.Weight.Bold))
        self.container_layout.addWidget(self.examples_header)

        # Examples Box (Syntax-highlighted code block)
        self.examples_box = QPlainTextEdit()
        ex_font = get_code_font(size=12)
        self.examples_box.setFont(ex_font)
        self.examples_box.document().setDefaultFont(ex_font)
        self.examples_box.setReadOnly(True)
        self.examples_highlighter = PythonHighlighter(self.examples_box.document(), theme=self.current_theme)
        self.container_layout.addWidget(self.examples_box)

        self.container_layout.addStretch()
        layout.addWidget(self.scroll)

        self.apply_theme(self.current_theme)

    def set_problem(self, problem):
        self.title_label.setText(problem.get("title", ""))
        self.desc_label.setText(problem.get("description", ""))
        examples = problem.get("examples", "")
        self.examples_box.setPlainText(examples)
        line_count = len(examples.strip().splitlines()) if examples else 2
        target_height = max(60, min(180, line_count * 22 + 20))
        self.examples_box.setFixedHeight(target_height)

    def apply_font_size(self, size: int):
        ex_font = self.examples_box.font()
        ex_font.setPointSize(size)
        configure_no_ligatures(ex_font)
        self.examples_box.setFont(ex_font)
        self.examples_box.document().setDefaultFont(ex_font)

    def apply_theme(self, theme):
        self.current_theme = theme
        self.setStyleSheet(f"""
            QWidget#problemDescriptionWidget, QWidget#problemDescriptionContainer {{
                background-color: {theme['table_bg']};
            }}
            QLabel {{
                background-color: transparent;
            }}
        """)
        self.scroll.setStyleSheet(f"""
            QScrollArea {{
                background-color: {theme['table_bg']};
                border: none;
            }}
            QScrollArea > QWidget > QWidget {{
                background-color: {theme['table_bg']};
            }}
            {get_scrollbar_stylesheet(theme)}
        """)
        self.title_label.setStyleSheet(f"color: {theme['brand_color']}; font-weight: bold; background: transparent;")
        self.desc_label.setStyleSheet(f"color: {theme['table_text']}; font-size: 13px; line-height: 1.4; background: transparent;")
        self.examples_header.setStyleSheet(f"color: {theme['brand_color']}; font-weight: bold; margin-top: 6px; background: transparent;")
        self.examples_highlighter.apply_theme(theme)
        self.examples_box.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {theme['console_bg']};
                color: {theme['console_text']};
                border: 1px solid {theme['border_color']};
                border-radius: 6px;
                padding: 8px;
            }}
            {get_scrollbar_stylesheet(theme)}
        """)


# ==========================================================
# Problem Solution View (Right Panel Tab 2)
# ==========================================================
class ProblemSolutionWidget(QWidget):
    copy_to_editor_requested = Signal(str)

    def __init__(self, parent=None, theme=DARK_THEME):
        super().__init__(parent)
        self.setObjectName("problemSolutionWidget")
        self.setAutoFillBackground(True)
        self.current_theme = theme
        self.current_problem = {}
        self.current_solution = ""

        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(10)

        # 1. Top Header Row: "Solution Code" + "Copy to Editor"
        header_layout = QHBoxLayout()
        self.header_label = QLabel("Solution Code")
        self.header_label.setFont(QFont("SF Pro Display", 13, QFont.Weight.Bold))
        header_layout.addWidget(self.header_label)
        header_layout.addStretch()

        self.copy_btn = QPushButton("Copy to Editor")
        self.copy_btn.setFont(QFont("SF Pro Text", 11))
        self.copy_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.copy_btn.clicked.connect(self.on_copy_clicked)
        header_layout.addWidget(self.copy_btn)
        layout.addLayout(header_layout)

        # 2. Complexity Banner: Monotone Vector Pills & Big-O Chart Button
        self.complexity_bar = QFrame()
        self.complexity_bar.setObjectName("complexityBar")
        comp_layout = QHBoxLayout(self.complexity_bar)
        comp_layout.setContentsMargins(0, 2, 0, 2)
        comp_layout.setSpacing(8)

        # Time Pill (Monotone SVG icon + Text)
        self.time_pill = QFrame()
        self.time_pill.setObjectName("timePill")
        time_pill_layout = QHBoxLayout(self.time_pill)
        time_pill_layout.setContentsMargins(10, 5, 12, 5)
        time_pill_layout.setSpacing(7)

        self.time_icon = QLabel()
        self.time_icon.setFixedSize(14, 14)
        self.time_icon.setScaledContents(True)
        time_pill_layout.addWidget(self.time_icon)

        self.time_label = QLabel("Time: O(n)")
        self.time_label.setFont(QFont("SF Pro Text", 11, QFont.Weight.Bold))
        time_pill_layout.addWidget(self.time_label)
        comp_layout.addWidget(self.time_pill)

        # Space Pill (Monotone SVG icon + Text)
        self.space_pill = QFrame()
        self.space_pill.setObjectName("spacePill")
        space_pill_layout = QHBoxLayout(self.space_pill)
        space_pill_layout.setContentsMargins(10, 5, 12, 5)
        space_pill_layout.setSpacing(7)

        self.space_icon = QLabel()
        self.space_icon.setFixedSize(14, 14)
        self.space_icon.setScaledContents(True)
        space_pill_layout.addWidget(self.space_icon)

        self.space_label = QLabel("Space: O(1)")
        self.space_label.setFont(QFont("SF Pro Text", 11, QFont.Weight.Bold))
        space_pill_layout.addWidget(self.space_label)
        comp_layout.addWidget(self.space_pill)

        comp_layout.addStretch()

        # Big-O Chart Button
        self.complexity_btn = QPushButton("? Big-O Chart")
        self.complexity_btn.setFont(QFont("SF Pro Text", 11, QFont.Weight.Bold))
        self.complexity_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.complexity_btn.setToolTip("Click to view Big-O Complexity Graph comparison")
        self.complexity_btn.clicked.connect(self.open_complexity_dialog)
        comp_layout.addWidget(self.complexity_btn)

        layout.addWidget(self.complexity_bar)

        # 3. Code View
        self.solution_view = QPlainTextEdit()
        sol_font = get_code_font(size=13)
        self.solution_view.setFont(sol_font)
        self.solution_view.document().setDefaultFont(sol_font)
        self.solution_view.setReadOnly(True)
        self.highlighter = PythonHighlighter(self.solution_view.document(), theme=self.current_theme)
        layout.addWidget(self.solution_view)

        self.apply_theme(self.current_theme)

    def set_problem(self, problem):
        self.current_problem = problem
        self.current_solution = problem.get("solution_code", "")
        self.solution_view.setPlainText(self.current_solution)

        # Update Complexity labels
        t_comp = problem.get("time_complexity", "O(n)")
        s_comp = problem.get("space_complexity", "O(1)")
        self.time_label.setText(f"Time: {t_comp}")
        self.space_label.setText(f"Space: {s_comp}")

    def apply_font_size(self, size: int):
        sol_font = self.solution_view.font()
        sol_font.setPointSize(size)
        configure_no_ligatures(sol_font)
        self.solution_view.setFont(sol_font)
        self.solution_view.document().setDefaultFont(sol_font)

    def on_copy_clicked(self):
        if self.current_solution:
            self.copy_to_editor_requested.emit(self.current_solution)

    def open_complexity_dialog(self):
        """Opens the Big-O Complexity vector comparison dialog."""
        dlg = BigOComplexityDialog(
            parent=self.window(),
            problem=self.current_problem,
            theme=self.current_theme
        )
        dlg.exec()

    def apply_theme(self, theme):
        self.current_theme = theme
        self.setStyleSheet(f"""
            QWidget#problemSolutionWidget {{
                background-color: {theme['table_bg']};
            }}
            QLabel {{
                background-color: transparent;
            }}
        """)
        self.header_label.setStyleSheet(f"color: {theme['brand_color']}; background: transparent;")
        self.highlighter.apply_theme(theme)

        # High quality monotone SVG icons
        icon_color = theme.get("btn_clear_text", "#d4d4d8")
        self.time_icon.setPixmap(render_svg_pixmap(TIME_SVG, size=14, color=icon_color))
        self.space_icon.setPixmap(render_svg_pixmap(SPACE_SVG, size=14, color=icon_color))

        # Complexity Bar styling
        self.complexity_bar.setStyleSheet("""
            QFrame#complexityBar {
                background-color: transparent;
                border: none;
            }
        """)
        self.time_pill.setStyleSheet(f"""
            QFrame#timePill {{
                background-color: {theme['btn_clear_bg']};
                border: 1px solid {theme['btn_clear_border']};
                border-radius: 6px;
            }}
        """)
        self.space_pill.setStyleSheet(f"""
            QFrame#spacePill {{
                background-color: {theme['btn_clear_bg']};
                border: 1px solid {theme['btn_clear_border']};
                border-radius: 6px;
            }}
        """)
        self.time_label.setStyleSheet(f"color: {theme['brand_color']}; font-weight: 600; background: transparent;")
        self.space_label.setStyleSheet(f"color: {theme['brand_color']}; font-weight: 600; background: transparent;")

        self.complexity_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme['btn_clear_bg']};
                color: {theme['btn_clear_text']};
                border: 1px solid {theme['btn_clear_border']};
                border-radius: 6px;
                padding: 5px 12px;
                font-size: 11px;
            }}
            QPushButton:hover {{
                background-color: {theme['btn_clear_hover']};
                color: {theme['brand_color']};
            }}
        """)

        self.copy_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {theme['btn_clear_bg']};
                color: {theme['btn_clear_text']};
                border: 1px solid {theme['btn_clear_border']};
                border-radius: 6px;
                padding: 4px 10px;
            }}
            QPushButton:hover {{
                background-color: {theme['btn_clear_hover']};
            }}
        """)
        self.solution_view.setStyleSheet(f"""
            QPlainTextEdit {{
                background-color: {theme['console_bg']};
                color: {theme['console_text']};
                border: 1px solid {theme['border_color']};
                border-radius: 6px;
                padding: 8px;
            }}
            {get_scrollbar_stylesheet(theme)}
        """)


# ==========================================================
# Problems List Selection Dialog (Categorized Sections)
# ==========================================================
class ProblemsListDialog(QDialog):
    problem_selected = Signal(dict)

    def __init__(self, parent=None, theme=DARK_THEME):
        super().__init__(parent)
        self.current_theme = theme
        self.setWindowTitle("Practice Problems")
        self.resize(500, 440)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(14, 14, 14, 14)
        layout.setSpacing(10)

        self.header_label = QLabel("Choose a Problem")
        self.header_label.setFont(QFont("SF Pro Display", 14, QFont.Weight.Bold))
        layout.addWidget(self.header_label)

        # Search filter
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Filter problems...")
        self.search_input.setFont(QFont("SF Pro Text", 12))
        self.search_input.textChanged.connect(self.filter_problems)
        layout.addWidget(self.search_input)

        # List of problems (with categorized sections)
        self.list_widget = QListWidget()
        self.list_widget.setFont(QFont("SF Pro Text", 13))
        self.list_widget.itemDoubleClicked.connect(self.on_item_double_clicked)
        layout.addWidget(self.list_widget)

        # Open button
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.open_btn = QPushButton("Open Problem")
        self.open_btn.setFont(QFont("SF Pro Text", 12, QFont.Weight.Bold))
        self.open_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.open_btn.setStyleSheet("""
            QPushButton {
                background-color: #10b981;
                color: #ffffff;
                border: none;
                border-radius: 6px;
                padding: 7px 18px;
            }
            QPushButton:hover {
                background-color: #059669;
            }
        """)
        self.open_btn.clicked.connect(self.on_open_clicked)
        btn_layout.addWidget(self.open_btn)
        layout.addLayout(btn_layout)

        self.apply_theme(self.current_theme)
        self.populate_list(PROBLEMS_DATA)

    def populate_list(self, problems):
        self.list_widget.clear()

        # Group problems by section: "Basics" (1-6), "Hash Map" (7-14), "Recursion" (15-20), "Linked List" (21-31), "Tree" (32-45), "Graph" (46-56), "Sliding Window" (57-69), "Two Pointer" (70-74), "Binary Search" (75-83), "Dynamic Programming" (84-101), "Stack" (102-106), "Array and String" (107-113), "Linked List II" (114-120), "Binary Tree II" (121-129), "Heap" (130-133), "Exhaustive Recursion" (134-141), "Graph II" (142-154), "Mixed Recall" (155-168)
        sections = [
            ("Basics", [p for p in problems if p.get("category") == "Basics"]),
            ("Hash Map", [p for p in problems if p.get("category") == "Hash Map"]),
            ("Recursion", [p for p in problems if p.get("category") == "Recursion"]),
            ("Linked List", [p for p in problems if p.get("category") == "Linked List"]),
            ("Tree", [p for p in problems if p.get("category") == "Tree"]),
            ("Graph", [p for p in problems if p.get("category") == "Graph"]),
            ("Sliding Window", [p for p in problems if p.get("category") == "Sliding Window"]),
            ("Two Pointer", [p for p in problems if p.get("category") == "Two Pointer"]),
            ("Binary Search", [p for p in problems if p.get("category") == "Binary Search"]),
            ("Dynamic Programming", [p for p in problems if p.get("category") == "Dynamic Programming"]),
            ("Stack", [p for p in problems if p.get("category") == "Stack"]),
            ("Array and String", [p for p in problems if p.get("category") == "Array and String"]),
            ("Linked List II", [p for p in problems if p.get("category") == "Linked List II"]),
            ("Binary Tree II", [p for p in problems if p.get("category") == "Binary Tree II"]),
            ("Heap", [p for p in problems if p.get("category") == "Heap"]),
            ("Exhaustive Recursion", [p for p in problems if p.get("category") == "Exhaustive Recursion"]),
            ("Graph II", [p for p in problems if p.get("category") == "Graph II"]),
            ("Mixed Recall", [p for p in problems if p.get("category") == "Mixed Recall"]),
        ]

        known_cats = ("Basics", "Hash Map", "Recursion", "Linked List", "Tree", "Graph", "Sliding Window", "Two Pointer", "Binary Search", "Dynamic Programming", "Stack", "Array and String", "Linked List II", "Binary Tree II", "Heap", "Exhaustive Recursion", "Graph II", "Mixed Recall")
        other_problems = [p for p in problems if p.get("category") not in known_cats]
        if other_problems:
            sections.append(("Other", other_problems))

        first_selectable_item = None

        for section_title, section_problems in sections:
            if not section_problems:
                continue

            # Section Header Item (Non-selectable category header)
            header_item = QListWidgetItem(f"─── {section_title.upper()} ───")
            header_item.setFlags(Qt.ItemFlag.NoItemFlags)
            self.list_widget.addItem(header_item)

            # Problem items with clean title only (no Big-O text)
            for p in section_problems:
                item = QListWidgetItem(f"   {p['title']}")
                item.setData(Qt.ItemDataRole.UserRole, p)
                self.list_widget.addItem(item)
                if first_selectable_item is None:
                    first_selectable_item = item

        if first_selectable_item:
            self.list_widget.setCurrentItem(first_selectable_item)

    def filter_problems(self, text):
        query = text.strip().lower()
        filtered = [
            p for p in PROBLEMS_DATA
            if query in p["title"].lower()
            or query in p["raw_title"].lower()
            or query in p.get("category", "").lower()
        ]
        self.populate_list(filtered)

    def on_item_double_clicked(self, item):
        problem = item.data(Qt.ItemDataRole.UserRole)
        if problem:
            self.problem_selected.emit(problem)
            self.accept()

    def on_open_clicked(self):
        item = self.list_widget.currentItem()
        if item:
            problem = item.data(Qt.ItemDataRole.UserRole)
            if problem:
                self.problem_selected.emit(problem)
                self.accept()

    def apply_theme(self, theme):
        self.header_label.setStyleSheet(f"color: {theme['brand_color']};")
        self.setStyleSheet(f"""
            QDialog {{
                background-color: {theme['window_bg']};
                color: {theme['brand_color']};
            }}
            QLineEdit {{
                background-color: {theme['table_bg']};
                color: {theme['table_text']};
                border: 1px solid {theme['border_color']};
                border-radius: 6px;
                padding: 6px 10px;
            }}
            QListWidget {{
                background-color: {theme['table_bg']};
                color: {theme['table_text']};
                border: 1px solid {theme['border_color']};
                border-radius: 6px;
                padding: 6px;
            }}
            QListWidget::item {{
                padding: 7px 10px;
                border-radius: 4px;
            }}
            QListWidget::item:disabled {{
                color: {theme['table_header_text']};
                font-size: 10px;
                font-weight: bold;
                letter-spacing: 1px;
                background-color: transparent;
                padding-top: 10px;
                padding-bottom: 4px;
            }}
            QListWidget::item:selected {{
                background-color: #2563eb;
                color: #ffffff;
            }}
            {get_scrollbar_stylesheet(theme)}
        """)
