import json
import  httplib
import MySQLdb

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

def getDataForCategory(cat_str,location):
	global output
	ll="near="+location
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
	conn.close()
	output=[]
	for venue in venues:
		place_name=getPlaces(cat_str,venue)
		output.append(place_name)
	return output

def getPlaces(category,json_dictionary):
	place_dictionary={}
	place_dictionary['name']=json_dictionary['name']
	place_dictionary['id']=json_dictionary['id']
	location=json_dictionary['location']
	place_dictionary['latitude']=location['lat']
	place_dictionary['longitude']=location['lng']
	if 'address' in location:
		place_dictionary['address']=location['address']
	place_dictionary['here_now']=json_dictionary['hereNow']['count']
	place_dictionary['category_string']=json_dictionary['categories'][0]['shortName']
	place_dictionary['category']=category
	extra_place=getExtraInfo(place_dictionary['id'])
	if 'rating' in extra_place:
		place_dictionary['rating']=extra_place['rating']
	else:
		place_dictionary['rating']=6;
	photo_groups=extra_place['photos']['groups']
	for group in photo_groups:
		for item in group['items']:
			image_url=0
			sizes=item['sizes']
			if sizes['count']>1:
				image_url=sizes['items'][1]['url']
			else:
				image_url=sizes['items'][0]['url']
			place_dictionary['image_url']=image_url	

	return place_dictionary


def getExtraInfo(place_id):
	db = MySQLdb.connect(host="localhost", user="root", passwd="athena", db="testdb", charset='utf8')
	cursor = db.cursor()
	sql = "select place_json from places where place_id='"+str(place_id)+"' limit 1"
	cursor.execute(sql)
	data =  cursor.fetchall()
	data1=""
	for row in data:
		data1=row[0]
		data1=data1.decode('unicode-escape').encode('utf8')
	if data1=="":
		client_string="client_id=ATCDKP1BI3F1YDPOHVOWI2UCEXIUFWGPR0GF3DOVSLJFRFBM&client_secret=YADGMVO5M5QJTZXXIDEIIDOYTRS5KLI5QHUQKB5DZ22ADROO"
		conn = httplib.HTTPSConnection("api.foursquare.com")
		url="/v2/venues/"+place_id+"?"+client_string;
		conn.request("GET", url)
		r1 = conn.getresponse()
		data1 = r1.read()
		cursor.execute("INSERT INTO places (place_id,place_json) values (%s,%s)",(place_id,data1.decode('utf8').encode('unicode-escape')))
		db.commit()
		conn.close()
#		cursor.execute("insert into places (place_id,place_json) values ('"+place_id+"','"+data1.decode('utf8').encode('unicode-escape')+"');")
		#print data1.encode('unicode-escape')
	decoded=json.loads(data1)
	return decoded['response']['venue']	
