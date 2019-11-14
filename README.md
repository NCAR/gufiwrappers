


These scripts are to help end users effectively and conveniently
use GUFI to manage their holdings under Project, Campaign and HPSS.
The gcache and gfind are to be run on the server on which GUFI DB
resides while grprt can be run anywhere as long as there is a decent
installation of python3.
usage: gwrap [-h] [--gufitmp-dir= path-name]
             [--list= filename,size,owner,project,mtime,atime]
             [--owners= User1,User2,..] [--projects= Proj1,Proj2,..]
             [--write-period= YYYY[MM[DD]]-YYYY[MM[DD]]]
             [--read-period= YYYY[MM[DD]]-YYYY[MM[DD]]]
             [--nthreads number-of-threads] [--verbose]
             Absolute Path of filesystem directory

Generate Cache DB and optionally a filename list for a given filesystem tree
querying GUFI DB

positional arguments:
  Absolute Path of filesystem directory
                        Absolute path of the filesystem tree located in either
                        in glade, campaign or HPSS

optional arguments:
  -h, --help            show this help message and exit
  --gufitmp-dir= path-name
                        Absolute path name to store the GUFI query output
                        default: /gpfs/fs1/scratch/sghosh/gufi_tmp
  --list= filename,size,owner,project,mtime,atime
                        Generate list of files with one or more of the
                        attributes from filename, size, owner, project, mtime,
                        atime in order as specified delimited by comma(,).
  --owners= User1,User2,..
                        for content owned only by users User1,User2,..
  --projects= Proj1,Proj2,..
                        for content associated with projects Proj1,Proj2..,
                        (applicable only in HPSS)
  --write-period= YYYY[MM[DD]]-YYYY[MM[DD]]
                        for content written during the time window
                        YYYY[MM[DD]]-YYYY[MM[DD]] either of begin or end
                        period may be omitted for open interval but not both.
                        For time specification 4-digit year is required,
                        2-digit month may be specified, if month is specified
                        2-digit may be specified.
  --read-period= YYYY[MM[DD]]-YYYY[MM[DD]]
                        for content read during time the window
                        YYYY[MM[DD]]-YYYY[MM[DD]] either of begin or end
                        period may be omitted for open interval but not both.
                        For time specification 4-digit year is required,
                        2-digit month may be specified, if month is specified
                        2-digit may be specified.
  --nthreads number-of-threads
                        Number of threads to run GUFI query
  --verbose, -v         Adds verbosity

The results are stored by default under 1. gufitmp-dir/raw (the raw output
from gufi_query) 2. gufitmp-dir/scripts (the scripts submitted to gufi_query)
3. gufitmp-dir/reports (the final reports, file lists etc.) 4. gufitmp-dir/log
(the errors etc.)
