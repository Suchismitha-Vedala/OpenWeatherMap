import math,numpy as np,os,pandas as pd,time
import config as cfg
import threading, json,pymongo
from pymongo import MongoClient
from urllib import urlopen
import webbrowser

def Insert_Database(data, report_type):
	client = MongoClient('mongodb://localhost:27017')
	db = client['Open_Weather_API']
	if(report_type=="fiveday"):
		test=db.fiveday
	if(report_type=="16day"):
		test=db.sixteenday
	if(report_type=="weather_map"):
		test=db.weather_map
	test.insert(data)
	#print("Inserted into Database", report_type)

def get_data(url,report_type):
	time.sleep(30)#making sure only 1 API call is made per second.
	response = urlopen(url).read().decode('utf-8')
	obj = json.loads(response)
	Insert_Database(obj, report_type)
	if(report_type=="weather_map"):
		if('main' in obj.keys()):
			if (obj['main']['temp_min']<256.484):
				print "AlERT! Temperature less than 2 degree Farenheit in ", str(obj['name']) 
	else:
		for each in range(len(obj)):
			if(obj['list'][each]['main']['temp_min']<256.484):
				print "AlERT! Temperature less than 2 degree Farenheit in ", str(obj['city']['name']), " on ", str(obj['list'][each]['dt_txt'])
			if (('snow' in obj['list'][each].keys()) and any(obj['list'][each]['snow'])):
				print "It is snowing in ", str(obj['city']['name']), " on ", str(obj['list'][each]['dt_txt'])
			if (('rain' in obj['list'][each].keys()) and any(obj['list'][each]['rain'])):
				print "It is Raining in ", str(obj['city']['name']), " on ", str(obj['list'][each]['dt_txt'])
				
			'''
			if(obj['list'][each]['main']['temp_min']<256.484):
				print("AlERT! Temperature less than 2 degree Farenheit in ", obj['city']['name'], " on ", obj['list'][each]['dt_txt'])
			if (('snow' in obj['list'][each].keys()) and any(obj['list'][each]['snow'])):
				print("It is snowing in ", obj['city']['name'], " on ", obj['list'][each]['dt_txt'])
			if (('rain' in obj['list'][each].keys()) and any(obj['list'][each]['rain'])):
				print("It is Raining in ", obj['city']['name'], " on ", obj['list'][each]['dt_txt'])
			'''




def view_map(url2,report_type):
	webbrowser.open(url2)
	print("Opening Weather Map in New window")

def main():
	jobs = []
	ids=cfg.city_id
	for each in ids:
		fiveday = threading.Thread(target=get_data, args=(cfg.url_5day+str(each)+'&APPID='+cfg.api_key,"fiveday"))
		jobs.append(fiveday)
		weather_map = threading.Thread(target=get_data, args=(cfg.url_weather+cfg.api_key+"&id="+str(each),"weather_map"))
		jobs.append(weather_map)
		view=threading.Thread(target=view_map, args=(cfg.url_view+str(each),"viewing_map"))
		jobs.append(view)

		#Paid Version
		#sixteen_day = threading.Thread(target=get_data, args=(cfg.url_16day+str(each)+cfg.api_key,"16day"))
		#jobs.append(sixteen_day)
	for each in jobs:
		each.start()

main()


            



