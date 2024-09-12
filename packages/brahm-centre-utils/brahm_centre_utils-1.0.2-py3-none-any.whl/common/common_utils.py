import pandas as pd
from difflib import SequenceMatcher
import re

def normalize_name(name):
    # Convert to lowercase
    name = name.lower()
    # Remove extra spaces
    name = re.sub(r'\s+', ' ', name).strip()
    # Remove special characters
    name = re.sub(r'[^a-z0-9\s]', '', name)
    return name
 
# Function to check if names are similar, considering word order
def are_names_similar(name1, name2, threshold=0.9):
    if pd.isna(name1) or pd.isna(name2):
        return False

    # Normalize the names
    name1_normalized = normalize_name(name1)
    name2_normalized = normalize_name(name2)
    
    # Sort the words in each name for comparison
    name1_sorted = ' '.join(sorted(name1_normalized.split()))
    name2_sorted = ' '.join(sorted(name2_normalized.split()))
    
    # Check if all words in one sorted name are in the other. Using subset method
    if set(name1_sorted.split()) <= set(name2_sorted.split()) or set(name2_sorted.split()) <= set(name1_sorted.split()):
        return True
    
    # Use SequenceMatcher to get a similarity ratio
    similarity_ratio = SequenceMatcher(None, name1_sorted, name2_sorted).ratio()
    
    return similarity_ratio >= threshold

# Function to get unique names in each list
def get_unique_names(list1, list_1_name, list2, list_2_name, threshold=0.9):
    unique_in_list1 = []
    unique_in_list2 = []
    
    for name1 in list1:
        is_similar = any(are_names_similar(name1, name2, threshold) for name2 in list2)
        if not is_similar:
            unique_in_list1.append(name1)
    
    for name2 in list2:
        is_similar = any(are_names_similar(name2, name1, threshold) for name1 in list1)
        if not is_similar:
            unique_in_list2.append(name2)
    return unique_in_list1, unique_in_list2