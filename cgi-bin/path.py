#!/usr/bin/env python3

from pathMap import PathMap
import cgi
import cgitb

DEBUG = 1
PATH_TO_SVG = r'/var/www/html/'
#PATH_TO_SVG = ''
BASE_SVG_NAME = r'drawing.svg'
RESULT_SVG_PREFIX = r'drawing_path_'

if DEBUG == 1:
    cgitb.enable()


#headers, essentiaal!
print (r'Content-type: text/html')
print ('\r\n\r\n')

#HTML-code
print ("<html><head>")
print ("<title>PathMaker (beta)</title>")
#print ("<meta http-equiv=\"refresh\" content=\"2\">")
print ("</head>")


print ("<body>")

form = cgi.FieldStorage()

if 'from' in form and 'to' in form:
    A, B = form['from'].value, form['to'].value
else:
    A, B = 3, 6
print ('From:', A, '<br>')
print ('To:', B, '<br>')
    
#    if A.isdigit() and B.isdigit():
if True:
    name = RESULT_SVG_PREFIX + str(A) + str(B) + '.svg'
    print ('<img src=\"/', name, '\"><br>', sep='')
    path = PathMap(PATH_TO_SVG + BASE_SVG_NAME)
    path.create_path(A, B, PATH_TO_SVG + name)
        
#else:
#    print ('Bad input<br>')

print("</body></html>")
