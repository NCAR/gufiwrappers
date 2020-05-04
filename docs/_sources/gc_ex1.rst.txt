List files owned by a user stored in any directory under HPSS
***********************

If you need to generate the list of files,

#.  owned by user *xyz123* 

in any directory under HPSS and list the files with 

#. project-name 
#. size and 
#. filename 

in comma separated format with one file per line then:

#. login to casper
#. module load gufiwrappers
#. **qdh \-\-storage=hpss \-\-list=project,size,filename \-\-owners=xyz123 \-\-directory=/**

The above command will run GUFI query in **squall** and generate the
filelist with date-time-stamped filename as:

/glade/scratch/<user-name>/gufi_tmp/reports/rep_ccYYmmdd_HHMMss.dat

where,

#. cc is for 2 digit century 19 for 19xx and 20 for 20xx
#. YY is 2 digit year e.g. 13 for 2013
#. mm is 2 digit month (1..12)
#. dd is 2 digit day (1..31)
#. HH is 2 digit hour (0..23)
#. MM is 2 digit minute (0..59)
#. ss is 2 digit second (0..59)

The first few lines may appear as::

    315566080,SCSG0001,/home/xyz123/test/icess_cam_waccm_code.tar
    1575905280,SCSG0001,/home/xyz123/test/icess_cam_waccm_data.tar
    20480,SCSG0001,/home/xyz123/test/memmon.tar
    2193511124,SCSG0001,/home/xyz123/test/oliker.tgz
    1374496,SCSG0001,/home/xyz123/test/vim74.tar.idx
    116719,SCSG0001,/home/xyz123/test4/test5/ts.jpg
    :
    :

where, the character comma (,) is the delimiter, 

#. first field is the size in bytes, 
#. second field is the project name and 
#. 3rd field is the filename with absolute path.

.. include:: footer.txt
