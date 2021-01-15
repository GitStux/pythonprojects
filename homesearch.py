from bs4 import BeautifulSoup
from requests import get
import pandas as pd
import datetime as dt

"""
Author: Matt Janousek

This program searches for 4+ bedroom homes in Puyallup, WA and appends an Excel doc to see trends.
"""


def panda_time(locationlist, pricelist, bedroomlist, bathroomlist, regionlist):  # appends an Excel doc to see
    # trending data posted on Trulia.com
    try:
        with pd.ExcelWriter(r'C:\Users\Matt\PycharmProjects\morningWarmup\Homelistings.xlsx', mode='a') as writer:
            df = pd.DataFrame(
                {"Price": pricelist, "Home Address": locationlist, "City": regionlist, "Bedrooms": bedroomlist,
                 "Bathrooms": bathroomlist})
            df.to_excel(writer, sheet_name=current.strftime("%d%b%y_%S"), index=False)

    except ValueError:
        print("Sorry could not output Excel document at this time. ")


def main():  # finds and stores home information from Trulia.com
    bedroomlist = []
    bathroomlist = []
    pricelist = []
    locationlist = []
    regionlist = []

    headers = {  # User-agent was needed for Trulia.com servers
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/72.0.3626.121 Safari/537.36'}
    url = get("https://www.trulia.com/for_rent/Puyallup,WA/4p_beds/", headers=headers)

    soup = BeautifulSoup(url.content, 'html.parser')
    homecard = soup.findAll("div", attrs={  # locates the div holding all home listing cards
        "class": "Grid__CellBox-sc-5ig2n4-0 SearchResultsList__WideCell-sc-183kqex-2 jLNYlr"})

    for x in homecard:  # for loop each inner div to locate specific information to be appended to separate lists

        try:
            price = x.find('div', attrs={'data-testid': 'property-price'})
            beds = x.find('div', attrs={'data-testid': 'property-beds'})
            bathroom = x.find('div', attrs={'data-testid': 'property-baths'})
            location = x.find('div', attrs={'data-testid': 'property-street'})
            region = x.find('div', attrs={'data-testid': 'property-region'})

            bedroomlist.append(beds.text)
            pricelist.append(price.text)
            bathroomlist.append(bathroom.text)
            locationlist.append(location.text)
            regionlist.append(region.text)

        except AttributeError:
            print("No info has been posted for this. ")
    panda_time(locationlist, pricelist, bedroomlist, bathroomlist, regionlist)


current = dt.datetime.now()  # datetime used to name each appended Excel sheet to see daily trends

if __name__ == "__main__":
    main()
