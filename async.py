# -*- coding: utf-8 -*-
# Python 3 версии
 
import os
import urllib.request
from threading import Thread

class DownloadThread(Thread):
	"""
	Пример скачивание файла используя многопоточность
	"""
	
	def __init__(self, url, name):
		"""Инициализация потока"""
		Thread.__init__(self)
		self.name = name
		self.url = url
	
	def run(self):
		"""Запуск потока"""
		handle = urllib.request.urlopen(self.url)
		fname = os.path.basename(self.url)
	
		with open(fname, "wb") as f_handler:
			while True:
				chunk = handle.read(1024)
				if not chunk:
					break
				f_handler.write(chunk)
		

		print("%s закончил загрузку %s!" % (self.name, self.url))


def main(urls):
	"""
	Запускаем программу
	"""
	for item, url in enumerate(urls):
		name = "Поток %s" % (item+1)
		thread = DownloadThread(url, name)
		thread.start()
 
if __name__ == "__main__":
	urls = [
		"https://www.amxmodx.org/amxxdrop/1.8/amxmodx-1.8.3-dev-git5154-base-windows.zip",
		"http://teamcity.rehlds.org/guestAuth/repository/download/ReGameDLLCs_Linux/.lastSuccessful/releaseRegamedllFixes/libcs.so",
		"http://teamcity.rehlds.org/guestAuth/repository/download/Metamod_Linux/.lastSuccessful/release/metamod_i386.so",
		"http://teamcity.rehlds.org/guestAuth/repository/download/ReVoice_Linux/.lastSuccessful/release/librevoice_mm_i386.so",
		"http://teamcity.rehlds.org/guestAuth/repository/download/Reapi_Linux/.lastSuccessful/release/reapi_amxx_i386.so"
	]
 
	main(urls)