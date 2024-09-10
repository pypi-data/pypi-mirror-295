# My Number Sorter

My Number Sorter is a Python library that sorts numbers from 1 to 100 based on their alphabetical word representation.

## Features

- Converts numbers to their word representation
- Sorts numbers based on the alphabetical order of their word representation
- Handles numbers within the range of 1 to 100.

## Installation

You can install the library via pip:

```bash
pip install my_number_sorter
```

# Import the library

from my_number_sorter import sort_numbers_by_word_representation

# Example list of numbers

numbers = [4, 6, 8, 3, 10,]

# Sort the numbers by their word representation

sorted_numbers = sort_numbers_by_word_representation(numbers)

# Print the sorted numbers

print(sorted_numbers) # Output: [8, 4, 6, 10, 3]
