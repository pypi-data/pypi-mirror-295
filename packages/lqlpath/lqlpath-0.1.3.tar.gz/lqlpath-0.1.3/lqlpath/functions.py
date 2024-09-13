import json

# Global dictionary to store key-value pairs
dict_k1 = {}


def fetch_key_value_from_json_file(file_name: str):
    """
    Reads a JSON file, parses it, and stores key-value pairs in dict_k1.

    Args:
        file_name (str): The name of the input JSON file.

    Returns:
        list: A list of paths (keys) extracted from the JSON structure.
    """
    try:
        with open(file_name, 'r') as file:
            nested_dict = json.load(file)
        paths = find_paths(nested_dict)
        return paths
    except FileNotFoundError:
        print(f"Error: The file {file_name} does not exist.")
    except json.JSONDecodeError:
        print(f"Error: The file {file_name} is not a valid JSON file.")
    except Exception as e:
        print(f"An error occurred: {e}")


def find_paths(d, current_path=""):
    """
    Recursively finds all paths (keys) in a nested dictionary.

    Args:
        d (dict): The dictionary to traverse.
        current_path (str): The current path being processed.

    Returns:
        list: A list of all keys (paths) in the dictionary.
    """
    paths = []

    if isinstance(d, dict):
        for k, v in d.items():
            new_path = f"{current_path}.{k}" if current_path else k
            if isinstance(v, dict):
                paths.extend(find_paths(v, new_path))
            elif isinstance(v, list):
                for v1 in v:
                    if isinstance(v1, dict):
                        paths.extend(find_paths(v1, new_path))
            else:
                paths.append(new_path)
                dict_k1[new_path] = v

    return paths


def get_byKey(file_name: str, key_search: str):
    """
    Search for a specific key in the JSON data.

    Args:
        file_name (str): The name of the JSON file.
        key_search (str): The key to search for in the JSON structure.

    Returns:
        list: A list of matching keys.
    """
    fetch_key_value_from_json_file(file_name)
    final_list = [k for k in dict_k1 if key_search in k]
    return final_list


def get_byValue(file_name: str, value_search: str, flag=None):
    """
    Search for a specific value in the JSON data.

    Args:
        file_name (str): The name of the JSON file.
        value_search (str): The value to search for in the JSON structure.
        flag (str, optional): If 'like', performs a partial match. Defaults to None.

    Returns:
        list: A list of matching values or keys.
    """
    fetch_key_value_from_json_file(file_name)
    final_list = []

    for k, v in dict_k1.items():
        if flag == 'like' and value_search.strip() in str(v):
            final_list.append(v)
        elif value_search.strip() == str(v):
            final_list.append(k)

    return final_list


# Example usage
