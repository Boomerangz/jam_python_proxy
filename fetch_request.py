import  httplib,urllib 
import time
import datetime
import threading
import json
import codecs
import MySQLdb



def fetchRequest(location):
	basic_address="/v2/venues/search"
	category="categoryId=4bf58dd8d48988d17f941735"
	version_string="v=20130805"
	client_string="client_id=ATCDKP1BI3F1YDPOHVOWI2UCEXIUFWGPR0GF3DOVSLJFRFBM&client_secret=YADGMVO5M5QJTZXXIDEIIDOYTRS5KLI5QHUQKB5DZ22ADROO"
	FSQ_TYPE_CINEMA = "4bf58dd8d48988d17f941735";
	FSQ_TYPE_CLUB = "4bf58dd8d48988d11f941735";
	FSQ_TYPE_HOTEL = "4bf58dd8d48988d1fa931735";
	FSQ_TYPE_FOOD = "4d4b7105d754a06374d81259";
	FSQ_TYPE_MARKET = "4d4b7105d754a06378d81259";
	FSQ_TYPE_THEATER = "4bf58dd8d48988d137941735";	
	FSQ_TYPE_COFFEE = "4d4b7105d754a06374d81259";
	FSQ_TYPE_BAR = "4d4b7105d754a06376d81259";
	FSQ_UNDEFINED = "??????????1";
	TYPES_ARRAY = [FSQ_TYPE_CINEMA,FSQ_TYPE_CLUB,FSQ_TYPE_FOOD,FSQ_TYPE_THEATER];

	output=[]
	ll="near="+location

	category_range=[FSQ_TYPE_CINEMA];
	threads=[]
	for cat_str in category_range:
		thrd=threading.Thread(target=lambda:getDataForCategory(cat_str))
		threads.append(thrd)
		thrd.daemon = True
		thrd.start()

	for thrd in threads:
		thrd.join()
	dt_end=time.time();
	diff=dt_end-dt_begin
	output={'location':location,'places':output,'events':getEvents(0),'films':getEvents(2),'my_recommendations':[]}
	output= json.dumps(output)
	return output;


def getEvents(rubr_id):
#	params = urllib.urlencode({'key': 'YADGMVO5M5QJTZXXIDEIIDOYTRS5KLI5QHUQKB5DZ22ADROO', 'rubr_id':'0', 'date_start': '2013-08-06', 'date_start': '2013-08-12'})
	date1=datetime.date.today()
	date2=date1+datetime.timedelta(days=+7)
	date1=str(date1)
	date2=str(date2)
	if rubr_id==2:
		params = urllib.urlencode({'key': 'YADGMVO5M5QJTZXXIDEIIDOYTRS5KLI5QHUQKB5DZ22ADROO', 'rubr_id':rubr_id})
	else:
		params = urllib.urlencode({'key': 'YADGMVO5M5QJTZXXIDEIIDOYTRS5KLI5QHUQKB5DZ22ADROO', 'rubr_id':rubr_id, 'date_start':date1, 'date_start': date2})
	headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
	conn = httplib.HTTPConnection("www.jam.kz")
	conn.request("POST", "/api/foursquare/event_all", params, headers)
	response = conn.getresponse()
	data = response.read()
	conn.close()
	return json.loads(data)