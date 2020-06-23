from bs4 import BeautifulSoup
import requests

page = requests.get('https://codecanyon.net/category/all?sort=sales')
pageTree = BeautifulSoup(page.content, 'html.parser')


def parse_categories():
    categories_stats = []
    categories = pageTree.select('ul[data-test-selector="category-filter"] > li')
    for category in categories:
        categories_stats.append((category.a.get_text(), int(category.span.get_text().replace(",", ""))))
    return categories_stats


def parse_tags():
    tags_stats = []
    tags = \
        pageTree.select('div[data-test-selector="search-filters"] > div:nth-child(1) > div:nth-child(3) > div > div')[0]
    prices = tags.select("a + span")
    names = tags.select("a > span:nth-child(2)")
    for index in range(len(tags)):
        tags_stats.append(
            (names[index].get_text(strip=True).capitalize(), int(prices[index].get_text().replace(",", ""))))
    return tags_stats


def parse_compatibility():
    compatibility_stats = []
    tags = \
        pageTree.select('div[data-test-selector="search-filters"] > div:nth-child(1) > div:nth-child(7) > div > div')[0]
    prices = tags.select("a + span")
    names = tags.select("a > span:nth-child(2)")
    for index in range(len(tags)):
        compatibility_stats.append(
            (names[index].get_text(strip=True).capitalize(), int(prices[index].get_text().replace(",", ""))))
    return compatibility_stats


def parse_dates():
    date_stats = []
    tags = \
        pageTree.select('div[data-test-selector="search-filters"] > div:nth-child(1) > div:nth-child(10) > div > div')[0]
    prices = tags.select("label + span")
    names = tags.select("label > span:nth-child(2)")
    for index in range(len(tags)):
        date_stats.append(
            (names[index].get_text(strip=True).capitalize(), int(prices[index].get_text().replace(",", ""))))
    return date_stats


print(parse_dates())
