#include "wfc.h"
#include <algorithm>
#include <iterator>
#include <iostream>
#include <cstdlib>
#include <ctime>

Cell::Cell(int row, int col, std::vector<int> options, int id, bool walkable)
:row(row),
 col(col),
 options(options),
 collapsed(false),
 id(id),
 walkable(walkable){}

void Cell::update(std::vector<int> new_options){
    std::sort(options.begin(), options.end());
    std::sort(new_options.begin(), new_options.end());
    std::vector<int> intersection;

    std::set_intersection(options.begin(),options.end(),
                          new_options.begin(),new_options.end(),
                          back_inserter(intersection)
                          );
    options = intersection;
}
std::vector<int> Cell::get_options(){return options;}
void Cell::clear_options(){options.clear();}
bool Cell::is_collapsed(){return collapsed;}

void Cell::set_collapse(){collapsed = true;}
void Cell::set_id(int id){this->id = id;}

int Cell::get_id(){return id;}
int Cell::get_row(){return row;}
int Cell::get_col(){return col;}

//implementacje wfc
 Wfc::Wfc(
        int output_width,
        int output_height,
        std::vector<int> start_options,
        std::map<int, Neighbors> neighbors_map
    )
    :output_width(output_width),
     output_height(output_height),
     start_options(start_options),
     neighbors_map(neighbors_map),
     output_id_mat(output_height, std::vector<int>(output_width, 0)){
        cell_matrix = {};
        for(int i = 0; i<output_height; i++){
            std::vector<Cell> line = {};
            for(int j = 0; j<output_width; j++){
                line.emplace_back(Cell(i, j, this->start_options, 0, false));
            }
            cell_matrix.emplace_back(line);
        }
     }

std::vector<std::vector<int>> Wfc::waveFunctionCollapse(){
    int collapse_counter = 0;
    srand(time(nullptr));
    int x = rand() % output_height;
    int y = rand() % output_width; 

    collapse_cell(x, y);
    update_near_collapsed_cell(x,y);
    collapse_counter++;

    while (!end_wfc(collapse_counter))
    {
        Cell* best = best_cell_to_collapse();
        if(best == nullptr)
            break;
        collapse_cell(best->get_row(), best->get_col());
        update_near_collapsed_cell(best->get_row(), best->get_col());
        collapse_counter++;
    }
    for(int i = 0; i< output_height; i++){
        for(int j = 0; j<output_width; j++){
            output_id_mat[i][j] = cell_matrix[i][j].get_id();
        }
    }
    return output_id_mat;
}
int Wfc::select_option_for_cell(int x, int y){
    if(cell_matrix[x][y].get_options().size()>0)
        return cell_matrix[x][y].get_options()[rand() % cell_matrix[x][y].get_options().size()];
    return 0;
}
void Wfc::collapse_cell(int x, int y){
    int id = select_option_for_cell(x, y);
    cell_matrix[x][y].set_id(id);
    cell_matrix[x][y].clear_options(); 
    cell_matrix[x][y].set_collapse();
}
Cell* Wfc::best_cell_to_collapse(){
    std::vector<Cell*> best;
    for(int i=0;i<output_height;i++){
        for(int j=0;j<output_width;j++){
            if(!cell_matrix[i][j].is_collapsed()){
                if(best.empty())
                    best.push_back(&cell_matrix[i][j]);
                else if(cell_matrix[i][j].get_options().size()==best[0]->get_options().size()){
                    best.push_back(&cell_matrix[i][j]);
                }
                else if(cell_matrix[i][j].get_options().size()<best[0]->get_options().size()){
                    best.clear();
                    best.push_back(&cell_matrix[i][j]);
                }
            }
        }
    }
    if(best.empty())
        return nullptr;
    return best[rand() % best.size()];
}
void Wfc::update_near_collapsed_cell(int x, int y){
    int direction = 0;
    std::vector<std::vector<int>> neighbors;
    neighbors.push_back(neighbors_map[cell_matrix[x][y].get_id()].northwest);
    neighbors.push_back(neighbors_map[cell_matrix[x][y].get_id()].north);
    neighbors.push_back(neighbors_map[cell_matrix[x][y].get_id()].northeast);
    neighbors.push_back(neighbors_map[cell_matrix[x][y].get_id()].west);
    neighbors.push_back(neighbors_map[cell_matrix[x][y].get_id()].east);
    neighbors.push_back(neighbors_map[cell_matrix[x][y].get_id()].southwest);
    neighbors.push_back(neighbors_map[cell_matrix[x][y].get_id()].south);
    neighbors.push_back(neighbors_map[cell_matrix[x][y].get_id()].southeast);
    for(int i = -1; i<2; i++){
        for(int j = -1; j<2; j++){
            if(!(i== 0 && j==0)){
                if((x+i)<output_height && (x+i)>=0 && (y+j)<output_width && (y+j)>=0 && !cell_matrix[x+i][y+j].is_collapsed()){
                    cell_matrix[x+i][y+j].update(neighbors[direction]);
                }
                direction++;
            }
        }
    }
}
bool Wfc::end_wfc(int collapsed_counter){
    if(collapsed_counter >= output_width*output_height)
        return true;
    return false;
}


//zaczyna sie od 00 nie wiem czemu