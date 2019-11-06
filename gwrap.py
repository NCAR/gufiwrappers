#!/usr/bin/env python

import os
import argparse
import gmapfuncs as gmap
import timefuncs as tm
import querygen as qg


gufitmp = os.path.join('/gpfs/fs1/scratch', os.environ['LOGNAME'], 'gufi_tmp')
defcachepref = os.path.join(gufitmp, 'cache')

parser = argparse.ArgumentParser(description='Generate Cache DB for a given tree')
parser.add_argument('--cache-dir=', '-c', dest='cdir', default=defcachepref, 
                    metavar='path-name',
                    help='Absolute path name to store the GUFI query output\
                    default: ' + defcachepref)
parser.add_argument('--list-mode=', dest='lmode', nargs=1, required=False, 
                       metavar='filename[,size[,owner[,project[,mtime[,atime]]]]]',
                       help='Generate list of files with one or more of the attributes\
                       from filename, size, owner, project, mtime, atime in order as\
                       specified delimited by comma(,). This mode toggles with the default\
                       cache mode output for post-processing using grprt.')
parser.add_argument('--owners=', dest='fuids', nargs=1, metavar='User1,User2,..',
                    help='for content owned only by users User1,User2,..')
parser.add_argument('--projects=', dest='projs', nargs=1, metavar='Proj1,Proj2,..',
                    help='for content associated with projects Proj1,Proj2.., (applicable\
                          only in HPSS)')
parser.add_argument('--write-period=', dest='writep', metavar='YYYY[MM[DD]]-YYYY[MM[DD]]',
                    help='for content written during the time window YYYY[MM[DD]]-YYYY[MM[DD]] \
                          either of begin or end period may be omitted for open interval but\
                          not both. For time specification 4-digit year is required, 2-digit\
                          month may be specified, if month is specified 2-digit may be specified.')
parser.add_argument('--read-period=', dest='readp',  metavar='YYYY[MM[DD]]-YYYY[MM[DD]]',
                    help='for content read during time the window YYYY[MM[DD]]-YYYY[MM[DD]] \
                          either of begin or end period may be omitted for open interval but\
                          not both. For time specification 4-digit year is required, 2-digit\
                          month may be specified, if month is specified 2-digit may be specified.')
parser.add_argument('--nthreads', dest='nthreads', default=20, metavar='number-of-threads',
                     help='Number of threads to run GUFI query')
parser.add_argument(dest='treename', help='Absolute path of the filesystem located in\
                          either in glade, campaign or HPSS')

args = parser.parse_args()


lmode = args.lmode
cachedir = args.cdir
uids = gmap.getUlist( args.fuids, 'users' )
pids = gmap.getUlist( args.projs, 'projects' )
wp = tm.procPeriod( args.writep )
rp = tm.procPeriod( args.readp )
nthreads = args.nthreads
gufitree = gmap.fsnameToSearch( args.treename )
if gufitree.startswith('/search/hpss'):
   wpname = 'ctime'
else:
   wpname = 'mtime'
print('cachedir: ',cachedir)
print('users: ',uids)
print('projects: ',pids)
print('write-period: ',wp)
print('read-period: ',rp)
print('list mode:',lmode)
inputdelim = ','
fullcmd = qg.getGufiQryCmd( uids, pids, wp, wpname, rp, lmode, inputdelim,
                   cachedir, nthreads, gufitree )
print(fullcmd)
