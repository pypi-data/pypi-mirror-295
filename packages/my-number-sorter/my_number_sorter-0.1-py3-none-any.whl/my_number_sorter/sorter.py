number_to_word = {
    0: "zero", 1: "one", 2: "two", 3: "three", 4: "four",
    5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
    10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
    15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen",
    20: "twenty", 30: "thirty", 40: "forty", 50: "fifty", 60: "sixty",
    70: "seventy", 80: "eighty", 90: "ninety", 100: "hundred"
}

def number_to_word_string(n:int):
    return number_to_word.get(n, str(n))

def sort_numbers_by_word_representation(numbers: list[int]):
    sorted_numbers = sorted(numbers, key=lambda x: number_to_word_string(x))
    return sorted_numbers

numbers = [4, 6, 8, 3, 10]
sorted_numbers = sort_numbers_by_word_representation(numbers)
print("Original numbers:", numbers)
print("Sorted numbers:", sorted_numbers)


# from typing import List

# # Helper dictionaries for number-to-word conversion
# ones = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]
# teens = ["eleven", "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen"]
# tens = ["", "ten", "twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]
# hundreds = "hundred"
# thousands = "thousand"

# def number_to_words(n: int) -> str:
#     """Convert an integer to its word representation."""
#     if n == 0:
#         return "zero"
    
#     result = ""
    
#     if n >= 1000:
#         result += ones[n // 1000] + " " + thousands
#         n %= 1000
#         if n > 0:
#             result += " "
    
#     if n >= 100:
#         result += ones[n // 100] + " " + hundreds
#         n %= 100
#         if n > 0:
#             result += " "
    
#     if 10 < n < 20:
#         result += teens[n - 11]
#     else:
#         result += tens[n // 10]
#         if n % 10 > 0:
#             result += " " + ones[n % 10]
#         elif n == 10:
#             result = "ten"
    
#     return result.strip()

# def sort_numbers_by_word_representation(numbers: List[int]) -> List[int]:
#     """Sort numbers based on their alphabetical word representation."""
#     # Sort based on the word string of the number
#     sorted_numbers = sorted(numbers, key=lambda x: number_to_words(x))
#     return sorted_numbers

# # Example usage
# numbers = [4, 6, 8, 3, 10, 105, 342, 19, 2000]
# sorted_numbers = sort_numbers_by_word_representation(numbers)

# print("Original numbers:", numbers)
# print("Sorted numbers:", sorted_numbers)

