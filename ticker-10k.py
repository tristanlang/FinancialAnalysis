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

    '''
    XBRL structure appears to be in the following format:
    <xbrl>
        <comment node />
        <data node>
            <SEC filing data type 1>value</SEC filing data type 1>
            <SEC filing data type 2>value</SEC filing data type 2>
            <SEC filing data type 3>value</SEC filing data type 3>
            ...
            ...
            <SEC filing data type N>value</SEC filing data type N>
        </data node>
    </xbrl>


    The node values can generally be accessed in the following manner:

        for node in [x for x in d.childNodes[1].childNodes if not x.nodeValue]:
            node.firstChild.nodeValue
    
    Where d is at the <xbrl> level, above.
    
    Some of the nodeValues are Text/HTML, which are used for explanations. These nodes
    generally have <<node.tagName>> values that contain words like "TextBlock", "Policy",
    "Use", or "Text", and they are typically over 100 characters in length.

    Some of the nodes do not have <<node.firstChild>> values because they do not wrap any
    numerical or text values and instead are one line XML tags. Thus far it seems that there
    are not many of these tags and they can be safely ignored, although one tag does seem to
    be a reference/link to a schema (.xsd) used by filing company, possibly for their internal
    schema definitions.
    '''

    nodes = [x for x in d.childNodes[1].childNodes if not x.nodeValue]
