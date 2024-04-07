#include "wfc.h"


Cell::Cell() : row(0), col(0), collapsed(false), id(nullptr), walkable(true), difficult_terrain(0.0f) {}

Cell::Cell(int row, int col, std::vector<int> options, float difficult_terrain = 0.1, int* id = nullptr, bool walkable = false)
    : row(row),
    col(col),
    options(options),
    collapsed(false),
    id(id),
    walkable(walkable),
    difficult_terrain(difficult_terrain) {}

void Cell::update(std::vector<int> new_options){
    std::sort(options.begin(), options.end());
    std::sort(new_options.begin(), new_options.end());

    std::vector<int> intersection;

    std::set_intersection(options.begin(), options.end(),
                          new_options.begin(), new_options.end(),
                          std::back_inserter(intersection));

    this->options = std::move(intersection);
}

int* Cell::get_id(){
    return id;
}

int Cell::get_row(){
    return row;
}

int Cell::get_col(){
    return col;
}

bool Cell::is_collapsed(){
    return collapsed;
}

std::vector<int> Cell::get_options(){
    return options;
}

void Cell::set_collapse(){
    collapsed = true;
}

void Cell::set_id(int id){
    this->id = &id;
}

void freeMemory(Cell** cell_arr, int height) {
    for (int i = 0; i < height; ++i) {
        delete[] cell_arr[i];
    }
    delete[] cell_arr;
}

void wfc(int width, int height, std::vector<int> start_options, std::map<int, Neighbors> neighbors_map, int*** id_arr){

    Cell** cell_arr = new Cell*[height];
    for (int i = 0; i < height; ++i) {
        cell_arr[i] = new Cell[width];
        for(int j = 0; j < width; j++){
            cell_arr[i][j] = Cell(i,j,start_options);
        }
    }

    std::random_device rd;
    std::mt19937 gen(rd()); 

    std::uniform_int_distribution<> dis(0, height);

    int x = dis(gen);
    int y = dis(gen);

    collapse_cell(x,y, cell_arr, neighbors_map, width, height);

    int end_counter = width*height;
    while(!end_collapse(end_counter)){
        find_best_cell(&x, &y, cell_arr, width, height);
        collapse_cell(x,y, cell_arr, neighbors_map, width, height);
        end_counter--;
    }

    *id_arr = new int*[height];
    for (int i = 0; i < height; ++i) {
        id_arr[i] = new int*[width];
        for(int j = 0; j < width; j++){
            id_arr[i][j] = cell_arr[i][j].get_id();
        }
    }

    freeMemory(cell_arr, height);
}

int best_cell_option(Cell* cell){
    std::random_device rd;
    std::mt19937 gen(rd());

    std::uniform_int_distribution<> dis(0, cell->get_options().size() - 1);
    int random_index = dis(gen);
    return cell->get_options()[random_index];
}

void collapse_cell(int x, int y, Cell** cell_arr,  std::map<int, Neighbors> neighbors_map, int width, int height){
    cell_arr[x][y].set_id(best_cell_option(&cell_arr[x][y]));
    cell_arr[x][y].set_collapse();
    cell_arr[x][y].get_options().clear();
    update_near_collapsed(x, y, cell_arr, neighbors_map, width, height);
}

void find_best_cell(int* x, int* y, Cell** cell_arr, int width, int height){
    std::vector<Cell*> best;
    for (int i = 0; i < height; ++i){
        for(int j = 0; j < width; j++){
            if(!cell_arr[i][j].is_collapsed()){
                if(best.empty()){
                    best.push_back(&cell_arr[i][j]);
                }
                else if(cell_arr[i][j].get_options().size()<best[0]->get_options().size()){
                    best.clear();
                    best.push_back(&cell_arr[i][j]);
                }
                else if(cell_arr[i][j].get_options().size()==best[0]->get_options().size()){
                    best.push_back(&cell_arr[i][j]);
                }
            }
        }
    }
    std::random_device rd;
    std::mt19937 gen(rd());

    std::uniform_int_distribution<> dis(0, best.size() - 1);
    int random_index = dis(gen);

    Cell* random_element = best[random_index];
    int row = random_element->get_row();
    int col = random_element->get_col();
    *x = row;
    *y = col;
}

void update_near_collapsed(int x, int y, Cell** cell_arr, std::map<int, Neighbors> neighbors_map, int width, int height) {
    std::vector<std::pair<int, int>> offsets = {
        {-1, 0}, {-1, 1}, {0, 1}, {1, 1},
        {1, 0}, {1, -1}, {0, -1}, {-1, -1}
    };

    for (const auto& offset : offsets) {
        int dx = offset.first;
        int dy = offset.second;
        int new_x = x + dx;
        int new_y = y + dy;

        if (new_x >= 0 && new_x < height && new_y >= 0 && new_y < width && !cell_arr[new_x][new_y].is_collapsed()) {
            switch (dx) {
                case -1:
                    switch (dy) {
                        case 0: cell_arr[new_x][new_y].update(neighbors_map[*cell_arr[x][y].get_id()].north); break;
                        case 1: cell_arr[new_x][new_y].update(neighbors_map[*cell_arr[x][y].get_id()].northeast); break;
                        case -1: cell_arr[new_x][new_y].update(neighbors_map[*cell_arr[x][y].get_id()].northwest); break;
                    }
                    break;
                case 0:
                    switch (dy) {
                        case 1: cell_arr[new_x][new_y].update(neighbors_map[*cell_arr[x][y].get_id()].east); break;
                        case -1: cell_arr[new_x][new_y].update(neighbors_map[*cell_arr[x][y].get_id()].west); break;
                    }
                    break;
                case 1:
                    switch (dy) {
                        case 0: cell_arr[new_x][new_y].update(neighbors_map[*cell_arr[x][y].get_id()].south); break;
                        case 1: cell_arr[new_x][new_y].update(neighbors_map[*cell_arr[x][y].get_id()].southeast); break;
                        case -1: cell_arr[new_x][new_y].update(neighbors_map[*cell_arr[x][y].get_id()].southwest); break;
                    }
                    break;
            }
        }
    }
}


bool end_collapse(int counter){
    return counter <= 0;
}
