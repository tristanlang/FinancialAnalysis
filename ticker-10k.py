from xml.dom import minidom
import urllib.request
import zipfile
from io import BytesIO
import requests

# from the SEC RSS XML, get the zip files associated with the most recent filings
contents = urllib.request.urlopen('https://www.sec.gov/Archives/edgar/usgaap.rss.xml').read()
d = minidom.parseString(contents)
filings = d.getElementsByTagName('item')

for filing in filings:
    period = filing.getElementsByTagName('edgar:period')[0].firstChild.nodeValue
    zipurl = filing.getElementsByTagName('enclosure').item(0).getAttribute('url')
    zipcontents = requests.get(zipurl)
    z = zipfile.ZipFile(BytesIO(zipcontents.content))
    
    # need to extract ticker(?)(...i believe tik was one of the tickers i looked at)...from filing, and replace tik
    f = z.open('tik-' + period + '.xml')
    secfiling = f.read() # string containing the full xbrl/xml of the filing
    f.close()

    # next step is to use this minidom to process the XBRL files that have been obtained from the SEC RSS XML
    d = minidom.parseString(secfiling)