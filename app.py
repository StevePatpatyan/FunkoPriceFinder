from requests_html import HTMLSession
from colorama import Fore, Back, Style
from  time import sleep
session = HTMLSession()


request = session.get("https://stockx.com/search/lowest-ask?s=breaking+bad+funko")

pops = request.html.find(".css-1yh5062")

names = []

imgs = []

for pop in pops:
    names.append(pop.find(".css-3lpefb", first=True).text)

for pop in pops:
    imgs.append(pop.find(".css-tkc8ar", first=True).find("img", first=True).attrs["srcset"].split(",")[-1].strip("\n"))

asks = request.html.find(".css-nsvdd9")

asks = [int(ask.text.replace("$", "").replace(",", "")) if ask.text != "--" else 9999999999 for ask in asks]

for x in range(asks.count(min(asks))):
    print(Style.BRIGHT + "-------------------------------------------------------------------------------------------" + Back.RESET)
    print(Fore.BLUE + "Price:\t", Fore.MAGENTA + str(min(asks)))
    print(Fore.GREEN + "-------------------------------------------------------------------------------------------")
    print(Fore.BLUE + "Name:\t", Fore.MAGENTA + names[asks.index(min(asks))])
    print(Fore.GREEN + "-------------------------------------------------------------------------------------------")
    print(Fore.BLUE + "Image:\t", Fore.MAGENTA + imgs[asks.index(min(asks))])
    print(Fore.GREEN + "-------------------------------------------------------------------------------------------")
    asks.remove(min(asks))