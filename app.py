from requests_html import HTMLSession
from colorama import Fore, Back, Style
import sys
import exceptions
import pandas
from functions import pop_data_finder, filter_min, filter_max

args = sys.argv[1:]

options = ["help", "bb", "sx", "min", "max", "gf"]

web_options = {"sx": "Searches for funkos on StockX"}

web_args = [arg for arg in args if arg in web_options]

category_options = {"bb": "Searches for funkos of the emmy-winning Breaking Bad", "gf": "Searches for funkos of the legendary trilogy of The Godfather"}

category_args = [arg for arg in args if arg in category_options]

full_names = {"sx": "StockX", "bb": "Breaking Bad", "gf": "The Godfather"}

data_altering_options = {"min": "Finds funkos with lowest ask price in all given categories and websites", "max": "Finds funkos with highest ask price in all given categories and websites"}

data_altering_functions = {"min": filter_min, "max": filter_max}

data_altering_args = {cmd: func for cmd, func in data_altering_functions.items() if cmd in args}

#tuple: (website, pop html class, pop price html class, pop name html class, pop image html class)
web_data = {"sx": {"bb": ("https://stockx.com/search?s=breaking+bad+funko", ".css-1yh5062", ".css-nsvdd9", ".css-3lpefb", ".css-tkc8ar"), "gf": ("https://stockx.com/search?s=godfather+funko", ".css-1yh5062", ".css-nsvdd9", ".css-3lpefb", ".css-tkc8ar")}}

if len(args) == 0:
    raise exceptions.InputNotFound(Fore.RED + "No options selected...")

for arg in args:
    if arg not in options:
        raise exceptions.OptionNotFound(Fore.RED + "Option: \"" + arg + "\" not valid.")
    
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
    for option in data_altering_options:
        print(Fore.BLUE + option + ":\t" + data_altering_options[option])
    print(Back.LIGHTRED_EX + "-------------------------------------------------------------------------------------------" + Back.RESET)

if len(args) > 1 and "help" in args or len(args) > 0 and "help" not in args:
    print(Back.RED + "-------------------------------------------------------------------------------------------" + Back.RESET)
    for web_arg in web_args:
        print(Fore.CYAN + Style.BRIGHT + "Website:\t" + Fore.MAGENTA + full_names[web_arg] + ":" + Fore.RESET)
        for category_arg in category_args:
            print(Style.BRIGHT + "-------------------------------------------------------------------------------------------" + Style.NORMAL)
            print(Fore.CYAN + Style.BRIGHT + "Category:\t" + Fore.MAGENTA + full_names[category_arg] + ":")
            data = pop_data_finder(*web_data[web_arg][category_arg])
            data_final = data
            if len(data_altering_args) > 0:
                data_final = {"prices": [], "names": [], "images": []}
            for altering in data_altering_args:
                for stat in data:
                    data_final[stat] += data_altering_args[altering](data)[stat]
            for x in range(len(data_final["prices"])): 
                print(Back.GREEN + "-------------------------------------------------------------------------------------------" + Back.RESET)
                print(Fore.BLUE + "Price:\t" + Fore.MAGENTA + str(data_final["prices"][x]))
                print(Fore.GREEN + "-------------------------------------------------------------------------------------------")
                print(Fore.BLUE + "Name:\t" + Fore.MAGENTA + data_final["names"][x])
                print(Fore.GREEN + "-------------------------------------------------------------------------------------------")
                print(Fore.BLUE + "Image:\t" + Fore.MAGENTA + data_final["images"][x])
    print(Back.RED + "-------------------------------------------------------------------------------------------" + Back.RESET)