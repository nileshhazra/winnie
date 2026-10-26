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
from theme import DARK_THEME, get_scrollbar_stylesheet
from highlighter import PythonHighlighter
from icons import TIME_SVG, SPACE_SVG, render_svg_pixmap


# ==========================================================
# Problems Database (All 45 Practice Problems)
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
        self.examples_box.setFont(QFont("Dank Mono", 12))
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
        self.examples_box.setFont(ex_font)

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
        self.solution_view.setFont(QFont("Dank Mono", 13))
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
        self.solution_view.setFont(sol_font)

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

        # Group problems by section: "Basics" (1-6), "Hash Map" (7-14), "Recursion" (15-20), "Linked List" (21-31), "Tree" (32-39)
        sections = [
            ("Basics", [p for p in problems if p.get("category") == "Basics"]),
            ("Hash Map", [p for p in problems if p.get("category") == "Hash Map"]),
            ("Recursion", [p for p in problems if p.get("category") == "Recursion"]),
            ("Linked List", [p for p in problems if p.get("category") == "Linked List"]),
            ("Tree", [p for p in problems if p.get("category") == "Tree"]),
        ]

        known_cats = ("Basics", "Hash Map", "Recursion", "Linked List", "Tree")
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
