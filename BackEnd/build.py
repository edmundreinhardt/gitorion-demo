#!/QOpenSys/usr/bin/python3
import os
from itoolkit import *
from itoolkit.lib.ilibcall import *

# Utility function
def check(step, itool):
  results = itool.dict_out(step)
  if 'success' in results:
    print (results['success'])
  else:
    print (results['error'])
    exit()

# Arguments
if len(sys.argv) > 1:
  tgtpgm = sys.argv[1];
else:
  tgtpgm = 'product'
if len(sys.argv) > 2:
  tgtlib = sys.argv[2];
else:
  tgtlib = 'oriondemo'

itransport = iLibCall()
itool = iToolKit()
itool.add(iCmd('chglibl', 'CHGLIBL LIBL('+tgtlib+') CURLIB('+tgtlib+')',{'error':'on'}))
itool.add(iCmd('crtsrcpf','CRTSRCPF QTEMP/BLDIFS RCDLEN(200)',{'error':'on'}))
cwd = os.path.abspath(os.path.dirname(__file__))
print (cwd)
itool.add(iCmd('cpystmf', 'CPYFRMSTMF FROMSTMF(\''+cwd+'/'+tgtpgm+'.rpgle\') TOMBR(\'/QSYS.LIB/QTEMP.LIB/BLDIFS.FILE/'+tgtpgm+'.mbr\') MBROPT(*REPLACE)',{'error':'on'}))
itool.add(iCmd('crtrpg',  'CRTBNDRPG '+tgtpgm+' SRCFILE(qtemp/bldifs) DBGVIEW(*SOURCE) OUTPUT(*PRINT) REPLACE(*YES)',{'error':'on'}))
# xmlservice
itool.call(itransport)

# check for success
check('chglibl', itool)
check('crtsrcpf', itool)
check('cpystmf', itool)
check('crtrpg', itool)

	