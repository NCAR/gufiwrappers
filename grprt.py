#!/usr/bin/env python

import os
import sys
import argparse
import glob
import numpy as np
import builddb as bdb
import gmapfuncs as gmap
import querygen as qg
import dsplyfunc as dpy
import outputlocs as ol
from multiprocessing import Pool
import timefuncs as tm

bdb.MAXHBINS = 1024  # Maximum histogram bins

def setFilterBywp( fwp ):
    """
    sets the filter DB
    """
    bdb.fwp = fwp
    bdb.fixWpRpList( )

def setFilterByrp( frp ):
    """
    sets the filter DB
    """
    bdb.frp = frp
    bdb.fixWpRpList( )
    print(frp)

def setFilterByUids( uids ):
    """
    sets the filter DB
    """
    for uid in uids:
       bdb.fuidpid.append( gmap.getUid( uid )) 

def setFilterByPids( pids ):
    """
    sets the filter DB
    """
    for pid in pids:
       bdb.fuidpid.append( gmap.getPid( pid )) 


def parseCmdLine( ):
    import cmdline as cmdl
    import getpass
    username = getpass.getuser()
    gufitmp = os.path.join('/gpfs/fs1/scratch', username, 'gufi_tmp')
    cmdl.gufitmp = gufitmp
    parser = cmdl.parserForGrprt( )
    args = parser.parse_args()
    gufitmp = args.gufitmp
    cachedir = os.path.join( gufitmp, 'raw' )
    fwp = tm.procPeriod( args.writep )
    frp = tm.procPeriod( args.readp )
    storage = args.storage[0]
    gufitree = gmap.fsnameToSearch( storage, args.treename )
    filen = qg.getOutputFilename( cachedir, gufitree, remove=False )
    print("-"*80)
    print("Using cache file(s).. ",filen + ".*")
    cfiles = glob.glob(filen + '.*' )
    ncores = int(args.ncores)
    nsbins = int(args.nsbins)
    return gufitmp, storage, args.byusers, args.byprojects, args.subdirsof, args.fuids, \
           args.fpids, fwp, frp, cfiles, ncores, args.nsbins


if __name__ == "__main__":
    gufitmp, storage, byusers, byprojects, subdirsof, fuids, fpids, \
    fwp, frp, cfiles, ncores, nsbins = parseCmdLine( )

    errorfile, wdir = ol.getProcFilename( gufitmp, "log" )
    sys.stderr = open(errorfile, 'w')
    print("Writing log file.. ",errorfile)
    print("The command line was: ",file=sys.stderr)
    print(sys.argv,file=sys.stderr)
    reportfile, wdir = ol.getProcFilename( gufitmp, "report" )
    repfh = open(reportfile, 'w')

    if not fuids == None:
        setFilterByUids( fuids[0].split(',') )

    if not fpids == None:
        setFilterByPids( fpids[0].split(',') )

    if bool(fwp):
        setFilterBywp( fwp )

    if bool(frp):
        setFilterByrp( frp )

    if byprojects:
       bdb.prefixdir = '/'
       activefunc = bdb.dataByProjs
       header = "Projs"
    elif subdirsof:
       bdb.prefixdir = gmap.fsnameToSearch( storage, subdirsof )
       activefunc = bdb.dataBySubDirs
       header = "Subdirs"
    else:
       bdb.prefixdir = '/'
       activefunc = bdb.dataByUids
       header = "Uname/Uids"

    res, total, basedir = bdb.getDataByFields(ncores, activefunc, cfiles )
    print("-"*80)
    print("Writing report file.. ",reportfile)
    dpy.displayDataByKey( res, total, basedir, nsbins, header, repfh )
    repfh.close()

    histfile, wdir = ol.getProcFilename( gufitmp, "hist" )
    print("Writing histogram file.. ",histfile)
    print("-"*80)
    dpy.dumpHistByKey( res, header, histfile )

    sys.stderr.close()
