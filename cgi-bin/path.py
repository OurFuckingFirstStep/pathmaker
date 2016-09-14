#!/usr/bin/env python3

from pathMap import PathMap, NoPath, UnknownVertex
import cgi
import cgitb

DEBUG = 1
PATH_TO_SVG = r'/var/www/html/'
#PATH_TO_SVG = ''
BASE_SVG_NAME = r'drawing.svg'
RESULT_SVG_PREFIX = r'drawing_path_'

if DEBUG == 1:
    cgitb.enable()

class BadInputFormat(Exception):
    pass

def get_points():
    form = cgi.FieldStorage()
    
    if 'from' not in form or 'to' not in form:
        raise BadInputFormat
#        A, B = 1, 2
    else:
        A, B = form['from'].value, form['to'].value

    if not A.isdigit() or not B.isdigit():
#    if False:
        raise BadInputFormat

    return A, B

def print_headers():
#headers, essentiaal!
    print (r'Content-type: text/html')
    print ('\r\n\r\n')

def print_html():
    #HTML-code
    print ("<html><head>")
    print ("<title>PathMaker (beta)</title>")
    #print ("<meta http-equiv=\"refresh\" content=\"2\">")
    print ("</head>")
    print ("<body>")

    try:
        A, B = get_points()
        print ('From:', A, '<br>')
        print ('To:', B, '<br>')
    
        name = RESULT_SVG_PREFIX + str(A) + str(B) + '.svg'
        path = PathMap(PATH_TO_SVG + BASE_SVG_NAME)
        path.create_path(A, B, PATH_TO_SVG + name)

        print ('<img src=\"/', name, '\"><br>', sep='')
        print("</body></html>")

    except BadInputFormat:
        print (r'<p>Bad input format!</p>')
    except (NoPath, UnknownVertex):
        print (r"<p>Can't build path between points", A, 'and', B,"</p>")
    
def main():
    print_headers()
    print_html()

if __name__ == "__main__":
    main()
