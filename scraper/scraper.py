import requests
from bs4 import BeautifulSoup
import csv
import json
import re
import pandas


BASE_URL = 'https://www.apartments.com/'
extension = 'new-york-ny/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:68.0) Gecko/20100101 Firefox/68.0'
}

data = {'properties': []}


def get_url_list():
    '''return a list of property URLs to parse in a given polygon'''
    soup = get_page(BASE_URL + extension)
    page_urls = get_all_page_urls(soup)
    listing_ids = []
    for url in page_urls:
        page = get_page(url)
        listing_ids += get_property_ids_from_page(page)

    return listing_ids


def get_page(url):
    '''get request a page and return beautiful soup object'''
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content, 'html.parser')


def get_all_page_urls(soup):
    '''Get all the urls needed to iterate over all the placards'''
    pages = soup.find('div', {'id': 'placardContainer'}).find('div', {'id': 'paging'}).find_all('a')
    start_page = pages[1].text
    last_page = pages[len(pages)-2].text
    return [BASE_URL+extension+str(page_number) for page_number in range(int(start_page), int(last_page) + 1)]


def get_property_ids_from_page(soup):
    '''get list of property listing IDs'''
    placards = soup.find('div', {'id': 'placardContainer'}).find_all('article', {})
    return [placard['data-listingid'] for placard in placards]


def get_property_address(soup):
    '''given page, extract address'''
    script = soup.find_all('script', type='text/javascript')[2].text
    address = find_tag(script, 'listingAddress') + ', ' + find_tag(script, "listingCity") + \
        ', ' + find_tag(script, "listingState") + ' ' + find_tag(script, "listingZip")
    print(address)


def find_tag(text, tag):
    '''helper method for get_property_address'''
    tag = tag + ": \'"
    start = text.find(tag) + len(tag)
    end = text.find("\',", start)
    return str(text[start: end])


def get_building_data(url):
    '''Get the data from the table of apartments associated with the building'''


def write_csv():
    '''write data structure (in format in testing/data_structure.json) to a csv file'''


def create_csv_file():
    '''create a csv file for writing data'''


def main():
    '''
    '''


if __name__ == '__main__':
    main()
