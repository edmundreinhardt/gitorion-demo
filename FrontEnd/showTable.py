#!/QOpenSys/usr/bin/python3
import sys
import cgi
import os
from itoolkit import *
from itoolkit.rest.irestcall import *

def show_table():
  # ---------------------
  # remote call to yips
  # ----------------------
  itransport = iRestCall("http://65.183.160.36/cgi-bin/xmlcgi.pgm","*NONE","*NONE")
  
  # ---------------------
  # normal fastcgi processing
  # ----------------------
  myCat = '1'
  #myMax = form['myMax'][0]
  myMax = '20'
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
  html_result = ""
  
  if 'success' in product:
    html_result = ( "<style>table, th, td {border: 1px solid black;border-collapse: collapse;}"
       "th, td {padding: 5px;text-align: left;width: 200px;}tr:nth-child(even) {background-color: #f3f3f3;}"
       "tr:nth-child(odd) {background-color:#fff;}th {background-color: #008ABF;color: white}</style>")
    html_result += ('<table border="1">\n'
                    "<th>title</th>\n"
                    "<th>price</th>\n"
                    "<th>photo</th>\n")
    prods = product['findMe']
    if 'title' in prods:
      tmp = prods
      prods = [tmp]
    for r in prods:
      if 'title' in r:
        html_result += "<tr>"
        html_result += "<td>" + r['title'] + "</td>"
        html_result += "<td>" + r['price'] + "</td>"
        html_result += "<td><img src='http://65.183.160.36/hats/master/" + r['photo'] + "'/></td>"
        html_result += "</tr>\n"
      else:
        html_result += "<tr><td colspan='3'>" + str(r) + "</td></tr>\n"
    html_result += '</table>\n'
  else:
    html_result += product['error']
    html_result += str(product)
  return html_result

# ---------------------
# command line testing only (optional)
# ---------------------
print (show_table())