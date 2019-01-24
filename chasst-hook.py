# -*- coding: utf-8 -*-

import bs4			
import requests
import time
import eventlet
import DiscordHooks

webhook_url = ""
news_url = "https://www.ru.playblackdesert.com/News/Notice?boardType=0"

file_name = "boards.txt"
boards = list()

type_news = {
	"type01": "Объявления",
	"type02": "Обновления",
	"type03": "Ивенты",
	"type04": "Заметки ГМ",
	"type05": "Премиум магазин",
}

color_news = {
	"type01": 0x00a8ff,
	"type02": 0xffa800,
	"type03": 0xffa800,
	"type04": 0xea5b5b,
	"type05": 0x283642,
}

def send_webhook(board_no, title, ntype):
	embed = DiscordHooks.Embed(type_news[ntype], 
		url="https://www.ru.playblackdesert.com/News/Notice/Detail?boardNo=" + str(board_no), 
		description=title, color=color_news[ntype])
	DiscordHooks.Hook(hook_url=webhook_url, embeds=[embed]).execute()

def get_data():
	timeout = eventlet.Timeout(10)
	try:
		page = requests.get(news_url)
		return page
	except eventlet.timeout.Timeout:
		return None
	finally:
		timeout.cancel()

def check_news():
	page = get_data()
	if page:
		parser = bs4.BeautifulSoup(page.text, "html.parser")
		news = parser.find_all('tr')
		for cell in news[1:]:
			ntype = cell.find("div").get("class")[0]
			news_no = str(cell.find('a').get("data-boardno"))
			if not news_no in boards:
				title = str(cell.find("a").next).strip()
				send_webhook(news_no, title, ntype)
				boards.append(news_no)
				time.sleep(5)

				with open(file_name, 'w') as file:
					for i in boards:
						file.write(i+"\n")
					
	if len(boards) > 12:
		boards.pop(0)

def main():
	with open(file_name) as file:
		for i in file:
			boards.append(i.splitlines()[0])

	while True:
		check_news()
		time.sleep(60 * 5)

if __name__ == "__main__":
	main()
	
