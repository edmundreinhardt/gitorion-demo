#!/QOpenSys/usr/bin/python3
from bottle import request, route, run
from showTable import show_table
 
port_number=80
host_location='embox1.demos.ibm.com' 
 
@route('/')
def sample():
    return show_table() 
 

run(host=host_location, port=port_number, debug=True) 