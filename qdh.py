#!/usr/bin/env python

import os
import getpass
import cmdline as cmdl
import glob
import gcache
import timefuncs as tm

parsedata = {}

def checkListFields( listfields ):
    validfields = ['filename', 'size', 'owner', 'project', 'mtime', 'atime']
    for ent in listfields:
       if ent not in validfields:
           print("The field ",ent," not valid, the list of valid field is: ", validfields)
           exit(-1)
    return True


def getCfiles4Tree( treename ):
    print("-"*80)
    print("Using cache file(s).. ",filen + ".*")
    gufitree = gmap.fsnameToSearch( storage, treename )
    filen = qg.getOutputFilename( cachedir, gufitree, remove=False )
    return glob.glob(filen + '.*' )

def parseCmdLine( ):
    username = getpass.getuser()
    gufitmp = os.path.join('/gpfs/fs1/scratch', username, 'gufi_tmp')
    cmdl.gufitmp = gufitmp
    parser = cmdl.parserForQdh( )
    args = parser.parse_args()
    parsedata['gufitmp'] = args.gufitmp
    parsedata['verbosity'] = args.verbosity
    parsedata['cachedir'] = os.path.join( gufitmp, 'raw' )
    parsedata['uids'] = args.fuids
    parsedata['pids'] = args.fpids
    parsedata['writep'] = tm.procPeriod( args.writep )
    parsedata['readp'] = tm.procPeriod( args.readp )
    parsedata['storage'] = args.storage[0]
    parsedata['treename'] = args.treename
    parsedata['ncores'] = int(args.ncores)
    parsedata['nsbins'] = int(args.nsbins)
    try:
       fields = args.listd[0].split(',')
       checkListFields( fields )
    except:
       fields = None
    parsedata['fields'] = fields
    






if __name__ == "__main__":
    parseCmdLine( )
    gcache.driver( parsedata )
