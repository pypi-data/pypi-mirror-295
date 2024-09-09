# PyJoker

**PyJoker** is a Python package that provides categorized one-liner jokes. You can either get a random joke or a joke from a specific category like `dad`, `tech`, etc.

## Installation

You can install the package via `pip` after it's published to PyPI:

```bash
pip install pyjoker


Alternatively, if you're developing locally, you can install it by navigating to the project directory and running:
pip install .

Usage
Here’s how you can use PyJoker:

Get a Random Joke
To get a random joke, call the get_joke() function with 'rand' as the argument:

import pyjoker

# Get a random joke
print(pyjoker.get_joke('rand'))

Get a Joke from a Specific Category

To get a joke from a specific category, pass the category name as a string. Example categories include:

1. puns
2. observational
3. deprecating
4. dark
5. sarcasm
6. dad
7. relationships
8. surreal
9. topical
10. tech
11. office
12. animal

import pyjoker

# Get a random 'dad' joke
print(pyjoker.get_joke('dad'))

# Get a random 'tech' joke
print(pyjoker.get_joke('tech'))

------
Make sure to pass the category name as a string (e.g., 'dad').

License
This project is licensed under the MIT License.