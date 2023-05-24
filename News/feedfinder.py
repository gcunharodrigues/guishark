import feedfinder2

url = "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/derivativos/ajustes-do-pregao/"
feeds = feedfinder2.find_feeds(url)

for feed in feeds:
    print(feed)