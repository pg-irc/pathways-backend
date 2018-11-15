#!/usr/bin/python2

import xml.etree.ElementTree as etree

CONTENT = etree.iterparse(
    '../../bc211/2018-09-24/iCarolExport-BC211-AIRSXML-20180924_210244.xml',
    events=(
        'end',
    )
)
for event, elem in CONTENT:
    if elem.tag == 'Agency':
        title = elem.find('Key').text
        if title:
            filename = 'Agency-{}.xml'.format(title)
            with open(filename, 'w') as f:
                f.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n")
                f.write('<Source>')
                f.write(etree.tostring(elem))
                f.write('</Source>')
