import feedparser
from bs4 import BeautifulSoup
import datetime
from dateutil import parser

# Time of last news
last_news_time = '7h45'
last_news_time_datetime = datetime.datetime.strptime(last_news_time, '%Hh%M')

# Parse the RSS feed
feed = feedparser.parse("https://www.infomoney.com.br/tudo-sobre/ao-vivo/feed/")

# Get today date
today = datetime.date.today()

# Print out the titles of the articles
for entry in feed.entries:
    entry_datetime = parser.parse(entry.published)
    if entry_datetime.date() == today:
        entry_title = entry.title
        entry_published = entry.published
        entry_content = entry.content[0].value
        break

# keys = feed.entries[0].keys()
# print(keys)
# entry = feed.entries[0]
# print(entry.published)
# print(entry.published_parsed)
# print(entry.summary)
content = BeautifulSoup(entry_content, "html.parser")

list_titles = [title for title in content.find('div')]
list_titles = [x for x in list_titles if x != ' ']

for item in list_titles:
    item_update = item.find('span').get_text().split()
    item_time = item_update[1]
    item_time_datetime = datetime.datetime.strptime(item_time, '%Hh%M')
    if item_time_datetime < last_news_time_datetime:
        item_title = item.find('h2').get_text()
        print(item_time)
        print(item_title)
        
        item_text = item.find('p')
        if item_text:
            item_text = item_text.get_text()
            print(item_text) 
            
        item_list_list = item.find_all('li')
        for item_list in item_list_list:
            if item_list:
                item_list = item_list.get_text()
                print(item_list)


# news = BeautifulSoup(list_titles[481], "html.parser")
# print(list_titles[481].get_text())
# content = entry.content[0].value
# print(content)

# date1 = feed.entries[0].published 
# date_time_str = date1
# date_time = parser.parse(date_time_str)

# print(date_time)