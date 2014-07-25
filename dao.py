#! /usr/bin/env python
#coding=utf-8

import pymongo
import time
import random

db=pymongo.Connection('192.168.4.238', 27027).douban

def getUids(n):
	return {item['_id'] for item in db.tagcoll.find({'book':{'$exists':False}}, limit=n)}

def saveTC(uid, movietags, musictags, booktags, movies, music, books):
	db.tagcoll.update({'_id':uid}, {'$set':{'book':books, 'movie':movies, 'music':music, 'booktag':booktags, 'movietag':movietags, 'musictag':musictags}})

def test():
	print(getUids(2))

if __name__=='__main__':
	test()
