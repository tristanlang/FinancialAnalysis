import urllib
import urllib2
import re
import sys

cik = sys.argv[1]

print "Searching for symbol that matches %s" % cik

yahoo_url = 'http://finance.yahoo.com/lookup?s='
edgar_url = 'http://www.sec.gov/cgi-bin/browse-edgar?CIK=%s&action=getcompany' % cik
string_match = 'companyName'

# Fetch company page from edgar using the CIK
response = urllib2.urlopen(edgar_url)
for line in response:
    if string_match in line:
        name_match = re.search('<span class="companyName">(.*)<acronym', line)
        company_name = name_match.group(1)
        print "Found company name %s from SEC" % company_name

# Here we do some fuzzy logic. If the company name has more than 
# three words then only use the first two unless the second word
# is 2 chars or less.
if len(company_name.split()) >= 2:
    company_name_words = company_name.split()
    if len(company_name_words[1]) <= 2:
        company_name = '%s %s %s' % (company_name_words[0],
                                     company_name_words[1],
                                     company_name_words[2])
    else:
        company_name = '%s %s' % (company_name_words[0], company_name_words[1])

print "Attempting to search yahoo finance for %s" % company_name


# URL encode the company name
company_name = urllib.quote(company_name)

#Take the company name to yahoo and get the ticker
yahoo_url = 'http://finance.yahoo.com/lookup?s=%s' % company_name
print "Yahoo search URL is %s" % yahoo_url
response = urllib2.urlopen(yahoo_url)
# Interate throught the HTML and print the first ticker. If there
# are more than one we only get the first.
for line in response:
    # the existence of "ticker_up" or "ticker_down" tells we are 
    # on the line with the first symbol
    if "ticker_up" in line or "ticker_down" in line:
        ticker_link = re.search('<td>(.*?)</td>', line).group(1)
        ticker = re.search('">(.*?)</a>', ticker_link).group(1)
        print ticker
        break