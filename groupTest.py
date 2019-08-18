from main import MainInformation

url = 'https://www.rbc.ru/society/12/08/2019/5d4cd72b9a7947db471405d4?from=from_main'
info = MainInformation(url)
info.saveToFile()

url = 'https://www.gazeta.ru/politics/2019/08/13_a_12575359.shtml'
info = MainInformation(url)
info.saveToFile()

url = 'https://lenta.ru/news/2019/08/05/boompripas/'
info = MainInformation(url)
info.saveToFile()

url = 'https://lenta.ru/news/2019/08/13/shoes/'
info = MainInformation(url)
info.saveToFile()

url = 'https://www.gazeta.ru/business/2019/08/16/12582253.shtml'
info = MainInformation(url)
info.saveToFile()

url = 'https://expert.ru/expert/2014/02/idei-ne-ischezayut/'
info = MainInformation(url)
info.saveToFile()

url = 'https://habr.com/ru/post/463969/'
info = MainInformation(url)
info.saveToFile()
