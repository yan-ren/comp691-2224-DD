import random
import json


def get_random_color():
    # Generate three random integers between 0 and 255
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    # Convert the integers to hex strings and concatenate them with a "#"
    hex_code = '#{0:02x}{1:02x}{2:02x}'.format(r, g, b)

    return hex_code


seen = set()
color_map = {}
i = 0

while i < 100000:
    color_hex = get_random_color()
    if color_hex in seen:
        continue
    seen.add(color_hex)
    color_map[i] = color_hex
    i += 1

with open('color_dict.json', 'w') as file:
    json.dump(color_map, file)
