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


def getCfiles( gufitmp, gufitree ):
    """
    returns the list of cachefiles to be used as input for the report
    """
    cachedir = os.path.join( gufitmp, 'raw' )
    filen = qg.getOutputFilename( cachedir, gufitree, remove=False )
    print("-"*80)
    print("Using cache file(s).. ",filen + ".*")
    return glob.glob(filen + '.*' )


def driver( parsedata ):
    gufitmp = parsedata['gufitmp']; storage = parsedata['storage']; 
    byusers = parsedata['byusers']; byprojects = parsedata['byprojects']; 
    bysubdirs = parsedata['bysubdirs']; fuids = parsedata['fuids'];
    fpids = parsedata['fpids']; fwp = parsedata['writep']; 
    frp = parsedata['readp']; ncores = parsedata['ncores']; 
    nsbins = parsedata['nsbins']; treename = parsedata['treename']
    gufitree = gmap.fsnameToSearch( storage, treename )
    cfiles = getCfiles( gufitmp, gufitree )

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
       activefunc = bdb.dataByProjs
       header = "Projs"
    elif bysubdirs:
       activefunc = bdb.dataBySubDirs
       header = "Subdirs"
    else:
       activefunc = bdb.dataByUids
       header = "Uname/Uids"

    res, total = bdb.getDataByFields(gufitree, ncores, activefunc, cfiles )
    print("-"*80)
    print("Writing report file.. ",reportfile)
    dpy.displayDataByKey( res, total, treename, nsbins, header, repfh )
    repfh.close()

    histfile, wdir = ol.getProcFilename( gufitmp, "hist" )
    print("Writing histogram file.. ",histfile)
    print("-"*80)
    dpy.dumpHistByKey( res, header, histfile )

    sys.stderr.close()
