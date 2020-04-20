#!/usr/bin/env python

import os
import getpass
import cmdline as cmdl
import glob
import gcache
import grprt
import timefuncs as tm

parsedata = {}

def checkListFields( listfields ):
    """
    Checks the list fields matches with expected entries
    """
    validfields = ['filename', 'size', 'owner', 'project', 'mtime', 'atime']
    for ent in listfields:
       if ent not in validfields:
           print("The field ",ent," not valid, the list of valid field is: ", validfields)
           exit(-1)
    return True


def parseCmdLine( ):
    """
    Actual parser is in cmdline module, here things are just passed along
    """
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
         'fuids':args.fuids, 'fpids':args.fpids, 'writep':tm.procPeriod( args.writep ),
         'readp':tm.procPeriod( args.readp ), 'storage':args.storage[0], 'treename':args.treename,
         'byusers':args.byusers, 'byprojects':args.byprojects, 'bysubdirs':args.bysubdirs,
         'ncores':int(args.ncores), 'nsbins':int(args.nsbins), 'fields':fields} 
    return parsedata
    
if __name__ == "__main__":
    parsedata = parseCmdLine( )
    gcache.driver( parsedata )
    if parsedata['fields'] == None:
       grprt.driver( parsedata )
