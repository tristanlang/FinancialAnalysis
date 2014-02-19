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

    '''
    GRAHAM RULES
    1.  An earnings-to-price yield of twice the triple-A bond yield. The earnings yield is the reciprocal of the price earnings ratio.
    2.  A price/earnings ratio down to four-tenths of the highest average P/E ratio the stock reached in the most recent five years. (Average P/E ratio is the average stock price for a year divided by the earnings for that year.)
    3.  A dividend yield of two-thirds of the triple-A bond yield.
    4.  A stock price down to two-thirds of tangible book value per share.
    5.  A stock price down to two-thirds of net current asset value — current assets less total debt.
    6.  Total debt less than tangible book value.
    7.  Current ratio (current assets divided by current liabilities) of two or more.
    8.  Total debt equal or less than twice the net quick liquidation value as defined in No. 5.
    9.  Earnings growth over the most recent ten years of seven percent compounded—a doubling of earnings in a ten-year period.
    10. Stability of growth in earnings—defined as no more than two declines of five percent or more in year-end earnings over the most recent ten years.
    '''