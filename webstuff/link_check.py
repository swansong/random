# Link Check goes through a URL, requests every link on the page, and prints
#	out the requested links and their respective status codes. It can also
#	write the results to a text or log file.
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
#	-- url: a url to retrieve links from
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
		# href is complete link
		if "www." in href or "http://" in href or "https://" in href:
			links.append(href)
		# href is a relative link
		else:
			if href.startswith("/"):
				links.append("".join([url, href]))
			else:
				links.append("/".join([url, href]))
	
	return links
	
#-------------------------------------------------------------------------------
# check_links
#	Check a list of links and print results of requests to stdout.
#	Optionally, write results to a file.
#	Parameters:
#	-- links: a list of links
#	-- log: a file to write the logs to
def check_links(links, log):
	links_checked = 0
	errors_found = 0
	
	if log:
		f = open(log, "w")
	else:
		f = None

	# request each link
	for link in links:
		# increment links checked
		links_checked += 1
	
		requesting = "Requesting " + link
		print requesting
		
		try:
			request = urllib2.urlopen(link)
			code = request.getcode()

			# 2xx is considered a successful request
			if code >= 200 and code <= 299:
				status = "%d OK" % code
			else:
				# increment errors found
				errors_found += 1
				
				status = "%d ERROR" % code
			
			print status
			print
			
			if f:
				f.write(requesting + '\n')
				f.write(status + '\n\n')
			
		except urllib2.HTTPError, e:
			# increment errors found
			errors_found += 1
			
			print e
			print
	
			if f:
				f.write(requesting + '\n')
				f.write("%s\n\n" % e)
	
	results = "Links checked: %4d" % links_checked
	errors = "Errors found:  %4d" % errors_found
	print results
	print errors
	
	if f:
		f.write(results + '\n')
		f.write(errors + '\n')

if __name__ == '__main__':
	parse_args()
