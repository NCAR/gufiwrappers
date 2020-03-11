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
    global parsedata
    username = getpass.getuser()
    gufitmp = os.path.join('/gpfs/fs1/scratch', username, 'gufi_tmp')
    cmdl.gufitmp = gufitmp
    parser = cmdl.parserForQdh( )
    args = parser.parse_args()
    try:
       fields = args.listd[0].split(',')
       checkListFields( fields )
    except:
       fields = None
    parsedata = {'gufitmp':args.gufitmp, 'verbosity':args.verbosity, 'cachedir':os.path.join(gufitmp, 'raw'),
         'uids':args.fuids, 'pids':args.fpids, 'writep':tm.procPeriod( args.writep ),
         'readp':tm.procPeriod( args.readp ), 'storage':args.storage[0], 'treename':args.treename,
         'ncores':int(args.ncores), 'nsbins':int(args.nsbins), 'fields':fields} 
    





if __name__ == "__main__":
    parseCmdLine( )
    gcache.driver( parsedata )
