import json

def read_json(file_path):
    """
    Read a JSON file and return the data.
    
    Args:
    file_path (str): Path to the JSON file.
    
    Returns:
    dict: The JSON data loaded into a Python dictionary.
    """
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data

def validate_json_format(data, required_fields):
    """
    Validate that each item in the JSON data contains all required fields.
    
    Args:
    data (dict): The JSON data to check.
    required_fields (list): List of fields that should be present in each item.
    
    Raises:
    AssertionError: If any field is missing in the data.
    """
    for item_id, item in data.items():
        missing_fields = [field for field in required_fields if field not in item]
        if missing_fields:
            raise AssertionError(f"Item ID {item_id} is missing fields: {missing_fields}")

