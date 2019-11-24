#!/usr/bin/env python

import argparse
import os

gufitmp = os.path.join('/gpfs/fs1/scratch', os.environ['LOGNAME'], 'gufi_tmp')
less_indent_formatter = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=10)

def parserForGwrap( ):
    """
    Mainly the argparser stuff dumped in a single function
    """
    global gufitmp
    parser = argparse.ArgumentParser(prog='gwrap',description="""Generate Cache DB and optionally a filename list for 
a given filesystem tree querying GUFI DB.""",
             formatter_class=less_indent_formatter,
             epilog="""The results are stored under
  1. <gufitmp>/raw     (the raw output from gufi_query)
  2. <gufitmp>/scripts (the scripts submitted to gufi_query)
  3. <gufitmp>/reports (the final reports, file lists etc.)
  4. <gufitmp>/log     (the errors etc.)""")
    parser.add_argument('--gufitmp-dir=', dest='gufitmp', default=gufitmp, 
             metavar='path-name', 
             help="""
Absolute path name to store the GUFI query output
default: """ + gufitmp + """
 
    """)
    parser.add_argument('--list=', dest='listd', nargs=1, required=False, 
                       metavar='filename,size,owner,project,mtime,atime',
             help="""
Generate list of files with one or more of the attributes
from filename, size, owner, project, mtime, atime in order as
specified delimited by comma(,).  
  
    """)
    parser.add_argument('--owners=', dest='fuids', nargs=1, metavar='User1,User2,..',
             help="""
for content owned only by users User1,User2,..
 
             """)
    parser.add_argument('--projects=', dest='projs', nargs=1, metavar='Proj1,Proj2,..',
             help="""
for content associated with projects Proj1,Proj2.., 
(applicable only in HPSS)
 
             """)
    parser.add_argument('--write-period=', dest='writep', metavar='YYYY[MM[DD]]-YYYY[MM[DD]]',
             help="""
for content written during the time window YYYY[MM[DD]]-YYYY[MM[DD]]
either of begin or end period may be omitted for open interval but
not both. For time specification 4-digit year is required, 2-digit
month may be specified, if month is specified 2-digit may be specified.

             """)
    parser.add_argument('--read-period=', dest='readp',  metavar='YYYY[MM[DD]]-YYYY[MM[DD]]',
             help="""
for content read during time the window YYYY[MM[DD]]-YYYY[MM[DD]]
either of begin or end period may be omitted for open interval but
not both. For time specification 4-digit year is required, 2-digit
month may be specified, if month is specified 2-digit may be specified.

             """)
    parser.add_argument('--nthreads', dest='nthreads', default=20, 
             metavar='number-of-threads', help="""
Number of threads to run GUFI query
    """)
    parser.add_argument('--verbose','-v',dest='verbosity', 
             action='store_true', help="""
Adds verbosity
    """)
    parser.add_argument(dest='treename', metavar='Absolute path', help="""
where absolute path in the filesystem tree starting with one of 
  1. /glade/p or /gpfs/fs1/p         for project spaces
  2. /glade/campaign or /gpfs/csfs1, for Campaign storage
  3. /                               for HPSS""")
    return parser



if __name__ == "__main__":
    parserForGwrap( ).parse_args()
    