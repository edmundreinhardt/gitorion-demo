#!/QOpenSys/usr/bin/python3
from bottle import request, route, run
from showTable import show_table
#from itoolkit import *
#from itoolkit.lib.ilibcall import *     #for local jobs
 
 
port_number=80
host_location='embox1.demos.ibm.com'
username = 'PYDEMO'
password = 'pydemo'
 
 
@route('/')
def sample():
    return show_table() 
 

run(host=host_location, port=port_number, debug=True) 