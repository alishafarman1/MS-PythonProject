import requests
import os.path
import json
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup

file_name = 'data.json'
data_source_url = 'https://codecanyon.net/search?sort=sales'
# Scrapper Begins


def parse_categories(page_tree):
    categories_stats = {}
    categories = page_tree.select('ul[data-test-selector="category-filter"] > li')
    for category in categories:
        categories_stats[category.a.get_text().capitalize()] = int(category.span.get_text().replace(",", ""))
    return categories_stats


def parse_tags(page_tree):
    tags_stats = {}
    tags = \
        page_tree.select('div[data-test-selector="search-filters"] > div:nth-child(1) > div:nth-child(3) > div > div')[0]
    prices = tags.select("a + span")
    names = tags.select("a > span:nth-child(2)")
    for index in range(len(tags)):
        tags_stats[names[index].get_text(strip=True).capitalize()] = int(prices[index].get_text().replace(",", ""))
    return tags_stats


def parse_compatibility(page_tree):
    compatibility_stats = {}
    tags = \
        page_tree.select('div[data-test-selector="search-filters"] > div:nth-child(1) > div:nth-child(7) > div > div')[0]
    prices = tags.select("a + span")
    names = tags.select("a > span:nth-child(2)")
    for index in range(len(tags)):
        compatibility_stats[names[index].get_text(strip=True).capitalize()] = int(
            prices[index].get_text().replace(",", ''))
    return compatibility_stats


def parse_dates(page_tree):
    date_stats = {}
    tags = \
        page_tree.select('div[data-test-selector="search-filters"] > div:nth-child(1) > div:nth-child(10) > div > div')[
            0]
    prices = tags.select("label + span")
    names = tags.select("label > span:nth-child(2)")
    for index in range(len(tags)):
        date_stats[names[index].get_text(strip=True).capitalize()] = int(prices[index].get_text().replace(",", ""))
    return date_stats


# Scrapper Ends

def scrap_and_save_data():
    page = requests.get(data_source_url)
    page_tree = BeautifulSoup(page.content, 'html.parser')
    with open(file_name, 'w') as outfile:
        json.dump([parse_tags(page_tree), parse_categories(page_tree), parse_dates(page_tree), parse_compatibility(page_tree)], outfile)


def init_matplot():
    plt.rc('font', **{'weight': 'bold', 'size': 12})
    fig, axs = plt.subplots(2, 2, figsize=(100, 10))
    plt.subplots_adjust(wspace=0.6)
    return axs


def create_plot(data, plot):
    names = list(data.keys())
    values = list(data.values())
    plot(names[1:6], values[1:6])


if not os.path.isfile(file_name):
    scrap_and_save_data()

with open(file_name) as json_file:
    axs = init_matplot()
    data = json.load(json_file)
    create_plot(data[0], axs[0, 0].bar)
    create_plot(data[1], lambda name, values: axs[0, 1].scatter(name, values, s=500))
    create_plot(data[2], axs[1, 0].plot)
    create_plot(data[3], axs[1, 1].barh)
    plt.show()
