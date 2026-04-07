
import json

# Serialize a Python object to a JSON string
data = {'name': 'John', 'age': 30, 'city': 'New York'}
json_string = json.dumps(data)
print(json_string)

# Deserialize a JSON string to a Python object
parsed_data = json.loads(json_string)
print(parsed_data)
