import json
import  httplib

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
			place_dictionary['photo']=image_url	

	return place_dictionary


def getExtraInfo(place_id):
	client_string="client_id=ATCDKP1BI3F1YDPOHVOWI2UCEXIUFWGPR0GF3DOVSLJFRFBM&client_secret=YADGMVO5M5QJTZXXIDEIIDOYTRS5KLI5QHUQKB5DZ22ADROO"
	conn = httplib.HTTPSConnection("api.foursquare.com")
	url="/v2/venues/"+place_id+"?"+client_string;
	conn.request("GET", url)
	r1 = conn.getresponse()
	data1 = r1.read()
	decoded=json.loads(data1)
	conn.close()
	return decoded['response']['venue']