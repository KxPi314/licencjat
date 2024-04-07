#include "load_input.h"

void load_wfc_input(char **args, int *width, int *height, std::vector<int> *start_options, std::map<int, Neighbors> *neighbors) {
    // Extracting width and height
    *width = std::stoi(args[1]);
    *height = std::stoi(args[2]);

    std::string input_str = args[3];
    std::string input_substr;

    // Extracting start options
    size_t pos = input_str.find("|");
    int size_of_options = std::stoi(input_str.substr(0, pos));
    input_substr = input_str.substr(pos + 1);

    std::vector<int> read_options;
    for (int i = 0; i < size_of_options; i++) {
        read_options.push_back(i);
    }
    *start_options = read_options;

    // Extracting neighbors
    pos = input_substr.find("|");
    while (pos != std::string::npos) {
        Neighbors temp;
        std::vector<int> directions[8];

        // Extracting directions for each neighbor
        for (int j = 0; j < 8; j++) {
            while (true) {
                int comma = input_substr.find(",");
                int semicolon = input_substr.find(";");
                if (semicolon < comma || semicolon == -1) // Changed line to handle last entry in a row.
                    break;
                int number = std::stoi(input_substr.substr(0, comma));
                input_substr = input_substr.substr(comma + 1);
                directions[j].push_back(number);
            }
        }
        // Assigning directions to temp struct
        temp.north = directions[0];
        temp.northeast = directions[1];
        temp.east = directions[2];
        temp.southeast = directions[3];
        temp.south = directions[4];
        temp.southwest = directions[5];
        temp.west = directions[6];
        temp.northwest = directions[7];
        (*neighbors)[neighbors->size()] = temp; // Storing neighbors in map
        pos = input_substr.find("|", pos + 1);
    }
}

void load_a_star_input(){
    // soon
};