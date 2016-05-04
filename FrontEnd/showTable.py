import sys
import cgi
import os
from itoolkit import *
from itoolkit.rest.irestcall import *
# ---------------------
# command line testing only (optional)
# ---------------------
if not 'environ' in locals():
  environ = dict()
  environ['REQUEST_METHOD'] = 'GET'
  if len(sys.argv) > 2:
    environ['QUERY_STRING'] = '&'.join(sys.argv)
  else:
    print("ERROR: Command line test missing arguments.")
    print("Example: python3 xmlhats.py myCat=1 myMax=20")
    exit()
else:
  pathname, junk = os.path.split(environ['SCRIPT_NAME'])
  student = pathname.replace("/","")
  print("<h3>Student: " + student + "</h3>")
 
# ---------------------
# remote call to yips
# ----------------------
itransport = iRestCall("http://65.183.160.36/cgi-bin/xmlcgi.pgm","*NONE","*NONE")

# ---------------------
# normal fastcgi processing
# ----------------------
if environ['REQUEST_METHOD'] == 'POST':
  environ['QUERY_STRING'] = environ['wsgi.input'].readline().decode()
form = cgi.parse_qs(environ['QUERY_STRING'])
myCat = form['myCat'][0]
myMax = form['myMax'][0]
myCount = '0'
findMe = ''

#     D ARRAYMAX        c                   const(999)
#     D prod_t          ds                  qualified based(Template)
#     D  prod                         10i 0
#     D  cat                          10i 0
#     D  title                        64a   varying(4)
#     D  photo                        64a   varying(4)
#     D  price                        12p 2
#      *+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#      * main(): Control flow
#      *+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
#     D Main            PI 
#     D  myCat                        10i 0
#     D  myMax                        10i 0
#     D  myCount                      10i 0
#     D  findMe                             likeds(prod_t) dim(ARRAYMAX)
itool = iToolKit()
itool.add(iCmd('chglibl', 'CHGLIBL LIBL(HATS) CURLIB(HATS)'))
itool.add(
 iPgm('product','PRODUCT')
 .addParm(iData('myCat','10i0',myCat))
 .addParm(iData('myMax','10i0',myMax))
 .addParm(iData('myCount','10i0',myCount,{'enddo':'myCount'}))
 .addParm(
  iDS('findMe',{'dim':'999','dou':'myCount'})
  .addData(iData('prod','10i0',''))
  .addData(iData('cat','10i0',''))
  .addData(iData('title','64a','',{'varying':'4'}))
  .addData(iData('photo','64a','',{'varying':'4'}))
  .addData(iData('price','12p2',''))
  )
 )

# xmlservice
itool.call(itransport)

# output
chglibl = itool.dict_out('chglibl')
if not 'success' in chglibl:
  print (chglibl['error'])
  exit()

product = itool.dict_out('product')
if 'success' in product:
  print('<table border="1">')
  print("<th>title</th>")
  print("<th>price</th>")
  print("<th>photo</th>")
  prods = product['findMe']
  if 'title' in prods:
    tmp = prods
    prods = [tmp]
  for r in prods:
    if 'title' in r:
      print("<tr>")
      print("<td>" + r['title'] + "</td>")
      print("<td>" + r['price'] + "</td>")
      print("<td><img src='http://65.183.160.36/hats/master/" + r['photo'] + "'/></td>")
      print("</tr>")
    else:
      print("<tr><td colspan='3'>" + str(r) + "</td></tr>")
  print('</table>')
else:
  print (product['error'])
  print (str(product))
