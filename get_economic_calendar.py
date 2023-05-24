from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time
import guishark_msg

def send_sched_msg(time_now, sched_list, *args):
    ant_message = args[0]
    for data in sched_list:
        datetime_test = data[0] - datetime.timedelta(minutes=5)
        previous_minute = time_now + datetime.timedelta(minutes=-1)
        if datetime_test > previous_minute and datetime_test < time_now:
           message = ant_message + data[1]
           guishark_msg.send_message(token, chat_id, message)
           sched_list = [x for x in sched_list if x != data]
    return sched_list

def zipping_lists(time_list, text_list):
    aux_time_list=[]
    for sched in time_list:
        datetime_sched = datetime.datetime.strptime(sched, '%H:%M').time()
        datetime_sched = datetime.datetime.combine(datetime.date.today(), 
                                               datetime_sched)
        aux_time_list.append(datetime_sched)
    zipped_list = [list(x) for x in zip(aux_time_list, text_list)]
    return zipped_list  

def get_last_news_time(all_time_list):
    aux_list = []
    for sched in all_time_list:
        datetime_sched = datetime.datetime.strptime(sched, '%H:%M').time()
        datetime_sched = datetime.datetime.combine(datetime.date.today(), 
                                                datetime_sched)
        aux_list.append(datetime_sched)
    last_news_time = max(aux_list)
    return last_news_time

# Make a GET request to the economic calendar page
url = 'https://br.investing.com/economic-calendar/'
r = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
response = urlopen(r).read()

# Parse the HTML content
soup = BeautifulSoup(response, 'html.parser')

# Find the table rows with the calendar events
events = soup.find_all('tr')

# Filter the events with USD or BRL currency
filtered_events = []
for event in events:
    currency = event.find('td', class_='left flagCur noWrap')
    if currency:
        currency = currency.get_text().strip()
        if currency in ('USD', 'BRL'):
            filtered_events.append(event)

merged_events = []
for event in filtered_events:
    event_textlist = event.get_text().split('\n')
    event_textlist = [x.strip() for x in event_textlist if x]
    bulls = event.find_all(class_='grayFullBullishIcon')
    event_textlist.append(str(len(bulls)))
    merged_events.append(event_textlist)  

df = pd.DataFrame(merged_events)
df.replace(to_replace='', value='None', inplace=True)
df.replace(to_replace='BRL', value='🇧🇷 BRL', inplace=True)
df.replace(to_replace='USD', value='🇺🇸 USD', inplace=True)

df1 = df[[0,1,2]]

try:
    df2 = df[[3,4,5,6,7]]
    df2 = df2.where(pd.isnull(df[7]), df.shift(-1, axis=1))
except:
    df2 = df[[3,4,5,6]]

df = pd.concat([df1, df2], axis=1)

try:
    df.drop(columns=[3,7], inplace=True)
except:
    df.drop(columns=[3], inplace=True)
   
df = df.reindex(columns=[1,0,6,2,4,5])

df[6].replace(to_replace='1', value='🦈    ', inplace=True)
df[6].replace(to_replace='2', value='🦈🦈  ', inplace=True)
df[6].replace(to_replace='3', value='🦈🦈🦈', inplace=True)
df[4].replace(to_replace='None', value='Sem Projeção', inplace=True)
df[5].replace(to_replace='None', value='Sem Prévia', inplace=True)

finalized_news_list = df.values.tolist()
news_text_list =[]
time_text_list =[]
for news in finalized_news_list:
    schedule_news = news[1]
    text = f'{news[0]} - {news[1]}: {news[2]} {news[3]}, \
est. {news[4]}, ant. {news[5]}'
    news_text_list.append(text)
    time_text_list.append(schedule_news)
       
message_calendar1 = 'Calendário Econômico\n\n'+'\n\n'.join(news_text_list) +\
'\n\n\nAbra a sua conta no BTG: http://www.uriel.pro/btg\n\nVenha fazer parte \
do nosso grupo de ideias de trades: http://www.uriel.pro/gruposhark'

df_important = df.loc[df[6] == '🦈🦈🦈']
important_news_list = df_important.values.tolist()
important_news_text_list =[]
important_news_time_list = []
for news in important_news_list:
    schedule_important_news = news[1]
    text = f'{news[0]} - {news[1]}: {news[2]} {news[3]}, \
est. {news[4]}, ant. {news[5]}'
    important_news_text_list.append(text)
    important_news_time_list.append(schedule_important_news)

with open('bot_token.txt') as f:
    token = f.read()
with open('chat_id.txt') as f:
    chat_id = f.read()

guishark_msg.send_message(token, chat_id, message_calendar1)

if len(important_news_list) > 0:
    message_calendar2 = 'Observações em relação ao Calendário econômico:\n\n\
⚠️ Atenção ⚠️\n\n'+'\n\n'.join(important_news_text_list)
    
else:
    message_calendar2 = 'Observações em relação ao Calendário econômico:\n\n\
Sem notícias relevantes\n\n'
          
guishark_msg.send_message(token, chat_id, message_calendar2) 

sched_time_list = important_news_time_list
sched_text_list = important_news_text_list

zip_time_text_list = zipping_lists(sched_time_list, sched_text_list)

abertura_mercados_time = ['09:00', '10:00', '10:30', '09:10']
abertura_mercados_text = ['⚠️ Atenção ⚠️\n9:00: Abertura BMF',
                          '⚠️ Atenção ⚠️\n10:00: Abertura B3', 
                          '⚠️ Atenção ⚠️\n10:30: Abertura NY',
                          'Bom dia, Sharks!']

zip_abertura_mercados = zipping_lists(abertura_mercados_time, 
                                      abertura_mercados_text)

for x in zip_time_text_list:
    print(x)
for x in zip_abertura_mercados:
    print(x)

all_time_list = sched_time_list + abertura_mercados_time
last_news_time = get_last_news_time(all_time_list)

print(datetime.datetime.now())
print(last_news_time)

active = True
while active:
    
    time_now = datetime.datetime.now()
    atencao_important_msg = '⚠️ Atenção ⚠️\n\n'
    
    zip_time_text_list = send_sched_msg(time_now, zip_time_text_list, 
                                        atencao_important_msg)
    zip_abertura_mercados = send_sched_msg(time_now, zip_abertura_mercados,
                                            '')    
    
    if time_now > last_news_time:
        active = False
        
    time.sleep(60) 