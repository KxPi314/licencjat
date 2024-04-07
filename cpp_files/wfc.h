#ifndef WFC_H
#define WFC_H

#include "load_input.h"
#include <vector>
#include <map>
#include <algorithm>
#include <iterator>
#include <random>

class Cell {
private:
    int row;
    int col;
    std::vector<int> options;
    bool collapsed;
    int* id;
    bool walkable;
    float difficult_terrain;

public:
    Cell();
    Cell(int row, int col, std::vector<int> options, float difficult_terrain = 0.1, int* id = nullptr, bool walkable = false);

    void update(std::vector<int> new_options);
    int* get_id();
    int get_row();
    int get_col();
    bool is_collapsed();
    std::vector<int> get_options();
    void set_collapse();
    void set_id(int id);
};

void wfc(int width, int height, std::vector<int> start_options, std::map<int, Neighbors> neighbors_map, int*** id_arr);
int best_cell_option(Cell* cell);
void collapse_cell(int x, int y, Cell** cell_arr,  std::map<int, Neighbors> neighbors_map, int width, int height);
void find_best_cell(int* x, int* y, Cell** cell_arr, int width, int height);
void update_near_collapsed(int x, int y, Cell** cell_arr, std::map<int, Neighbors> neighbors_map, int width, int height);
bool end_collapse(int counter);

#endif //WFC_H
