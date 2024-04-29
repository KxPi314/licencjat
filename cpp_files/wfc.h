#ifndef WFC_H
#define WFC_H

#include "load_input.h"
#include <vector>

class Cell{
private:
    int row;
    int col;
    std::vector<int> options;
    bool collapsed;
    int id;
    bool walkable;

public:
    Cell(int row, int col, std::vector<int> options, int id = 0, bool walkable = false);

    void update(std::vector<int> new_options);
    std::vector<int> get_options();
    void clear_options();
    bool is_collapsed();
    
    void set_collapse();
    void set_id(int id);

    int get_id();
    int get_row();
    int get_col();
};

class Wfc{
private:
    int output_width; // wymiary mapy wyjsciowej
    int output_height;
    std::vector<int> start_options; //opcje startowe kazdej komórki
    std::map<int, Neighbors> neighbors_map; //mapa relacji komórek (mozliwi sasiedzi w kazdym kierunku)
    std::vector<std::vector<int>> output_id_mat; //szablon wyjscia
    std::vector<std::vector<Cell>> cell_matrix; //plansza

public:
    Wfc(
        int output_width,
        int output_height,
        std::vector<int> start_options,
        std::map<int, Neighbors> neighbors_map
    );
    std::vector<std::vector<int>> waveFunctionCollapse(); //główna funkcja zwracająca mapę
    int select_option_for_cell(int x, int y); //zwraca id wybranej wartosci
    void collapse_cell(int x, int y);
    Cell* best_cell_to_collapse(); // wpisuje polozenie komórki po zmienne
    void update_near_collapsed_cell(int x, int y); // aktualizuje opcje komórek sasiednich do podanej
    bool end_wfc(int collapsed_counter); // porownuje licznik z wielkosia outputu
};

#endif // WFC_H