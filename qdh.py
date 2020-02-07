#!/usr/bin/env python

import os
import getpass
import cmdline as cmdl

def parseCmdLine( ):
    username = getpass.getuser()
    gufitmp = os.path.join('/gpfs/fs1/scratch', username, 'gufi_tmp')
    cmdl.gufitmp = gufitmp
    parser = cmdl.parserForQdh( )
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
