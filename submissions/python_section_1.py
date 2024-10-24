# -*- coding: utf-8 -*-
"""python_section_1

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1vSmdP8thEwzoyUWVFJG6u3c9mnT9ojIs
"""

from typing import Dict, Any
from typing import List
import re
import pandas as pd
import polyline
import math

def reverse_in_chunks(lst: list[int], n: int) -> list[int]:
    """
    Reverses elements in groups of 'n' in the input list.
    """
    result = []
    length = len(lst)

    for start in range(0, length, n):
        end = min(start + n, length)
        chunk = lst[start:end]


        left, right = 0, len(chunk) - 1
        while left < right:
            chunk[left], chunk[right] = chunk[right], chunk[left]
            left += 1
            right -= 1

        result.extend(chunk)

    return result
print(reverse_in_chunks([1, 2, 3, 4, 5, 6, 7, 8], 3))
print(reverse_in_chunks([1, 2, 3, 4, 5], 2))
print(reverse_in_chunks([10, 20, 30, 40, 50, 60, 70], 4))

def group_strings_by_length(strings: list[str]) -> dict[int, list[str]]:
    """
    Groups a list of strings by their length and returns a dictionary.

    """
    grouped_strings = {}

    for string in strings:
        string_length = len(string)

        if string_length not in grouped_strings:
            grouped_strings[string_length] = []


        grouped_strings[string_length].append(string)


    return dict(sorted(grouped_strings.items()))


print(group_strings_by_length(["apple", "bat", "car", "elephant", "dog", "bear"]))
print(group_strings_by_length(["one", "two", "three", "four"]))

def flatten_dict(nested_dict: Dict, sep: str = '.') -> Dict:
    """
    Flattens a nested dictionary into a single-level dictionary.

    Args:
    nested_dict: The nested dictionary to flatten.
    sep: The separator to use for joining nested keys. Defaults to '.'.

    Returns:
    A flattened dictionary.
    """

    def _flatten(current_dict: Any, parent_key: str = '') -> Dict:
        items = []
        for key, value in current_dict.items():
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):

                items.extend(_flatten(value, new_key).items())
            elif isinstance(value, list):

                for index, item in enumerate(value):
                    list_key = f"{new_key}[{index}]"
                    if isinstance(item, dict):
                        items.extend(_flatten(item, list_key).items())
                    else:
                        items.append((list_key, item))
            else:
                items.append((new_key, value))

        return dict(items)

    return _flatten(nested_dict)



nested_dict = {
    "road": {
        "name": "Highway 1",
        "length": 350,
        "sections": [
            {
                "id": 1,
                "condition": {
                    "pavement": "good",
                    "traffic": "moderate"
                }
            }
        ]
    }
}

flattened_dict = flatten_dict(nested_dict)
print(flattened_dict)

def unique_permutations(nums: List[int]) -> List[List[int]]:
    """
    Generate all unique permutations of a list of integers that may contain duplicates.

    Args:
        nums (List[int]): A list of integers which may contain duplicates.

    Returns:
        List[List[int]]: A list of unique permutations.
    """
    def backtrack(start: int):

        if start == len(nums):
            result.append(nums[:])
            return

        seen = set()
        for i in range(start, len(nums)):
            if nums[i] in seen:
                continue

            seen.add(nums[i])
            nums[start], nums[i] = nums[i], nums[start]
            backtrack(start + 1)
            nums[start], nums[i] = nums[i], nums[start]

    nums.sort()
    result = []
    backtrack(0)
    return result


input_list = [1, 1, 2]
unique_perms = unique_permutations(input_list)
print(unique_perms)

def find_all_dates(text: str) -> List[str]:
    """
    Find all valid dates in the given string.

    Args:
        text (str): A string that may contain dates in various formats.

    Returns:
        List[str]: A list of valid dates found in the text.
    """

    patterns = [
        r'\b\d{2}-\d{2}-\d{4}\b',   # dd-mm-yyyy
        r'\b\d{2}/\d{2}/\d{4}\b',   # mm/dd/yyyy
        r'\b\d{4}\.\d{2}\.\d{2}\b'   # yyyy.mm.dd
    ]


    combined_pattern = '|'.join(patterns)

    matches = re.findall(combined_pattern, text)

    return matches

text = "I was born on 23-08-1994, my friend on 08/23/1994, and another one on 1994.08.23."
found_dates = find_all_dates(text)
print(found_dates)

def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6371000
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)

    a = (math.sin(delta_phi / 2) ** 2 +
         math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c

def decode_polyline(polyline_str):
    coords = polyline.decode(polyline_str)
    df = pd.DataFrame(coords, columns=['latitude', 'longitude'])
    distances = [0.0]

    for i in range(1, len(coords)):
        lat1, lon1 = coords[i - 1]
        lat2, lon2 = coords[i]
        distance = calculate_distance(lat1, lon1, lat2, lon2)
        distances.append(distance)

    df['distance'] = distances
    return df


polyline_string = "u~w~Fj~r~c@j`@hB_@}C"
result_df = decode_polyline(polyline_string)
print(result_df)

def rotate_matrix(matrix):
    n = len(matrix)
    return [[matrix[n - 1 - j][i] for j in range(n)] for i in range(n)]

def transform_matrix(matrix):
    n = len(matrix)
    return [[sum(matrix[i]) - matrix[i][j] + sum(matrix[k][j] for k in range(n)) - matrix[i][j] for j in range(n)] for i in range(n)]

def rotate_and_transform(matrix):
    return transform_matrix(rotate_matrix(matrix))


matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
result = rotate_and_transform(matrix)
print(result)

from pandas import Timedelta

def verify_timestamps(df):

    def get_time_range(row):
        day_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3,
                   'Friday': 4, 'Saturday': 5, 'Sunday': 6}
        start = pd.Timestamp('1970-01-01') + pd.to_timedelta(day_map[row['startDay']], unit='D') + pd.to_timedelta(row['startTime'])
        end = pd.Timestamp('1970-01-01') + pd.to_timedelta(day_map[row['endDay']], unit='D') + pd.to_timedelta(row['endTime'])
        return start, end


    df[['startDatetime', 'endDatetime']] = df.apply(get_time_range, axis=1, result_type='expand')


    results = []
    grouped = df.groupby(['id', 'id_2'])

    for (id_val, id_2_val), group in grouped:
        total_time_covered = Timedelta(0)
        group = group.sort_values('startDatetime')

        for _, row in group.iterrows():
            total_time_covered += row['endDatetime'] - row['startDatetime']


        results.append(((id_val, id_2_val), total_time_covered >= Timedelta(days=7)))


    index = pd.MultiIndex.from_tuples([r[0] for r in results], names=['id', 'id_2'])
    return pd.Series([r[1] for r in results], index=index)


boolean_series = verify_timestamps(df)
print(boolean_series.head())