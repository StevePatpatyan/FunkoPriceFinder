from requests_html import HTMLSession

session = HTMLSession()

def pop_data_finder(website, pop_class, price_class, name_class, image_class):
    request = session.get(website)

    pops = request.html.find(pop_class)

    names = []

    imgs = []

    prices = []

    for pop in pops:
        prices.append(pop.find(price_class, first=True))

    prices = [int(price.text.replace("$", "").replace(",", "")) if price.text.replace("$", "").replace(",", "").isnumeric() else price.text for price in prices]
    
    for pop in pops:
        names.append(pop.find(name_class, first=True).text)

    for pop in pops:
        imgs.append(pop.find(image_class, first=True).find("img", first=True).attrs["srcset"].split(",")[-1].strip("\n"))

    return {"prices": prices, "names": names, "images": imgs}


def filter_min(data):
    new_data = dict(data)
    new_data["prices"] = [price if type(price) == int else 9999999999999999999 for price in new_data["prices"]]
    new_data["names"] = [name for name in new_data["names"] if new_data["prices"][new_data["names"].index(name)] == min(new_data["prices"])]
    new_data["images"] = [img for img in new_data["images"] if new_data["prices"][new_data["images"].index(img)] == min(new_data["prices"])]
    new_data["prices"] = [str(price) + " (min)" for price in new_data["prices"] if price == min(new_data["prices"])]
    return new_data

def filter_max(data):
    new_data = dict(data)
    new_data["prices"] = [price if type(price) == int else -1 for price in new_data["prices"]]
    new_data["names"] = [name for name in data["names"] if new_data["prices"][new_data["names"].index(name)] == max(new_data["prices"])]
    new_data["images"] = [img for img in new_data["images"] if new_data["prices"][new_data["images"].index(img)] == max(new_data["prices"])]
    new_data["prices"] = [str(price) + " (max)" for price in new_data["prices"] if price == max(new_data["prices"])]
    return new_data