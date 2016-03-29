import urllib2
from bs4 import BeautifulSoup
import os
from multiprocessing import Pool

opener = urllib2.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0')]
champs=[]

class champions:
	def __init__(self, code):
		self.code = code
		self.name = code.span.text
		self.positions = code.findAll('a', {"style" : "display:block"})
		self.url = gather_urls(self.positions)

def find_champ():
	url = "http://champion.gg"
	ourUrl = opener.open(url).read()
	soup = BeautifulSoup(ourUrl)
	global patch
	patch = soup.findAll('strong')[0].text
	for i in soup.findAll('div', {"class" : "champ-index-img"}):
		champs.append(champions(i))

def gather_urls(urls):
	url = []
	for i in urls:
		url.append(i['href'])
	return url

def get_items(web):
	url = "http://champion.gg%s" % web
	template = '{"map": "any", "isGlobalForChampions": false, "blocks": [{"items": [%s], "type": "Most Frequent Starters"}, {"items": [%s], "type": "Highest Win Rate Starters"}, {"items": [%s], "type": "Most Frequent Build"}, {"items": [%s], "type": "Highest Win Rate Build"}, {"items":[{"count":1,"id":"3340"},{"count":1,"id":"3341"},{"count":1,"id":"3363"},{"count":1,"id":"3364"},{"count":1,"id":"2043"}],"type":"Trinkets and Wards"}], "associatedChampions": [], "title": "%s", "priority": false, "mode": "any", "isGlobalForMaps": true, "associatedMaps": [], "type": "custom", "sortrank": 1, "champion": "%s"}'
	name = web.split("/")[2]
	lane = web.split("/")[3]
	title = "%s %s" % (lane, patch)
	print "Starting %s %s" % (name, title)
	ourUrl = opener.open(url).read()
	soup = BeautifulSoup(ourUrl)
	items = []
	for list in soup.findAll('div', {"class" : "build-wrapper"}):
		build = []
		for item in list.findAll('img'):
			if item['src'].replace('.png', '')[-4:] == "2010":
				build.append('{"count": 1, "id": "2003"}')
			else:
				build.append('{"count": 1, "id": "%s"}' % item['src'].replace('.png', '')[-4:])
		items.append(build)
	final_build = template % (','.join(items[2]),','.join(items[3]),','.join(items[0]),','.join(items[1]), title, name)
	create_file(final_build, name, title)
	
def create_file(build, name, title):
	directory = "Champions/%s/Recommended" % (name)
	filename = '%s.json' % title.replace('.', '_').replace(' ', '_')
	if not os.path.exists(directory):
		os.makedirs(directory)
	with open(os.path.join(directory, filename), 'wb') as temp_file:
		temp_file.write(build)
	print "Finished %s %s" % (name, title)
		
def main():
	find_champ()
	urls = []
	for i in champs:
		for url in i.url:
			urls.append(url)
	my_pool = Pool(5)
	my_pool.map(get_items, urls)	
				
if  __name__ =='__main__':main()