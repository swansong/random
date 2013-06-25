# Link Check goes through a URL, requests every link on the page, and prints
# 	out the requested links and their respective status codes. It also saves
#	the statuses to requests.txt for further perusal.
# By Jeff Chheng

from BeautifulSoup import BeautifulSoup
import urllib2
import re

# page to get info, replace with whatever (no trailing slash)
url = "http://escience.washington.edu"

# get/store info from page
page = urllib2.urlopen(url)
soup = BeautifulSoup(page.read())
a = soup.findAll("a")
links = []

# format links
for link in a:
	href = link["href"]
	if "http://" in href or "https://" in href:
		links.append(href)
	else:
		if href.startswith("/"):
			links.append("".join([url, href]))
		else:
			links.append("/".join([url, href]))

f = open("requests.txt", "w")

# request links and write statuses to file
for link in links:
	requesting = "Requesting %s" % link
	
	print requesting
	f.write("%s\n" % requesting)
	
	try:
		request = urllib2.urlopen(link)
		code = request.getcode()

		if code == 200:
			status = "200 OK\n"
		else:
			status = "%s ERROR\n" % code
		
		print status
		f.write("%s\n" % status)
		
	except urllib2.HTTPError, e:
		error = "%s\n" % e
		print error
		f.write("%s\n" % error)
		
