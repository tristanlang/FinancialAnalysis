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
    z = zipfile.ZipFile(BytesIO(requests.get(zipurl).content))

    f = z.open(list(filter(lambda x: ('-%s.xml' % period) in x, z.namelist()))[0])
    secfiling = f.read() # string containing the full xbrl/xml of the filing
    f.close()

    # next step is to use this minidom to process the XBRL files that have been obtained from the SEC RSS XML
    d = minidom.parseString(secfiling)