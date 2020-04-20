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
    """
    If list option is given then this routine writes the output
    """
    repfile, repdir = ol.getProcFilename( gufitmp, 'report' )
    print("-"*80)
    print("Writing output in file:")
    print(repfile)
    print("-"*80)
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
                      fullname = '/'.join([tmp[6][7:],tmp[5]])
                   else:
                      proj = 'NULL'; 
                      fullname = '/'.join([tmp[5][7:],tmp[4]])
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
    import subprocess
    result = subprocess.run(scriptfile)
    

def driver( parsedata ):
    """
    The main driver, caches the data querying gufi_query and optionally
    producing a flat list of files.
    """
    verbosity = parsedata['verbosity']
    fuids = gm.getUlist( parsedata['fuids'], 'users' )
    fpids = gm.getUlist( parsedata['fpids'], 'projects' )
    wp = parsedata['writep'] 
    rp = parsedata['readp'] 
    storage = parsedata['storage']
    if storage.startswith('hpss'):
       wpname = 'ctime'
    else:
       wpname = 'mtime'
    fields = parsedata['fields']
    inputdelim = ','
    gufitmp = parsedata['gufitmp']
    cachedir = parsedata['cachedir']
    nthreads = parsedata['ncores']
    gufitree = gm.fsnameToSearch( storage, parsedata['treename'] )

    errorfile, wdir = ol.getProcFilename( gufitmp, "logs" )
    print("-"*80)
    print("Writing log file...", errorfile)
    sys.stderr = open(errorfile, 'a+')
    print("The command line was: ",file=sys.stderr)
    print(sys.argv,file=sys.stderr)

    guficmd, filen = qg.getGufiQryCmd( fuids, fpids, wp, wpname, rp, cachedir, nthreads, gufitree )
    scriptfile, scriptdir = writeGufiScript( gufitmp, guficmd )
    print("Executing gufi command...writing cache files in:")
    print("  ",filen + ".*")    
    print("-"*80)
    if verbosity:
        print(guficmd)
    executeGufiScriptOnServer( scriptfile )
    cfiles = glob.glob(qg.getOutputFilename( cachedir, gufitree, remove=False ) + '.*' )
    if not fields == None:
        conCatReport( cfiles, gufitmp, fields )
