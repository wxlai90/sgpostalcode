#!/usr/bin/python

import requests, sys, threading

def check_end(html_content):
	end_keyword = 'Its zip code'
	if end_keyword not in html_content:
		return True

def parse_into_csv(content):	
	for i in content.split('"'):
		if 'Its zip code is' in i:
			address = i.split(' is located')[0]
			zip = i.split(' ')[-1].replace('.','')
			break
	
	with open('database', 'a+') as f:
		f.write(zip + ', ' + address + '\n')
	

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36'
}



def main(i):
	baseurl = 'https://sgp.postcodebase.com/node/'
	url = baseurl + str(i)
	print "Scraping:", url
	raw_input()
	r = requests.get(url, headers=headers, verify=False)
	content = r.content
	if check_end(content):
		print "Reached end of nodes"
		sys.exit(1)
	parse_into_csv(content)

i = 0
while 1:
	threads = []
	for n in range(5):
		i += 1
		t = threading.Thread(target = main, args=(i, ))
		threads.append(t)

	for jobs in threads:
		jobs.start()	

	for jobs in threads:
		jobs.join()	
