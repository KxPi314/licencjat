import subprocess
import time


def wfcRunner(neighbour_dict, output_width, output_height):
    neighbours_csv = open("cpp_files/neighbors.csv", "w")
    num_of_options = len(neighbour_dict.keys())
    neighbours_csv.write(f"{num_of_options};left_up;up;right_up;left;right;left_down;right_down\n")

    lines = []

    for key in neighbour_dict.keys():
        line = ""
        # dodanie listy elementów z kazdego kierunku
        for index, direction in enumerate(neighbour_dict.get(key)):
            # przecinki miedzy elementami
            line += ",".join(map(str, direction))
            # sredniki między kazdym kierunkiem
            if index != len(neighbour_dict.get(key)) - 1:
                line += ";"
        lines.append(line + "\n")

    # wynik zapisany do csv
    neighbours_csv.writelines(lines)
    neighbours_csv.close()
    cpp_executable_path = "cpp_files/program.exe"
    try:
        # do pliku cpp jako ardumenty podaję wymiaery koncowej planszy
        result = subprocess.run([cpp_executable_path, str(output_height), str(output_width)], capture_output=True,
                                text=True)
        print(result.stdout)
    except FileNotFoundError:
        print("C++ executable not found.")
    except Exception as e:
        print(f"Error: {e}")
