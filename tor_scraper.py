#!/usr/bin/env python
import socks
import socket
import requests
import argparse
from bs4 import BeautifulSoup
from urllib.request import urlopen
from colorama import Fore
from colorama import Style


### Setting up arguments and help
info = 'This program is designed to help pull link references from .onion sites.'
parser = argparse.ArgumentParser(description=info)
parser.add_argument('-u', '--url', metavar='', type=str, required=True, help='Place a .onion url here.')
group = parser.add_mutually_exclusive_group()
group.add_argument('-v', '--verbose', action='store_true', help='Print Verbose')
args = parser.parse_args()

### Main script for parsing site.
def tor_scrape(url_arg):
	link_1 = 1
	link_2 = 1
	try:
		#print(url_arg)

		### Configuring Socks to use Tor
		socks.set_default_proxy(socks.SOCKS5, 'localhost', 9150)
		socket.socket = socks.socksocket

		### Use Tor for DNS resolution
		def getaddrinfo(*args):
			return [(socket.AF_INET, socket.SOCK_STREAM, 6, '', (args[0], args[1]))]

		socket.getaddrinfo = getaddrinfo

		### Usings requests to read website

		### Test site Hidden Wiki
		#url_arg = 'http://s4k4ceiapwwgcm3mkb6e4diqecpo7kvdnfr5gg7sph7jjppqkvwwqtyd.onion/'
		res = requests.get(url_arg)
		### PRint the status code of the requested site
		print("Site status: " + str(res.status_code))

		### Using BeutifulSoup to get website content in nice format
		soup = BeautifulSoup(res.content, 'html.parser')

		#print(soup.prettify())

		soup.title

		### Grabbing all the links from the html

		links = [link.get('href') for link in soup.find_all('a')]
		links = list(filter(None, links))

		### Saving all onion links into a list.

		onion = []

		for l in links:
			if 'onion' in l:
				onion.append(l)

		for o in onion:
			print(str(link_1) + ' | ' + o)
			link_1 += 1

		if len(onion) > 0:
			choice = input('\nWould you like to test these addresses for connectivity? (y) or (n)\n')
			if choice.lower() == 'y':
				for o in onion:
					try:
						res = requests.head(o)
						if res.status_code == 200:
							print(str(link_2) + ' | ' + f'{Fore.GREEN}' + str(res.status_code) + f'{Style.RESET_ALL} | ' + str(o))
							link_2 += 1
							continue
						else:
							print(str(link_2) + ' | ' + f'{Fore.RED}' + str(res.status_code) + f'{Style.RESET_ALL} | ' + str(o))
							link_2 += 1
							continue
					except requests.ConnectionError:
						print(f'{Fore.RED}Failed to connect{Style.RESET_ALL} | ' + str(o))
						continue

	except:
		print(str(link_2) + ' | ' + f'{Fore.RED}Failed to connect{Style.RESET_ALL}')
		link_2 += 1



if __name__== '__main__':
	results = tor_scrape(args.url)
	if args.verbose:
		print('Here are the links: \n')
		results
	else:
		results

