import os
import pandas as pd
import random
from .categories import JokeCategories

# Define the path to the CSV file relative to the current file
csv_path = os.path.join(os.path.dirname(__file__), 'jokes.csv')

def load_jokes_from_csv(file_path=csv_path):
    """
    Load jokes from the CSV file.

    Parameters:
    - file_path (str): The path to the CSV file containing the jokes.

    Returns:
    - dict: A dictionary where the keys are joke categories and values are lists of jokes.
    """
    try:
        jokes_df = pd.read_csv(file_path)
        jokes_dict = {category.lower(): [] for category in JokeCategories.__dict__.keys() if not category.startswith('__')}
        
        for _, row in jokes_df.iterrows():
            category = row['category'].lower()
            joke = row['joke'].strip(' "')  # Clean up the joke string
            if category in jokes_dict:
                jokes_dict[category].append(joke)

        return jokes_dict
    except Exception as e:
        print(f"Error loading jokes from CSV: {e}")
        return {}

jokes = load_jokes_from_csv()

def get_joke(input_value='rand'):
    """
    Get a random joke or a joke from a specific category.

    Parameters:
    - input_value (str): The category of the joke or 'rand' for a random joke.
                         Available categories include 'puns', 'dad', 'tech', etc.

    Returns:
    - str: A joke from the specified category or a random joke if 'rand' is passed.
    """
    input_value = input_value.lower()  # Normalize input to lowercase

    if input_value == 'rand':
        try:
            return random.choice([j for category in jokes.values() for j in category])
        except IndexError:
            return "No jokes available. Please check the CSV file."
    
    if input_value in jokes:
        try:
            return random.choice(jokes[input_value])
        except IndexError:
            return f"No jokes available for category '{input_value}'."
    
    return "Category not found. Please provide a valid category."
