import json
import objectpath
from JSON.json_definition import EnergyObject

js = '''{"name": "My_model", "geometry": {"geo_type": "Wall", "plane": [[0,0,0],[2,4,1]]}, "boundary": "bbb"}'''
js2 = '''{"name": "model", "boundary": [[0,0,0],[2,4,1]]}'''
j = json.loads(js)  # return dictionary
# obj = EnergyObject(**j)
# print(j["geometry"]["plane"][1])

# Read a json file
f = open("D:\Projects\OpenStudioDev\Room.json", "r")
data = json.loads(f.read())

# Create json file
# 1. from dictionary:
my_dict = {"name": "kobe", "team": "Lakers", "number": 24}
js_dict = json.dumps(my_dict, indent=4)  # Return a json string
print(js_dict)

# 2. from python list:
my_list = [{"name": "kobe"}, {"team": "Lakers", "number": 24}]
js_list = json.dumps(my_list, indent=4)  # Return a json string
print(js_list)

# 3. from python tuple:
my_tuple = ({"name": "kobe"}, {"team": "Lakers", "number": 24})
js_tuple = json.dumps(my_tuple, indent=4)  # Return a json string
print(js_tuple)


# Extract nested values from a json tree
def json_extract(obj, key):
    # Recursively fetch values from nested JSON
    arr = []

    def extract(obj, arr, key):
        # Recursively search for values of key in JSON tree.
        if isinstance(obj, dict):
            for k, v in obj.items():
                if isinstance(v, (dict, list)):
                    extract(v, arr, key)
                elif k == key:
                    arr.append(str(v))
        elif isinstance(obj, list):
            for item in obj:
                extract(item, arr, key)
        return arr

    values = extract(obj, arr, key)
    return values


my_plane = json_extract(j, "geometry")
print(my_plane)

arr = [[0, 0, 0], [2, 4, 1]]
print(isinstance(arr, list))


# Function to parse json using objectpath:
def json_parse(obj: dict, expr: str) -> (str, list, int):
    tree = objectpath.Tree(obj)
    content = tree.execute(expr)

    if isinstance(content, (objectpath.generator, objectpath.chain)):
        return list(content)
    else:
        return content


# js_tree = objectpath.Tree(data["rooms"])
# result = list(js_tree.execute('$..plane'))
result = json_parse(data, "$.display_name")
print(result)
