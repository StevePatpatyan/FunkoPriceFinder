from requests_html import HTMLSession
from colorama import Fore, Back, Style
import sys
import exceptions
import pandas
from functions import pop_data_finder, filter_min, filter_max

args = sys.argv[1:]

options = ["help", "bb", "sx", "min", "max", "legend"]

web_options = ["sx"]

web_args = [arg for arg in args if arg in web_options]

category_options = ["bb"]

category_args = [arg for arg in args if arg in category_options]

full_names = {"sx": "StockX", "bb": "Breaking Bad"}

data_altering_options = {"min": filter_min, "max": filter_max}

data_altering_args = {cmd: func for cmd, func in data_altering_options.items() if cmd in args}

#tuple: (website, pop html class, pop price html class, pop name html class, pop image html class)
web_data = {"sx": {"bb": ("https://stockx.com/search?s=breaking+bad+funko", ".css-1yh5062", ".css-nsvdd9", ".css-3lpefb", ".css-tkc8ar")}}

if len(args) == 0:
    raise exceptions.InputNotFound(Fore.RED + "No options selected...")

for arg in args:
    if arg not in options:
        raise exceptions.OptionNotFound(Fore.RED + "Option: \"" + arg + "\" not valid.")


prices = []

names = []

imgs = []

for web_arg in web_args:
    print(Back.RED + "-------------------------------------------------------------------------------------------" + Back.RESET)
    print(Fore.BLUE + Style.BRIGHT + "Website: " + Fore.MAGENTA + full_names[web_arg] + ":" + Fore.RESET)
    for category_arg in category_args:
        print(Style.BRIGHT + "-------------------------------------------------------------------------------------------")
        print(Fore.BLUE + Style.BRIGHT + "Category: " + Fore.MAGENTA + full_names[category_arg] + ":")
        data = pop_data_finder(*web_data[web_arg][category_arg])
        print(data)
        data_final = data
        if len(data_altering_args) > 0:
            data_final = {"prices": [], "names": [], "images": []}
        for altering in data_altering_args:
            for stat in data:
                data_final[stat] += data_altering_args[altering](data)[stat]
        for x in range(len(data_final["prices"])): 
            print(Back.GREEN + "-------------------------------------------------------------------------------------------" + Back.RESET)
            print(Fore.BLUE + "Price: " + Fore.MAGENTA + str(data_final["prices"][x]))
            print(Fore.GREEN + "-------------------------------------------------------------------------------------------")
            print(Fore.BLUE + "Name: " + Fore.MAGENTA + data_final["names"][x])
            print(Fore.GREEN + "-------------------------------------------------------------------------------------------")
            print(Fore.BLUE + "Image: " + Fore.MAGENTA + data_final["images"][x])
print(Back.RED + "-------------------------------------------------------------------------------------------" + Back.RESET)