from requests_html import HTMLSession
from colorama import Fore, Back, Style
import sys
import exceptions
import pandas
from functions import pop_data_finder, filter_min, filter_max, sort_lowest, sort_highest

args = sys.argv[1:]

options = ["help", "bb", "sx", "min", "max", "gf", "bcs", "pkmn", "lf", "hf"]

web_options = {"sx": "Searches for funkos on StockX"}

web_args = [arg for arg in args if arg in web_options]

category_options = {"bb": "Searches for funkos of the emmy-winning Breaking Bad", "gf": "Searches for funkos of the legendary trilogy of The Godfather", "bcs": "Searches for funkos of the BB prequel Better Call Saul", "pkmn": "Searches for funkos of Pokemon"}

category_args = [arg for arg in args if arg in category_options]

full_names = {"sx": "StockX", "bb": "Breaking Bad", "gf": "The Godfather", "bcs": "Better Call Saul", "pkmn": "Pokemon"}

data_filtering_options = {"min": "Finds funkos with lowest ask price in all given categories and websites", "max": "Finds funkos with highest ask price in all given categories and websites"}

data_filtering_functions = {"min": filter_min, "max": filter_max}

data_filtering_args = {cmd: func for cmd, func in data_filtering_functions.items() if cmd in args}

data_sorting_options = {"lf": "lowest To highest asking price per category and website", "hf": "Highest to lowest asking price per category and website"}

data_sorting_functions = {"lf": sort_lowest, "hf": sort_highest}

data_sorting_args = {cmd: func for cmd, func in data_sorting_functions.items() if cmd in args}

#tuple: (websites, pop html class, pop price html class, pop name html class, pop image html class)
web_data = {"sx": {"bb": (["https://stockx.com/search?s=breaking+bad+funko"], ".css-1yh5062", ".css-nsvdd9", ".css-3lpefb", ".css-tkc8ar"), "gf": (["https://stockx.com/search?s=godfather+funko"], ".css-1yh5062", ".css-nsvdd9", ".css-3lpefb", ".css-tkc8ar"), "bcs": (["https://stockx.com/search?s=better+call+saul+funko"], ".css-1yh5062", ".css-nsvdd9", ".css-3lpefb", ".css-tkc8ar"), "pkmn": (["https://stockx.com/search?s=pokemon+funko&page=1", "https://stockx.com/search?s=pokemon+funko&page=2"], ".css-1yh5062", ".css-nsvdd9", ".css-3lpefb", ".css-tkc8ar")}}

if len(args) == 0:
    raise exceptions.InputNotFound(Fore.RED + "No options selected...")

for arg in args:
    if arg not in options:
        raise exceptions.OptionNotFound(Fore.RED + "Option: \"" + arg + "\" not valid.")
    
if "lf" in args and "hf" in args:
    raise exceptions.MutuallyExclusiveOptions(Fore.RED + "Options \"lf\" and \"hf\" can't be used at the same time")
    
if "help" in args:
    print(Back.LIGHTRED_EX + "-------------------------------------------------------------------------------------------" + Back.RESET)
    print(Fore.CYAN + Style.BRIGHT + "Website Options:" + Style.NORMAL)
    for option in web_options:
        print(Fore.BLUE + option + ":\t" + web_options[option])
    print(Back.GREEN + "-------------------------------------------------------------------------------------------" + Back.RESET)
    print(Fore.CYAN + Style.BRIGHT + "Category Options:" + Style.NORMAL)
    for option in category_options:
        print(Fore.BLUE + option + ":\t" + category_options[option])
    print(Back.GREEN + "-------------------------------------------------------------------------------------------" + Back.RESET)
    print(Fore.CYAN + Style.BRIGHT + "Data Filtering Options:" + Style.NORMAL)
    for option in data_filtering_options:
        print(Fore.BLUE + option + ":\t" + data_filtering_options[option])
    print(Back.LIGHTRED_EX + "-------------------------------------------------------------------------------------------" + Back.RESET)

if len(args) > 1 and "help" in args or len(args) > 0 and "help" not in args:
    print(Back.RED + "-------------------------------------------------------------------------------------------" + Back.RESET)
    for web_arg in web_args:
        print(Fore.CYAN + Style.BRIGHT + "Website:\t" + Fore.MAGENTA + full_names[web_arg] + ":" + Fore.RESET)
        for category_arg in category_args:
            print(Style.BRIGHT + "-------------------------------------------------------------------------------------------" + Style.NORMAL)
            print(Fore.CYAN + Style.BRIGHT + "Category:\t" + Fore.MAGENTA + full_names[category_arg] + ":")
            data = pop_data_finder(*web_data[web_arg][category_arg])
            for sorting in data_sorting_args:
                data_sorting_args[sorting](data)
            data_final = data
            if len(data_filtering_args) > 0:
                data_final = {"prices": [], "names": [], "images": []}
            for filtering in data_filtering_args:
                for stat in data:
                    data_final[stat] += data_filtering_args[filtering](data)[stat]
            for x in range(len(data_final["prices"])): 
                print(Back.GREEN + "-------------------------------------------------------------------------------------------" + Back.RESET)
                print(Fore.BLUE + "Price:\t" + Fore.MAGENTA + str(data_final["prices"][x]))
                print(Fore.GREEN + "-------------------------------------------------------------------------------------------")
                print(Fore.BLUE + "Name:\t" + Fore.MAGENTA + data_final["names"][x])
                print(Fore.GREEN + "-------------------------------------------------------------------------------------------")
                print(Fore.BLUE + "Image:\t" + Fore.MAGENTA + data_final["images"][x])
    print(Back.RED + "-------------------------------------------------------------------------------------------" + Back.RESET)