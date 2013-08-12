import json
import  httplib


def getOptionalInfo(place_id):
	client_string="client_id=ATCDKP1BI3F1YDPOHVOWI2UCEXIUFWGPR0GF3DOVSLJFRFBM&client_secret=YADGMVO5M5QJTZXXIDEIIDOYTRS5KLI5QHUQKB5DZ22ADROO"
	conn = httplib.HTTPSConnection("api.foursquare.com")
	url="/v2/venues/"+place_id+"?"+client_string;
	conn.request("GET", url)
	r1 = conn.getresponse()
	data1 = r1.read()
	place={}
	json_place=json.loads(data1)
	return {'tips':getTips(json_place),'photos':getPhotos(place_id)}





def getTips(json_place):
	json_tip_groups_list=json_place['response']['venue']['tips']['groups']
	tip_list=[]
	for json_tip_group in json_tip_groups_list:
		json_tips_list=json_tip_group['items']
		for json_tip in json_tips_list:
			tip_text=json_tip['text']
			create_date=json_tip['createdAt']
			author=json_tip['user']['firstName']+json_tip['user']['lastName']
			tip={'author':author,'date':create_date,'text':tip_text}
			tip_list.append(tip)
	return tip_list


def getPhotos(place_id):
	client_string="client_id=ATCDKP1BI3F1YDPOHVOWI2UCEXIUFWGPR0GF3DOVSLJFRFBM&client_secret=YADGMVO5M5QJTZXXIDEIIDOYTRS5KLI5QHUQKB5DZ22ADROO"
	conn = httplib.HTTPSConnection("api.foursquare.com")
	url="/v2/venues/"+place_id+"/photos"+"?"+client_string;
	conn.request("GET", url)
	r1 = conn.getresponse()
	data1 = r1.read()
	json_photos_list=json.loads(data1)
	print json.dumps(json_photos_list['response']['photos'])
	json_photos__groups_list=json_photos_list['response']['photos']['groups']
	photos_list=[]
	for json_photos_list in json_photos__groups_list:
		photos_list=[]
		json_photos_list=json_photos_list['items']
		for json_photo in json_photos_list:
			little_url=json_photo['sizes']['items'][1]['url']
			big_url=json_photo['sizes']['items'][0]['url']
			photos_list.append({'big_url':big_url,'little_url':little_url})
