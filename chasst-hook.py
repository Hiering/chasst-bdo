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

def send_webhook(board_no, title):
	embed = DiscordHooks.Embed(title, 
		url="https://www.ru.playblackdesert.com/News/Notice/Detail?boardNo=" + str(board_no), 
		description=title, color=0xFF851B)
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
		news = parser.find_all(class_='td')
		for cell in news:
			news_no = str(cell.find('a').get("data-boardno"))
			if not news_no in boards:
				title = str(cell.find("a").next).strip()
				send_webhook(news_no, title)
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
