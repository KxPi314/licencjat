import subprocess

# test_data#######
neighbour_dict = {}
neighbour_dict[0] = [[0, 1], [0, 1], [0, 1], [0, 1], [0, 2, 1], [0, 1], [0, 1], [0, 1]]
neighbour_dict[1] = [[0, 1], [0, 1], [0, 2, 1], [0, 1], [0, 1], [0, 1], [0, 1], [0, 1]]
neighbour_dict[2] = [[0, 1, 2], [0, 1], [0, 1], [0, 1, 2], [0, 1], [0, 1], [0, 1], [0, 1]]

output_width = 10
output_height = 10
##################

neighbours_str_parts = []

num_of_options = len(neighbour_dict.keys())
neighbours_str_parts.append(str(num_of_options))

for key in neighbour_dict:
    option_parts = []
    for direction in neighbour_dict[key]:
        direction_str = ",".join(map(str, direction))
        option_parts.append(direction_str)
    neighbours_str_parts.append(";".join(option_parts))

neighbours_str = "|".join(neighbours_str_parts)
neighbours_str += '#'
neighbours_str.

print(neighbours_str)
cpp_executable_path = "./my_cpp"

try:
    subprocess.run([cpp_executable_path, str(output_height), str(output_width), neighbours_str])
except FileNotFoundError:
    print("C++ executable not found.")
except Exception as e:
    print(f"Error: {e}")

# output
# map_elements.csv
