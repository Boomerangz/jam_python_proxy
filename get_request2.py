<%import  httplib 
import time
import threading
import json
import codecs

basic_address="/v2/venues/search"
ll="near=Almaty"
category="categoryId=4bf58dd8d48988d17f941735"
version_string="v=20120522"
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
TYPES_ARRAY = [FSQ_TYPE_CINEMA];

dt_begin=time.time();

output=[]

def getDataForCategory(cat_str):
	global output
	conn = httplib.HTTPSConnection("api.foursquare.com")
	url=basic_address+"?"+ll;
	if (cat_str!=FSQ_UNDEFINED):
		url+="&categoryId="+cat_str
	url+="&"+version_string+"&"+client_string	
	conn.request("GET", url)
	r1 = conn.getresponse()
	data1 = r1.read()
	decoded=json.loads(data1)
	response=decoded['response']
	venues=response['venues']
	for place in venues:
		place_name=place['name']
		output.append(place_name)
	conn.close()

category_range=[FSQ_TYPE_CINEMA,FSQ_TYPE_THEATER,FSQ_TYPE_CLUB,FSQ_TYPE_MARKET,FSQ_UNDEFINED];
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
output= json.dumps(output)
%>
<%=output%>