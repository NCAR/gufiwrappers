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
    gufitmp = os.path.join('/gpfs/fs1/scratch', os.environ['LOGNAME'], 'gufi_tmp')
    parser = argparse.ArgumentParser(description='Generate report from raw data')
    parser.add_argument('--gufitmp-dir=', dest='gufitmp', default=gufitmp,
                    metavar='path-name',
                    help='Absolute path name to store the GUFI query output\
                    default: ' + gufitmp)
    grprprtby = parser.add_mutually_exclusive_group(required=False)
    grprprtby.add_argument('--by-users', dest='byusers', action='store_true',
                       help='report by user-name / user-ids (if mapping not found)')
    grprprtby.add_argument('--by-projects', dest='byprojects', action='store_true', 
                       help='report by project-name / project-id (if mapping not found) HPSS only')
    grprprtby.add_argument('--by-subdirs-of=', dest='subdirsof',  metavar='[Parent directory]',
                       help='report by subdirectories of this parent directory')
    parser.add_argument('--filter-by-unames=', dest='fuids', nargs='+', metavar='[User1,User2,..]',
                    help='Report only for User1[,User2]..')
    parser.add_argument('--filter-by-projects=', dest='fpids', nargs='+', metavar='[Project1,Project2,..]',
                    help='Report only for Project1[,Project2]..')
    parser.add_argument('--nthreads', dest='ncores', default=1, metavar='number-of-cores or processes',
                      help='Number of cores / threads to run')
    parser.add_argument('--nsbins', dest='nsbins', default=8, metavar='number-of-histogram bins [8]',
                       help='Number of write / read stat histogram bins')
    parser.add_argument('--hist', dest='hist', nargs='+', metavar='Histogram output file',
                       help='CSV file name for histgram data')
    parser.add_argument(dest='treename', help='Absolute path of the filesystem tree located in\
                          either in glade, campaign or HPSS')
    args = parser.parse_args()
    gufitmp = args.gufitmp
    cachedir = os.path.join( gufitmp, 'raw' )
    gufitree = gmap.fsnameToSearch( args.treename )
    cfiles = glob.glob(qg.getOutputFilename( cachedir, gufitree, remove=False ) + '.*' )
    ncores = int(args.ncores)
    nsbins = int(args.nsbins)
    return gufitmp, args.byusers, args.byprojects, args.subdirsof, args.fuids, \
           args.fpids, cfiles, ncores, args.nsbins, args.hist 


if __name__ == "__main__":
    gufitmp, byusers, byprojects, subdirsof, fuids, fpids, cfiles, ncores, nsbins, hist = parseCmdLine( )

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

    if not hist == None:
       dpy.dumpHistByKey( res, header, hist[0] )

sys.stderr.close()
