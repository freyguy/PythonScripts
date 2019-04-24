### Import required modules

import dns.resolver
import sys

### Sets domain resolvers to one internal NS and Google's public NS

myresolver = dns.resolver.Resolver()
localDNSserver = raw_input("What is the IP of the local DNS server: ")
myresolver.nameservers = [localDNSserver, '8.8.8.8']

### Provide domain to search on

domain = raw_input("Please provide FQDN of site to resolve information for: ")

### For a given domain, "query_list", retrieve A record, MX records, & name server
###	records from either an internal NS or Google's public DNS server

### Returns A record for given domain
def a_resolution(domain):
	print '\n' + '-'*8 + 'A RECORD'+'-'*8
	for x in myresolver.query(domain, 'A'):
		try:
			host = str(x.address)
			print domain + ' : ' + host
		except dns.resolver.NXDOMAIN:
			print "No A record available"

### Returns MX record for given domain
def mx_resolution(domain):
	try:
		print '\n' + '-'*8 + 'MX RECORD'+'-'*8
		for x in myresolver.query(domain, 'MX'):
			host = str(x.exchange)
			# print "MX record: " + str(x.exchange)
			for y in myresolver.query(host, 'A'):
				print host + ' : ' + str(y.address)
	except dns.resolver.NoAnswer:
		print'-'*8 + 'MX RECORD'+'-'*8
		print "No MX record available"


### Returns name server records for given domain
def ns_resolution(domain):
	try:
		print '\n' + '-'*8 + 'NS RECORD'+'-'*8
		for x in myresolver.query(domain, 'NS'):
			host = str(x.target)
			for y in myresolver.query(host, 'A'):
				print host + ' : ' + str(y.address)
	except dns.resolver.NoAnswer:
		print'-'*8 + 'NS RECORD'+'-'*8
		print "No NS record available"

a_resolution(domain)
mx_resolution(domain)
ns_resolution(domain)



