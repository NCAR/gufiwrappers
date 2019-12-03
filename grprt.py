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
from datetime import datetime
import time

bdb.MAXHBINS = 1024  # Maximum histogram bins

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
    gufitmp = os.path.join('/gpfs/fs1/scratch', os.environ['LOGNAME'], 'gufi_tmp')
    cmdl.gufitmp = gufitmp
    parser = cmdl.parserForGrprt( )
    args = parser.parse_args()
    gufitmp = args.gufitmp
    cachedir = os.path.join( gufitmp, 'raw' )
    gufitree = gmap.fsnameToSearch( args.treename )
    cfiles = glob.glob(qg.getOutputFilename( cachedir, gufitree, remove=False ) + '.*' )
    ncores = int(args.ncores)
    nsbins = int(args.nsbins)
    return gufitmp, args.byusers, args.byprojects, args.subdirsof, args.fuids, \
           args.fpids, cfiles, ncores, args.nsbins


if __name__ == "__main__":
    gufitmp, byusers, byprojects, subdirsof, fuids, fpids, \
    cfiles, ncores, nsbins = parseCmdLine( )

    errorfile, wdir = ol.getProcFilename( gufitmp, "log" )
    sys.stderr = open(errorfile, 'w')
    print("The command line was: ",file=sys.stderr)
    print(sys.argv,file=sys.stderr)
    reportfile, wdir = ol.getProcFilename( gufitmp, "report" )
    repfh = open(reportfile, 'w')

    if not fuids == None:
        setFilterByUids( fuids[0].split(',') )

    if not fpids == None:
        setFilterByPids( fpids[0].split(',') )

    if byprojects:
       bdb.prefixdir = '/'
       activefunc = bdb.dataByProjs
       header = "Projs"
    elif subdirsof:
       bdb.prefixdir = gmap.fsnameToSearch( subdirsof )
       activefunc = bdb.dataBySubDirs
       header = "Subdirs"
    else:
       bdb.prefixdir = '/'
       activefunc = bdb.dataByUids
       header = "Uname/Uids"

    res, total, basedir = bdb.getDataByFields(ncores, activefunc, cfiles )
    dpy.displayDataByKey( res, total, basedir, nsbins, header, repfh )
    repfh.close()

    histfile, wdir = ol.getProcFilename( gufitmp, "hist" )
    dpy.dumpHistByKey( res, header, histfile )

    sys.stderr.close()
