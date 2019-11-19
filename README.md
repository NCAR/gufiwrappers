# gufiwrappers

**gufiwrappers** is a collection of python scripts for NCAR users
of our Grand Unified File Index (GUFI) installation for querying
and reporting against out data holdings under different CISL 
maintained NCAR storage devices. The syntax of Raw **GUFI** 
query tools are somewhat terse and output most often 
requires further processing for meaningful and actionable reports. 
Hence is the reason for coming up with these wrappers.

The **GUFI** tools (primarily gufi_query or multi-threaded breadth
first search in a tree) generates raw reports, in csv
format, one file per thread. Considering the format and mechanism of
generation of this input the **gufiwrappers** tool set is broken 
into two parts,
1. gwrap (generates raw reports and optionally a file list))
2. grprt (generates statistics from raw report)
So functionally users need to execute these two commands in 
sequence.

Both the scripts are available in users path after loading **gufiwrappers**
module on Casper nodes. Both of these scripts have '-h/--help' option
for basic usage details. In this page little more elabore usage detail
and few example output is explained.


## gwrap
usage: gwrap [-h] [--gufitmp-dir= path-name]\
             [--list= filename,size,owner,project,mtime,atime]\
             [--owners= User1,User2,..] [--projects= Proj1,Proj2,..]\
             [--write-period= YYYY[MM[DD]]-YYYY[MM[DD]]]\
             [--read-period= YYYY[MM[DD]]-YYYY[MM[DD]]]\
             [--nthreads number-of-threads] [--verbose]\
             Absolute Path of filesystem directory\
\
Generate Cache DB and optionally a filename list for a given filesystem tree
querying GUFI DB
\
positional arguments:\
  Absolute Path of filesystem directory\
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
