#!/usr/bin/env python

import os
import sys
import argparse
import glob
import gmapfuncs as gm
import timefuncs as tm
import querygen as qg
import outputlocs as ol


def writeGufiScript( gufitmp, guficmd ):
    """
    Writes gufi script file in scriptdir
    """
    scrfile, scriptdir = ol.getProcFilename( gufitmp, 'script' )
    with open(scrfile, 'w') as fh:
       fh.write('%s\n\n' % '#!/bin/bash')
       fh.write('%s\n' % guficmd)
    fh.close()
    os.system('chmod +x ' + scrfile)
    return scrfile, scriptdir

def conCatReport( cfiles, gufitmp, inputfields ):
    repfile, repdir = ol.getProcFilename( gufitmp, 'report' )
    with open(repfile, 'w') as wfh:
       for fl in cfiles:
          with open(fl, encoding = "ISO-8859-1") as fh:
             l = 0
             for line in fh:
                tmp = line.split('\x1E')
                try:
                   size = int(tmp[0]); uid = int(tmp[1])
                   mtime = int(tmp[2]); atime = int(tmp[3]);
                   if len(tmp) > 7:
                      proj = gm.getPname( int(tmp[4]) ); 
                      fullname = '/'.join([gm.searchToFsName(tmp[6]),tmp[5]])
                   else:
                      proj = 'NULL'; 
                      fullname = '/'.join([gm.searchToFsName(tmp[5]),tmp[4]])
                   if atime < mtime:
                      atime = mtime
                   fdict = {'filename':fullname, 'size':str(size), 'owner':gm.getUname( uid ),
                            'project':proj, 'mtime':tm.tsToYMND( mtime ),
                            'atime':tm.tsToYMND( atime )}
                   vals = []
                   for ent in inputfields:
                      vals.append( fdict[ent])
                   valstr = ','.join(vals)
                   wfh.write("%s\n" % valstr)
                except:
                   print("Discarded line:",l,"from: ",fl,"line: ",tmp, file=sys.stderr)
                l += 1
     

def executeGufiScriptOnServer( scriptfile ):
    """ 
    Execute script from Casper to GUFI server
    """ 
    sshcmd = 'ssh -oHostBasedAuthentication=yes squall1.ucar.edu'
    fullcmd = ' '.join([sshcmd, scriptfile])
    os.system(fullcmd)
    
def checkListFields( listfields ):
    validfields = ['filename', 'size', 'owner', 'project', 'mtime', 'atime']
    for ent in listfields:
       if ent not in validfields:
           print("The field ",ent," not valid, the list of valid field is: ", validfields)
           exit(-1)
    return True

def parseCmdLine( ):
    """
    Mainly the argparser stuff dumped in a single function
    """
    import cmdline as cmdl
    gufitmp = os.path.join('/gpfs/fs1/scratch', os.environ['LOGNAME'], 'gufi_tmp')
    cmdl.gufitmp = gufitmp
    parser = cmdl.parserForGwrap( )
    args = parser.parse_args()
    gufitmp = args.gufitmp
    try:
       fields = args.listd[0].split(',')
       checkListFields( fields )
    except:
       fields = None
    cachedir = os.path.join(gufitmp, 'raw')
    uids = gm.getUlist( args.fuids, 'users' )
    pids = gm.getUlist( args.projs, 'projects' )
    wp = tm.procPeriod( args.writep )
    rp = tm.procPeriod( args.readp )
    nthreads = args.nthreads
    verbosity = args.verbosity
    gufitree = gm.fsnameToSearch( args.treename )
    if gufitree.startswith('/search/hpss'):
       wpname = 'ctime'
    else:
       wpname = 'mtime'
    inputdelim = ','
    if verbosity:
       print('Using cachedir: ',cachedir)
       print('users: ',uids)
       print('projects: ',pids)
       print('write-period: ',wp)
       print('read-period: ',rp)
       print('list mode:',lmode)
    return verbosity, uids, pids, wp, wpname, rp, fields, inputdelim, gufitmp, cachedir, nthreads, gufitree



verbosity, uids, pids, wp, wpname, rp, fields, inputdelim, gufitmp, cachedir, nthreads, gufitree = parseCmdLine( )

errorfile, wdir = ol.getProcFilename( gufitmp, "logs" )
sys.stderr = open(errorfile, 'a+')
print("The command line was: ",file=sys.stderr)
print(sys.argv,file=sys.stderr)

guficmd = qg.getGufiQryCmd( uids, pids, wp, wpname, rp, cachedir, nthreads, gufitree )
scriptfile, scriptdir = writeGufiScript( gufitmp, guficmd )
if verbosity:
    print(guficmd)
executeGufiScriptOnServer( scriptfile )
cfiles = glob.glob(qg.getOutputFilename( cachedir, gufitree, remove=False ) + '.*' )
if not fields == None:
    conCatReport( cfiles, gufitmp, fields )
