import urllib
import lxml
import database
import basic_sentiment_analysis
import nltk
import yaml
import sys
import os
import re
import datetime
from dateutil import parser
from pprint import pprint
from lxml import etree

page='http://www.amazon.com/Dekart-SIM-Card-Reader-Windows/product-reviews/B0045BIUGG/ref=cm_cr_getr_d_paging_btm_1?ie=UTF8&showViewpoints=1&sortBy=recent&pageNumber='

def GetPage(index):
	url=page+str(index)
	a=urllib.urlopen(url).read()
	return a
	

def GetDataFromPage(a, i):
	x=etree.HTML(a) 
	rating = x.xpath("string(//div[@id='cm_cr-review_list']/div["+str(i)+"]/div[1]/a[1]/i)")
	author =  x.xpath("string(//div[@id='cm_cr-review_list']/div["+str(i)+"]/div[2]/span[1]/a)")
	dat = x.xpath("string(//div[@id='cm_cr-review_list']/div["+str(i)+"]/div[2]/span[4])")
	datee = dat[3:]
	date = datetime.datetime.strptime(datee, '%B %d, %Y').date()
	text = x.xpath("string(//div[@id='cm_cr-review_list']/div["+str(i)+"]/div[4]/span)")
	splitted_sentences = splitter.split(text)
	pprint(splitted_sentences)
	pos_tagged_sentences = postagger.pos_tag(splitted_sentences)
	pprint(pos_tagged_sentences)
	dict_tagged_sentences = dicttagger.tag(pos_tagged_sentences)
	pprint(dict_tagged_sentences)
	emotion=basic_sentiment_analysis.sentiment_score(dict_tagged_sentences)
	if emotion > 0:
		emotion="pozitiv"
	elif emotion==0:
		emotion="neutral"
	else:
		emotion="negativ"
	dict = {}
	dict['rating']=rating[:4]
	dict['author']=author
	dict['date']=date
	dict['text']=text
	dict['emotion']=emotion
	return dict
	
	
qs = database.CommentStorage("feedback.db")
qs.CreateDb()
s = basic_sentiment_analysis.Splitter()
splitter = basic_sentiment_analysis.Splitter()
postagger = basic_sentiment_analysis.POSTagger()
dicttagger = basic_sentiment_analysis.DictionaryTagger([ 'dicts/positive.yml', 'dicts/negative.yml', 
                                                         'dicts/inc.yml', 'dicts/dec.yml', 'dicts/inv.yml'])

for j in range (1, 13):
	a = GetPage(j)
	for i in range(1, 11):
		data = GetDataFromPage(a,i)
		qs.AddComment(data['rating'], data['author'], data['date'], data['text'], data['emotion'])
		print i

qs.Close()		
print "Done!"		

	
	
