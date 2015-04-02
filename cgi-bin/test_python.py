#!/usr/bin/env python

import sys
from datetime import datetime
print 'Content-type: text/html\n'
print '\n\n'
print '<HTML><HEAD><TITLE>Python Test File</TITLE></HEAD>'
print '<BODY><H1>Python test script</H1>'
print 'Python Version information:'
print 'Version info:', sys.version_info
print '<p>'
print 'The current date and time are:'
print datetime.now().strftime('%Y-%m-%d %H:%M:%S')
print '<p>'

print '</BODY></HTML>'
