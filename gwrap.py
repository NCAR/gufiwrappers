#!/usr/bin/env python

import os
import sys
import argparse
import glob
import gmapfuncs as gmap
import timefuncs as tm
import querygen as qg


def getProcFilename( gufitmp, ftype ):
    """
    returns data-time attached script-filename
    """
    import time
    from datetime import datetime
    ts = datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    if ftype == 'script':
       fn = ftype[:3] + '_' + ts + '.sh'
       wdir = os.path.join(gufitmp, 'scripts')
    else:
       fn = ftype[:3] + '_' + ts + '.dat'
       wdir = os.path.join(gufitmp, 'reports')
    if not os.path.exists(wdir):
       os.system('mkdir -p ' + wdir)
    fullfn = os.path.join(wdir, fn )
    return fullfn, wdir

def writeGufiScript( gufitmp, guficmd ):
    """
    Writes gufi script file in scriptdir
    """
    scrfile, scriptdir = getProcFilename( gufitmp, 'script' )
    with open(scrfile, 'w') as fh:
       fh.write('%s\n\n' % '#!/bin/bash')
       fh.write('%s\n' % guficmd)
    fh.close()
    os.system('chmod +x ' + scrfile)
    return scrfile, scriptdir

def conCatReport( cfiles, gufitmp, inputfields ):
    repfile, repdir = getProcFilename( gufitmp, 'report' )
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
                      proj = gmap.getPname( int(tmp[4]) ); 
                      fullname = '/'.join([gmap.searchToFsName(tmp[6]),tmp[5]])
                   else:
                      proj = 'NULL'; 
                      fullname = '/'.join([gmap.searchToFsName(tmp[5]),tmp[4]])
                   if atime < mtime:
                      atime = mtime
                   fdict = {'filename':fullname, 'size':str(size), 'owner':gmap.getUname( uid ),
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
    sshcmd = 'ssh -oHostBasedAuthentication=yes squall1.ucar.edu'
    fullcmd = ' '.join([sshcmd, scriptfile])
    os.system(fullcmd)
    

def parseCmdLine( ):
    """
    Mainly the argparser stuff dumped in a single function
    """
    gufitmp = os.path.join('/gpfs/fs1/scratch', os.environ['LOGNAME'], 'gufi_tmp')
    parser = argparse.ArgumentParser(prog='gwrap',description='Generate Cache DB and\
             optionally a filename list for a given filesystem tree \
             querying GUFI DB', epilog="""
             The results are stored by default under
                1. gufitmp-dir/raw     (the raw output from gufi_query)
                2. gufitmp-dir/scripts (the scripts submitted to gufi_query)
                3. gufitmp-dir/reports (the final reports, file lists etc.)
                4. gufitmp-dir/log     (the errors etc.)
             """)
    parser.add_argument('--gufitmp-dir=', dest='gufitmp', default=gufitmp, 
                    metavar='path-name',
                    help='Absolute path name to store the GUFI query output\
                    default: ' + gufitmp)
    parser.add_argument('--list=', dest='listd', nargs=1, required=False, 
                       metavar='filename,size,owner,project,mtime,atime',
                       help='Generate list of files with one or more of the attributes\
                       from filename, size, owner, project, mtime, atime in order as\
                       specified delimited by comma(,).')
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
    parser.add_argument('--verbose','-v',dest='verbosity', action='store_true', help='Adds verbosity')
    parser.add_argument(dest='treename', metavar='Absolute Path of filesystem directory',
                        help='Absolute path of the filesystem tree located in\
                          either in glade, campaign or HPSS')
    args = parser.parse_args()
    gufitmp = args.gufitmp
    fields = args.listd[0].split(',')
    cachedir = os.path.join(gufitmp, 'raw')
    uids = gmap.getUlist( args.fuids, 'users' )
    pids = gmap.getUlist( args.projs, 'projects' )
    wp = tm.procPeriod( args.writep )
    rp = tm.procPeriod( args.readp )
    nthreads = args.nthreads
    verbosity = args.verbosity
    gufitree = gmap.fsnameToSearch( args.treename )
    if gufitree.startswith('/search/hpss'):
       wpname = 'ctime'
    else:
       wpname = 'mtime'
    inputdelim = ','
    if verbosity:
       print('Using cachedir: ',cachedir)
       print('users: ',uids)
       print('projects: ',pids)
       print('write-period: ',wp)
       print('read-period: ',rp)
       print('list mode:',lmode)
    return verbosity, uids, pids, wp, wpname, rp, fields, inputdelim, gufitmp, cachedir, nthreads, gufitree



verbosity, uids, pids, wp, wpname, rp, fields, inputdelim, gufitmp, cachedir, nthreads, gufitree = parseCmdLine( )
guficmd = qg.getGufiQryCmd( uids, pids, wp, wpname, rp, cachedir, nthreads, gufitree )
scriptfile, scriptdir = writeGufiScript( gufitmp, guficmd )
if verbosity:
    print(guficmd)
executeGufiScriptOnServer( scriptfile )
cfiles = glob.glob(qg.getOutputFilename( cachedir, gufitree, remove=False ) + '.*' )
if not fields == None:
    conCatReport( cfiles, gufitmp, fields )
