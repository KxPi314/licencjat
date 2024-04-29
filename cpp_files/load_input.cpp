#include "load_input.h"
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>



void load_wfc_input(std::ifstream& csv_file, std::vector<int> *start_options, std::map<int, Neighbors> *neighbors)
{
    std::map<int, Neighbors> new_neighbors = {};
    std::vector<int> new_start_options = {};
    
    int point_counter = 0;
    std::string line;
    std::getline(csv_file, line);
    //iterowanie po linijkach "sasiadach"
    while (std::getline(csv_file, line)) {
        std::vector<std::string> tokens;
        std::stringstream str_stream(line);
        std::string token;
        Neighbors point;
        
        while (std::getline(str_stream, token, ';')) {
            tokens.push_back(token);
        }
        int direction_counter = 0;
        //iterowanie po kierunkach
        for (const std::string& t : tokens) {
            std::vector<int> direction = {};
            std::stringstream tokenStream(t);
            std::string number;
            
            //iterowanie po elementach kierunków.
            while (std::getline(tokenStream, number, ',')) {
                // dodawanie wartosci do wektora kierunku.
                int value = std::stoi(number);
                direction.push_back(value);
                // dodawanie do opcji startowych jesli juz tam nie jest.
                auto iter = std::find(new_start_options.begin(), new_start_options.end(), value);
                if (iter == new_start_options.end() && value!=0) {
                    new_start_options.push_back(value);
                }
            }
            switch (direction_counter)
            {
            case 0:
                point.northwest = direction;
                break;
            case 1:
                point.north = direction;
                break;
            case 2:
                point.northeast = direction;
                break;
            case 3:
                point.west = direction;
                break;
            case 4:
                point.east = direction;
                break;
            case 5:
                point.southwest = direction;
                break;
            case 6:
                point.south = direction;
                break;
            case 7:
                point.southeast = direction;
                break;
            default:
                break;
            }
            direction_counter++;
        }
        new_neighbors[point_counter] = point;
        point_counter++;
    }

    // zapis wyjscia
    *neighbors = new_neighbors;
    *start_options = new_start_options;

    return;
}

void load_a_star_input(){
    // soon
};