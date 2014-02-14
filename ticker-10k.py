from xml.dom import minidom
import urllib.request
import zipfile
from io import StringIO
import codecs

contents = urllib.request.urlopen('https://www.sec.gov/Archives/edgar/usgaap.rss.xml').read()
d = minidom.parseString(contents)
filings = d.getElementsByTagName('item')

for filing in filings:
    period = filing.getElementsByTagName('edgar:period')[0].firstChild.nodeValue
    zipurl = filing.getElementsByTagName('enclosure').item(0).getAttribute('url')
    zipcontents = urllib.request.urlopen(zipurl)
    z = zipfile.ZipFile(StringIO(zipcontents.read().decode('zip')))#codecs.iterdecode(zipcontents, 'utf-8')))#
    
    f = z.open('tik-' + period + '.xml')
    secfiling = f.read()
    f.close()

