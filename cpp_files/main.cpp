#include "wfc.h"
#include "load_input.h"
#include <string>
#include <fstream>
#include <iostream>

bool load_output_to_file(std::vector<std::vector<int>> arr, const char* filename){
    std::ofstream file(filename);
    if (file.is_open()) {
        for(int i = 0;i<arr.size();i++){
            for(int j = 0;j<arr[0].size();j++){
                file<<std::to_string(arr[i][j])<<" ";
            }
            file<<"\n";
        }
        file.close();
        std::cout << "Plik zostal zapisany." << std::endl;
    } else {
        std::cerr << "Nie udalo sie otworzyc pliku." << std::endl;
    }
    return 0;
}

int main(int argc, char *argv[])
{
    if (argc != 3)
    {
        std::cout << "Niepoprawna ilosc argumentow" << std::endl;
        return 1;
    }
    
    int output_width = std::stoi(argv[2]);
    int output_height = std::stoi(argv[1]);

    std::vector<int> start_options;
    std::map<int, Neighbors> neighbors;
    std::vector<std::vector<int>> id_arr;

    // Otwarcie pliku CSV
    std::ifstream csv_file("cpp_files/neighbors.csv");
    //std::ifstream csv_file("neighbors.csv");
    if (!csv_file.is_open()) {
        std::cout << "Nie udalo sie zaladowac danych" << std::endl;
        return 1;
    }

    // Wywołanie funkcji do odczytu danych z pliku i załadowania ich do struktur
    load_wfc_input(csv_file, &start_options, &neighbors);
    Wfc wfc = Wfc(output_width, output_height, start_options, neighbors);
    std::vector<std::vector<int>> output = wfc.waveFunctionCollapse();
    load_output_to_file(output,"out.txt");
    return 0;
}

// trzeba zrobic liste best i ja nadpisywac kiedy trzeba