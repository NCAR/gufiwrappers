#!/usr/bin/env python

import argparse
import os

less_indent_formatter = lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=10)
gufitmp = os.path.join('/gpfs/fs1/scratch', 'sghosh', 'gufi_tmp')

def parserForGcache( ):
    """
    Mainly the argparser stuff dumped in a single function
    """
    global gufitmp
    parser = argparse.ArgumentParser(prog='gcahe',description="""Generate Cache DB and optionally a filename list for 
a given filesystem tree querying GUFI DB.""",
             formatter_class=less_indent_formatter,
             epilog="""The results are stored under
  1. <gufitmp>/raw     (the raw output from gufi_query)
  2. <gufitmp>/scripts (the scripts submitted to gufi_query)
  3. <gufitmp>/reports (the final reports, file lists etc.)
  4. <gufitmp>/log     (the errors etc.)""")
    parser.add_argument('--gufitmp-dir=', dest='gufitmp', default=gufitmp, 
             metavar='path-name', 
             help="""Absolute path name to store the GUFI query output
default: """ + gufitmp + """
 
    """)
    parser.add_argument('--storage=', dest='storage', nargs=1, 
                       metavar='project,campaign,hpss',default='project',
             help="""Storage device where files are stored in.
  
    """)
    parser.add_argument('--list=', dest='listd', nargs=1, required=False, 
                       metavar='filename,size,owner,project,mtime,atime',
             help="""Generate list of files with one or more of the attributes
from filename, size, owner, project, mtime, atime in order as
specified delimited by comma(,).  
  
    """)
    parser.add_argument('--owners=', dest='fuids', nargs=1, metavar='User1,User2,..',
             help="""for content owned only by users User1,User2,..
 
             """)
    parser.add_argument('--projects=', dest='projs', nargs=1, metavar='Proj1,Proj2,..',
             help="""for content associated with projects Proj1,Proj2.., 
(applicable only in HPSS)
 
             """)
    parser.add_argument('--write-period=', dest='writep', metavar='YYYY[MM[DD]]-YYYY[MM[DD]]',
             help="""for content written during the time window YYYY[MM[DD]]-YYYY[MM[DD]]
either of begin or end period may be omitted for open interval. Here
is how it will be interpreted:
   1.  YYYY[MM[DD]]- => times newer or equal to YYYY[MM[DD]]
   2. -YYYY[MM[DD]]  => times older or equal to YYYY[MM[DD]]
   3.  YYYY[MM[DD]]  => -YYYY[MM[DD]]
For time specification 4-digit year is required (implies 01 month and
01 day), 2-digit month may be specified (01 day), if month is specified 
2-digit day may be specified.

             """)
    parser.add_argument('--read-period=', dest='readp',  metavar='YYYY[MM[DD]]-YYYY[MM[DD]]',
             help="""for content read during time the window YYYY[MM[DD]]-YYYY[MM[DD]]
either of begin or end period may be omitted for open interval. Here
is how it will be interpreted:
   1.  YYYY[MM[DD]]- => times newer or equal to YYYY[MM[DD]]
   2. -YYYY[MM[DD]]  => times older or equal to YYYY[MM[DD]]
   3.  YYYY[MM[DD]]  => -YYYY[MM[DD]]
For time specification 4-digit year is required (implies 01 month and
01 day), 2-digit month may be specified (01 day), if month is specified 
2-digit day may be specified.

             """)
    parser.add_argument('--nthreads', dest='nthreads', default=20, 
             metavar='number-of-threads', help="""Number of threads to run GUFI query

    """)
    parser.add_argument('--verbose','-v',dest='verbosity', 
             action='store_true', help="""Adds verbosity

    """)
    parser.add_argument(dest='treename', metavar='Absolute path', help="""where absolute path in the filesystem tree starting with one of 
  1. /glade/p or /gpfs/fs1/p         for project spaces
  2. /glade/campaign or /gpfs/csfs1, for Campaign storage
  3. /                               for HPSS

""")
    return parser

def parserForGrprt( ):
    global gufitmp
    parser = argparse.ArgumentParser(description='Generate report from raw data',
             formatter_class=less_indent_formatter)
    parser.add_argument('--gufitmp-dir=', dest='gufitmp', default=gufitmp,
                    metavar='path-name',
                    help="""Absolute path name to store the GUFI query output default:
""" + gufitmp + """

""")
    parser.add_argument('--storage=', dest='storage', nargs=1, 
                       metavar='project,campaign,hpss',default='project',
             help="""Storage device where files are stored in.
  
    """)
    grprprtby = parser.add_mutually_exclusive_group(required=False)
    grprprtby.add_argument('--by-users', dest='byusers', action='store_true',
                       help="""report by user-name / user-ids (if mapping not found)

""")
    grprprtby.add_argument('--by-projects', dest='byprojects', action='store_true',
                       help="""report by project-name / project-id (if mapping not found) HPSS only

""")
    grprprtby.add_argument('--by-subdirs-of=', dest='subdirsof',  metavar='[Parent directory]',
                       help="""report by subdirectories of this parent directory

""")
    parser.add_argument('--filter-by-unames=', dest='fuids', nargs='+', metavar='[User1,User2,..]',
                    help="""Report only for User1[,User2]..

""")
    parser.add_argument('--filter-by-projects=', dest='fpids', nargs='+', metavar='[Project1,Project2,..]',
                    help="""Report only for Project1[,Project2]..

""")
    parser.add_argument('--write-period=', dest='writep', metavar='YYYY[MM[DD]]-YYYY[MM[DD]]',
             help="""for content written during the time window YYYY[MM[DD]]-YYYY[MM[DD]]
either of begin or end period may be omitted for open interval. Here
is how it will be interpreted:
   1.  YYYY[MM[DD]]- => times newer or equal to YYYY[MM[DD]]
   2. -YYYY[MM[DD]]  => times older or equal to YYYY[MM[DD]]
   3.  YYYY[MM[DD]]  => -YYYY[MM[DD]]
For time specification 4-digit year is required (implies 01 month and
01 day), 2-digit month may be specified (01 day), if month is specified 
2-digit day may be specified.

             """)
    parser.add_argument('--read-period=', dest='readp',  metavar='YYYY[MM[DD]]-YYYY[MM[DD]]',
             help="""for content read during time the window YYYY[MM[DD]]-YYYY[MM[DD]]
either of begin or end period may be omitted for open interval. Here
is how it will be interpreted:
   1.  YYYY[MM[DD]]- => times newer or equal to YYYY[MM[DD]]
   2. -YYYY[MM[DD]]  => times older or equal to YYYY[MM[DD]]
   3.  YYYY[MM[DD]]  => -YYYY[MM[DD]]
For time specification 4-digit year is required (implies 01 month and
01 day), 2-digit month may be specified (01 day), if month is specified 
2-digit day may be specified.

             """)
    parser.add_argument('--nthreads', dest='ncores', default=1, metavar='number-of-cores or processes',
                      help="""Number of cores / threads to run

""")
    parser.add_argument('--nsbins', dest='nsbins', default=8, metavar='number-of-histogram bins [8]',
                       help="""Number of write / read stat histogram bins in report

""")
    parser.add_argument(dest='treename', help="""Absolute path of the filesystem tree located in\
                          either in glade, campaign or HPSS

""")
    return parser


def parserForGplot( ):
    parser = argparse.ArgumentParser(description='Generate plot from histogram data')
    parser.add_argument(dest='histfile', help='Name of the histogram file generated by running grprt')
    return parser

if __name__ == "__main__":
    import getpass
    username = getpass.getuser()
    gufitmp = os.path.join('/gpfs/fs1/scratch', username, 'gufi_tmp')
    parserForCache( ).parse_args()
#   parserForGrprt( ).parse_args()
#   parserForGplot( ).parse_args()
