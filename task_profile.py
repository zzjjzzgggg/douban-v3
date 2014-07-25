#! /usr/bin/env python
#coding=utf-8

from config import *
from queue import Queue
from workers import *
import dao


def process():
	uidQueue=Queue(1000)

	# workers are ready
	proxies=conf.getint('default','proxies')
	workers=conf.getint('default','threads_per_proxy')
	for proxyid in range(proxies):
		for i in range(workers):
			name='worker_%d_%d' % (proxyid, i)
			worker=CTHarvestor(name, proxyid, uidQueue)
			worker.start()
	
	olduids=set()
	while True:
		while not uidQueue.empty(): time.sleep(10)
		uids=dao.getUids(1000) - olduids
		print('Fetched ', len(uids))
		if len(uids)==0: break
		for uid in uids: uidQueue.put(uid)
		olduids=uids
		time.sleep(10)

	print('waite to finish....')
	uidQueue.join()
	
if __name__=='__main__':
	process()
