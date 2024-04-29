#ifndef INPUT_LOADER_H
#define INPUT_LOADER_H

#include <map>
#include <vector>
#include <string>

struct Neighbors
{
    std::vector<int> northwest; // Neighbors to the northwest
    std::vector<int> north;     // Neighbors to the north
    std::vector<int> northeast; // Neighbors to the northeast
    std::vector<int> east;      // Neighbors to the east
    std::vector<int> west;      // Neighbors to the west
    std::vector<int> southwest; // Neighbors to the southwest
    std::vector<int> south;     // Neighbors to the south
    std::vector<int> southeast; // Neighbors to the southeast
};

// Function to load WFC input form python
void load_wfc_input(std::ifstream& csv_file, std::vector<int> *start_options, std::map<int, Neighbors> *neighbors);

// Function to load A* input from python
void load_a_star_input();

#endif
