# Link Check goes through a URL, requests every link on the page, and prints
#	out the requested links and their respective status codes. It can also
#	write the results to a text or log file.
# By Jeff Chheng

from BeautifulSoup import BeautifulSoup
import urllib2
import argparse

def parse_args():
    """
    takes the arguments from the script call and calls the proper
    main method based on those arguments
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--link",
        help="Check the links on the specified web page",
        nargs=1,
        required=True)

    parser.add_argument("--log",
        help="Log results to a file",
        nargs=1,
        default=False)

    parser.add_argument("--is_sitemap",
        help="If true, the url passed will be treated as a sitemap to be crawled",
        nargs=1,
        default=False)

    parser.add_argument("--site_root",
        help="When crawling a sitemap for links to check, this helps to weed out off-site links",
        nargs=1,
        default=None)

    args = parser.parse_args()
    if args.is_sitemap:
        sitemap_method(args)
    else:
        main_method(args)

def main_method(args):
    """
    standard method that gets all links on a page and checks them
    """
    links = get_links(args.link[0])

    if links:
        if args.log:
            check_links(links, args.log[0])
        else:
            check_links(links, args.log)
    else:
        print "Your specified URL doesn't have any links to check."

def sitemap_method(args):
    """
    visits all links on the sitemap page and tests all links on those pages
    """
    this_url = args.link[0]
    links = get_links(this_url)
    full_results = {}

    if args.site_root:
        site_root = args.site_root[0]
    else:
        site_root = ""

    for link in links:
        if site_root in link:
            links_to_check = get_links(link)
            if args.log:
                full_results = check_links(links_to_check, args.log[0])
            else:
                full_results[link] = check_links(links_to_check, args.log)

    for key in full_results:
        print "%s: %d errors" % (key, len(full_results[key]))
        for bad_link in full_results[key]:
            print bad_link


def get_links(url):
    """
    takes a url and returns all links on that page
    """
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
        try:
            href = link["href"]
        except KeyError:
            print "horrible failure " + str(link)
            href = None

        if href:
            # disregard mailto links and http://# because ???
            if "mailto:" not in href and "http://#" not in href:
                # add http to links or else urllib2 will complain
                if href.startswith("//"):
                    href = "http:" + href

                # href is complete link
                if "http://" in href or "https://" in href:
                    links.append(href)
                # href is a relative link
                else:
                    links.append("/".join([url, href]))

    return links
	
def check_links(links, log):
    """
    Check a list of links and print results of requests to stdout.
    Optionally, write results to a file.
    """
    links_checked = 0
    errors_found = 0
    bad_links = []
    
    if log:
        f = open(log, "w")
    else:
        f = None

    if not links:
        return 'no links to check'

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
                bad_links.append(status + ": " + link)
                print status + '\n'
			
            if f:
                f.write(requesting + '\n')
                f.write(status + '\n\n')
			
        except (urllib2.HTTPError, urllib2.URLError), e:
            # increment errors found
            errors_found += 1
            print "%s\n" % e
            bad_links.append("%s: %s" % (unicode(e), unicode(link)))
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

    return bad_links

if __name__ == '__main__':
	parse_args()
