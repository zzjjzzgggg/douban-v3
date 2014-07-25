#! /usr/bin/env python
#encoding: utf-8

from config import *
import urllib.request
import json, feedparser

class HttpClient:

	def __init__(self, proxyid=0):
		if proxyid>0:
			proxy=conf.get('proxy', 'proxy%d' % proxyid)
			proxy_handler = urllib.request.ProxyHandler({'http': proxy, 'https': proxy})
			self.opener = urllib.request.build_opener(proxy_handler)
		else:
			self.opener=urllib.request.build_opener()

	def _read(self, fp, encode):
		buf=''
		for l in fp: buf+=l.decode(encode)
		fp.close()
		return buf
	
	def getJson(self, url, encode='utf8'):
		for i in range(5):
			try:
				f=self.opener.open(url, timeout=7)
				return json.loads(self._read(f, encode))
			except Exception as e:
				print('Error!', e, 'Try again', i)
				time.sleep(3)
		return None
	
	def getFeed(self, url, encode='utf8'):
		for i in range(5):
			try:
				return feedparser.parse(url)
			except Exception as e:
				print('Error!', e, 'Try again', i)
				time.sleep(3)
		return None

if __name__=='__main__':
	client=HttpClient()
	#dat=client.getJson('https://api.douban.com/shuo/v2/users/1000001/followers')
	dat=client.getFeed('http://api.douban.com/people/sakinijino/collection?cat=movie')
	print(dat)
