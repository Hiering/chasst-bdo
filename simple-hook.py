# -*- coding: utf-8 -*-

import bs4			
import requests
import time
import eventlet
import DiscordHooks

webhook_url = "https://discordapp.com/api/webhooks/502380587361763328/_h_rA9UWWtSUnX-A5BFiNC-8aP3WT3FdN0EO8vikFmDrTKkdDZbLelrRPFCPRkmpJ5AD"
news_url = "https://www.ru.playblackdesert.com/News/Notice?boardType=0"
boards = list()

def send_webhook(board_no, title):
	embed = DiscordHooks.Embed(title='look here', 
		url="https://www.ru.playblackdesert.com/News/Notice/Detail?boardNo=" + board_no, 
		description=title, color=0x001f3f)
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
	parser = bs4.BeautifulSoup(page.text, "html.parser")
	news = parser.find_all(class_='td')
	for cell in news:
		news_no = str(cell.find('a').get("data-boardno"))
		if not news_no in boards:
			title = str(cell.find("a").next).strip()
			send_webhook(news_no, title)
			boards.append(news_no)
	if len(boards) > 15:
		boards.pop(0)

def main():
	page = requests.get(news_url)
	parser = bs4.BeautifulSoup(page.text, "html.parser")
	news = parser.find_all(class_='td')
	for cell in news:
		boards.insert(0, str(cell.find('a').get("data-boardno")))
	
	while True:
		check_news()
		time.sleep(60 * 5)

if __name__ == "__main__":
	main()