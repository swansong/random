# Link Check goes through a URL, requests every link on the page, and prints
#	out the requested links and their respective status codes. It also saves
#	the statuses to requests.txt for further perusal.
# By Jeff Chheng

from BeautifulSoup import BeautifulSoup
import urllib2
import argparse

#-------------------------------------------------------------------------------
# parse_args
#	Parse command-line arguments and calls other methods with appropriate
#	parameters.
def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument("--link",
		help="Check the links on the specified web page",
		nargs=1,
		required=True)
	
	parser.add_argument("--log",
		help="Log results to a file",
		nargs=1,
		default=False)
	
	args = parser.parse_args()
	links = get_links(args.link[0])
	if links:
		if args.log:
			check_links(links, args.log[0])
		else:
			check_links(links, args.log)
	else:
		print "Your specified URL doesn't have any links to check."

#-------------------------------------------------------------------------------
# get_links
#	Get links from a specified url.
#	Parameters:
#		-- url: a url to retrieve links from
#	Return a list of the links.
def get_links(url):
	# remove trailing slashes
	while url.endswith("/"):
		url = url[:-1]
		
	try:
		# get/store info from page
		page = urllib2.urlopen(url)
	except urllib2.URLError, e:
		print e
		return None
	
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
	
	return links
	

#-------------------------------------------------------------------------------
# check_links
#	Check a list of links and print results of requests to stdout. Optionally,
#	write results to a file.
#	Parameters:
#		-- links: a list of links
#		-- log: a file to write the logs to
def check_links(links, log):
	if log:
		file = open(log, "w")
	else:
		file = None

	# request each link
	for link in links:
		requesting = "Requesting %s" % link
		print requesting
		
		try:
			request = urllib2.urlopen(link)
			code = request.getcode()

			# check HTTP status code
			if code == 200:
				status = "200 OK\n"
			else:
				status = "%s ERROR\n" % code
			
			print status
			
			if file:
				file.write("%s\n" % requesting)
				file.write("%s\n" % status)
			
		except urllib2.HTTPError, e:
			error = "%s\n" % e
			print error
			if file:
				file.write("%s\n" % requesting)
				file.write("%s\n" % error)

if __name__ == '__main__':
	parse_args()
