List files owned by a user and written between year 2010 and 2015
***********************

If you need to generate a list of files,

#.  owned by user *xyz123* 
#.  written (or created) between year 2010 and 2015

in any directory under HPSS with 

#. project-name 
#. size 
#. modification time
#. filename 

in comma separated format with one file per line then:

#. login to casper
#. module load gufiwrappers
#. **qdh \-\-storage=hpss \-\-list=project,size,mtime,filename \-\-owners=xyz123 \-\-write-period=2010-2015 --directory=/**

The above command will run GUFI query in **squall1** and generate the
filelist under

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

    116719,SCSG0001,2012-05-04,/home/xyz123/test4/ts.jpg
    4031308,SCSG0001,2012-02-13,/home/xyz123/pwsc1pqr/PQR_filelist
    150556190720,SCSG0001,2012-02-13,/home/xyz123/pwsc1pqr/XYZQ-1_PQR.tar
    63717500,SCSG0001,2011-07-01,/home/xyz123/archives/rfp11/comp_lic.tar.gz
    394240,SCSG0001,2014-11-03,/home/xyz123/test3/2014:11:03.htar
    3872,SCSG0001,2014-11-03,/home/xyz123/test3/2014:11:03.htar.idx
    0,SCSG0001,2011-10-31,/home/xyz123/test3/junk
    :
    :

where, the character comma (,) is the delimiter, 

#. first field is the size in bytes, 
#. second field is the project name and 
#. 3rd field is the modification time
#. 4th field is the filename with absolute path.

.. include:: footer.txt
