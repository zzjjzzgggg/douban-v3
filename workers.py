#coding: utf-8

from config import *
import threading
import dao
from httpclient import HttpClient
from doubanclient import DoubanClient
from tag import Tag
from collection import Collection
from random import randrange

# Collection and tag harvestor
class CTHarvestor(threading.Thread):
	def __init__(self, name, proxyid, uidQueue):
		threading.Thread.__init__(self)
		self.daemon=True
		self.name=name
		self.proxyid=proxyid
		self.queue=uidQueue

	def run(self):
		httpClient=HttpClient(self.proxyid)
		keysv1=conf.getint('default', 'keysv1')
		n=0
		while True:
			if n%100==0:
				keyv1=conf.get('keyv1', 'key%d' % randrange(keysv1))
				dbclientv1=DoubanClient(keyv1, httpClient)
				tagClient=Tag(dbclientv1)
				colClient=Collection(dbclientv1)
			n+=1
			uid=self.queue.get()
			print(self.name, 'is processing', uid)
			try:
				movietags=tagClient.getTagsAll(uid, 'movie')
				musictags=tagClient.getTagsAll(uid, 'music')
				booktags=tagClient.getTagsAll(uid, 'book')
				movies=colClient.getMoviesAll(uid)
				books=colClient.getItemsAll(uid, 'book')
				music=colClient.getItemsAll(uid, 'music')
				dao.saveTC(uid, movietags, musictags, booktags, movies, music, books)
			except Exception as e: print(uid, e)
			self.queue.task_done()

