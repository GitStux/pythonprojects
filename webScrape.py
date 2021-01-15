from bs4 import BeautifulSoup
from requests import get
from contextlib import closing
import pandas as pd
import re

"""
Author: Matt Janousek

This program allows user input to search for items on Newegg.com and create an Excel document
with the output.
"""


def urlgrab(url):  # returns the response content from the provided url argument
    with closing(get(url, stream=True)) as resp:
        return resp.content


def getcards(user_input):  # grabs the items from the webpage and stores the selected information
    url = f'https://www.newegg.com/p/pl?d='

    for i in user_input:  # loops through the user_input to add to url
        url += i
        if i != user_input[-1]:
            url += "+"
    print(url + "&PageSize=96")
    response = urlgrab(url + "&PageSize=96")

    cardNames = []
    cardPrice = []
    cardStock = []

    soup = BeautifulSoup(response, 'html.parser')
    card_finder = soup.findAll("div", attrs={'class': 'item-container'})  # grabs the div holding all item cards
    price_box = soup.findAll("div", attrs={'class': "item-action"})  # grabs the div that holds each item's price

    for a in card_finder:  # finds and stores the item's availability and brand name
        try:
            name = a.find('a', attrs={'class': 'item-title'})
            cardNames.append(name.text)

            stock = a.p.text
            cardStock.append(stock)

        except AttributeError:
            cardStock.append("In stock")

    for i in price_box:  # find and store the item's price
        try:
            p = i.find(re.compile("^strong"))
            cardPrice.append(p.text)

        except AttributeError:
            cardPrice.append("$$$$")

    panda_time(cardStock, cardNames, cardPrice)  # panda pass


def panda_time(cardStock, cardNames, cardPrice):  # takes the filtered information from getcards() and creates an
    # Excel doc
    try:
        df = pd.DataFrame({"In Stock?": cardStock, "Item Name": cardNames, "Item Price": cardPrice})
        df.to_excel('NeweggSearch.xlsx', index=False)
    except ValueError:
        print("Sorry could not output Excel document at this time. ")


def main():
    user_input = input("Search Newegg >> ").lower().split(" ")
    getcards(user_input)


if __name__ == "__main__":
    main()
