import feedparser
from bs4 import BeautifulSoup
import datetime
from dateutil import parser
import guishark_msg

# Time of last news
first_news_time = '6h55'
last_news_time = '7h07'
first_news_time_datetime = datetime.datetime.strptime(first_news_time, '%Hh%M')
last_news_time_datetime = datetime.datetime.strptime(last_news_time, '%Hh%M')

# Parse the RSS feed
feed = feedparser.parse("https://www.infomoney.com.br/tudo-sobre/ao-vivo/feed/")

# Get today date
today = datetime.date.today()
# today = datetime.datetime.strptime('2023-01-06', '%Y-%m-%d')
# today = today.date()
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

item_list =[]
for item in list_titles:
    each_item_list=[]
    item_update = item.find('span').get_text().split()
    item_time = item_update[1]
    item_time_datetime = datetime.datetime.strptime(item_time, '%Hh%M')
    each_item_list.append(item_time)
    
    if item_time_datetime < last_news_time_datetime and \
        item_time_datetime >= first_news_time_datetime:
        item_title = '*' + item.find('h2').get_text() + '*'
        each_item_list.append(item_title)
          
        item_text = item.find('p')
        if item_text:
            item_text = item_text.get_text() 
            each_item_list.append(item_text)
        
        each_item_list_list=[]    
        item_list_list = item.find_all('li')
        for list_html in item_list_list:
            if list_html:
                list_html = list_html.get_text()
                each_item_list_list.append(list_html)
        each_item_list.append(each_item_list_list)    
        item_list.append(each_item_list)

news_message_list = [] 
for item in item_list:
    item = [x for x in item if x]
    news_message_list.append(item[1:])

for news_message in news_message_list:
    index_1 = news_message_list.index(news_message)
    for message in news_message:
        index_2 = news_message.index(message)
        if isinstance(message, list):
            news_message_list[index_1][index_2] = '\n'.join(['\t- ' + x for x in message])

merged_news_list = []
for news_message in reversed(news_message_list):
    merged_news = '\n'.join(news_message)
    merged_news_list.append(merged_news)

merged_news_list.insert(0, 'Panorama Diário\n') 
    
# tosend_merged_news_list = 'Panorama Diário\n\n' + '\n\n'.join(merged_news_list)

with open('bot_token.txt') as f:
    token = f.read()
with open('chat_id.txt') as f:
    chat_id = f.read()
with open('chat_id2.txt') as f:
    chat_id2 = f.read()
for news in merged_news_list:
    guishark_msg.send_message(token, chat_id, news)
    guishark_msg.send_message(token, chat_id2, news)