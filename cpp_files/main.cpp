#include "wfc.h"
#include "load_input.h"
#include <string>
#include <iostream>

int main(int argc, char *argv[])
{
    if (argc != 5)
        return 1;

    int *output_width;
    int *output_height;
    std::vector<int> *start_options;
    std::map<int, Neighbors> *neighbors;
    int ***id_arr;

    load_wfc_input(argv, output_width, output_height, start_options, neighbors);
    wfc(*output_width, *output_height, *start_options, *neighbors, id_arr);
    // output id_arr

    return 0;
}