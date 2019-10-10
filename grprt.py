#!/usr/bin/env python

import os
import argparse
import numpy as np
from multiprocessing import Pool
from datetime import datetime
import time

MAXHBINS = 1024  # Maximum histogram bins
# size,uid,mtime,atime,xattrs,name,path() for HPSS mtime is replaced by ctime
xattrs2proj = {}
uid2uname = {}
prefixdir = '/'

def dataByDir( size, uid, mtime, atime, proj, fname, path ):
   """
   """

def uidToUname( passwdfile ):
   """
   This is for reporting purpose to create table between user-name
   and uid.
   """
   global uid2uname
   if passwdfile is None:
      return
   else:
      with open( passwdfile ) as fl:
          for line in fl:
              tmp = line.split(':')
              uid = int(tmp[2])
              uname = tmp[0]
              uid2uname[uid] = uname    

def qryUidToUname( uid ):
   if uid in uid2uname:
      return uid2uname[uid]
   else:
      return str(uid)


def xattrsToProjname( projmap ):
   """
   This is for reporting purpose to create table between proj-name
   and proj id in HPSS.
   """
   global xattrs2proj
   if projmap is None:
      return
   else:
      with open( projmap ) as fl:
          for line in fl:
              tmp = line.split(':')
              projid = int(tmp[-3])
              projname = tmp[-2]
              xattrs2proj[projid] = projname    

def qryProjidToProjname( projid ):
   if projid in xattrs2proj:
      return xattrs2proj[projid]
   else:
      return str(projid)

def parseNfill( fl ):
   """
   Core function scheduled / map using multiprocessing module
   """
   global activefunc
   ref = {}
   with open(fl) as fh:
      for line in fh:
         tmp = line.split('\x1E')
         try:
            size = int(tmp[0]); uid = int(tmp[1]); mtime = int(tmp[2]); 
            atime = int(tmp[3]); proj = int(tmp[4]); fname = tmp[5]; path = tmp[6];
            if atime < mtime:
               atime = mtime
            activefunc( ref, size, uid, mtime, atime, proj, fname, path )
         except:
            print(fl)
            exit(-1)
   return ref


def tsToYrMnIdx( tme ):
   """returns yr month index from unix time"""
   yr, mn = datetime.fromtimestamp(tme).strftime('%Y,%m').split(',')
   yr = int(yr)
   mn = int(mn)
   return (yr - 1970)*12 + (mn - 1)

def yrMnIdxToTs( idx ):
   """Generates Unix time stamp from month inde since 01/01/1970"""
   yr = int( idx / 12 )
   mn = (idx - 12*yr)
   return datetime((1970 + yr), (1 + mn), 1).timestamp()
   
def idxToYrMnStr( idx ):
   """Generates the yymm string from index"""
   ts = yrMnIdxToTs( idx )
   return datetime.fromtimestamp(ts).strftime('%y%m')


def crEntry( ):
   """returns an initialized empty row"""
   return {'size': 0.0, 'count': 0, 
           'wHist': np.zeros(MAXHBINS), 
           'rHist': np.zeros(MAXHBINS)} 

def fillData( ref, size, uid, mtime, atime, proj, fname, path ):
   """
   """
   if uid not in ref:
      ref[uid] = crEntry( )
   entry = ref[uid]
   entry['size'] += size
   entry['count'] += 1
   whidx = tsToYrMnIdx( mtime )
   rhidx = tsToYrMnIdx( atime )
   entry['wHist'][whidx] += size
   entry['rHist'][rhidx] += size

def dataByUids( ref, size, uid, mtime, atime, proj, fname, path ):
   """
   Function for storing rows per uid
   """
   fillData( ref, size, uid, mtime, atime, proj, fname, path )

def dataByProjs( ref, size, uid, mtime, atime, proj, fname, path ):
   """
   Function for storing rows per projects
   """
   fillData( ref, size, proj, mtime, atime, proj, fname, path )

def dataBySubdirs( ref, size, uid, mtime, atime, proj, fname, path ):
   """
   Function for storing rows per subdirs
   """
   global prefixdir
   if path.startswith(prefixdir):
      lpref = len(prefixdir)
      tmp = path[lpref+1:].split('/')
      fillkey = tmp[0]
      fillData( ref, size, fillkey, mtime, atime, proj, fname, path )

def conCatDataByKey( resfromtasks ):
   """
   Gathers all the data from all multiprocessing tasks and sums those
   to that of task-0
   """
   totres = resfromtasks[0]
   for ent in resfromtasks[1:]:
      for key in ent.keys():
         entuid = ent[key]
         if key in totres:
            tot = totres[key]
            for attr in tot.keys():
               tot[attr] += entuid[attr]
         else:
            totres[key] = entuid
   ct = 0
   totrow = crEntry( )
   for key in totres.keys():
      tot = totres[key]
      tot['wHist'] /= tot['size']
      tot['rHist'] /= tot['size']
      for attr in tot.keys():
          totrow[attr] += tot[attr]
      ct += 1
   totrow['wHist'] /= ct
   totrow['rHist'] /= ct
   return totres, totrow

def getDsplyIdx( hist, nh ):
   """ Returns an array of nh yrmn entries """
   frac = 10.**(-6)
   idxlst = []
   totf = 0.0
   for i in range(len(hist)):
      totf += hist[i] 
      while totf > frac:
         idxlst.append( idxToYrMnStr( i ))
         frac += 1./nh
   return idxlst

def prtOneCharLine( char, n ):
   for i in range(n):
      print("%1s" % char, end="")
   print( )
         
def displayHeaders( nh, keyid ):
   """
   Given display key prints the headers
   """
   prtOneCharLine( "=", (43+nh*6) )
   print("%34s %40s" % ("","% (Write / Read) stats over yymm"))
   print("%9s " % "Size(TB)", end=" ")
   print("%5s " % "%-age", end=" ")
   print("%5s " % "Cum-%", end=" ")
   print("%5s  " % "Count", end=" ")
   for i in range(nh):
      f = 100.0*float(i+1)/nh
      print("%4.1f " % f, end=" ")
   print("%-8s " % keyid)
   prtOneCharLine( "-", (43+nh*6) )


def displayRow( keyid, uid, row, totrow, cumperc, nh ): 
   """
   Display each row
   """
   perc = 100.0*float(row['size'])/float(totrow['size'])
   cumperc += perc
   sizetb = float(row['size'])/float(10.**12)
   print("%9.3e " % sizetb, end=" ")
   print("%5.1f " % perc, end=" ")
   print("%5.1f " % cumperc, end=" ")
   print("%7.1e " % float(row['count']), end=" " )
   whist = getDsplyIdx( row['wHist'], nh )
   rhist = getDsplyIdx( row['rHist'], nh )
   for ent in whist:
      print("%4s " % ent, end=" ")
   if keyid == "Uname/Uids":
      keyname = qryUidToUname( uid )
   elif keyid == "Projs":
      keyname = qryProjidToProjname( uid )
   else:
      keyname = uid
   print("%-s " % keyname)
   print("%33s" % "", end=" ")
   for ent in rhist:
      print("%4s " % ent, end=" ")
   print( )
   return cumperc

def displayDataByKey( results, totrow, nh, keyid ):
   global uid2uname
   displayHeaders( nh, keyid )
   uids = sorted(results.items(), key=lambda kv: kv[1]['size'], reverse=True)
   cumperc = 0.0
   displayRow( keyid, "Total", totrow, totrow, cumperc, nh )
   for uid, row in uids:
      cumperc = displayRow( keyid, uid, row, totrow, cumperc, nh )


def getDataByFields(np, databyfields, cfiles ):
   global activefunc
   activefunc = databyfields
   p = Pool(np)
   resfromtasks = p.map(parseNfill, cfiles)
   p.close()
   p.join()
   return conCatDataByKey( resfromtasks )

defcachepref = os.path.join('/gpfs/fs1/scratch', os.environ['LOGNAME'], 'gufi_cache')

parser = argparse.ArgumentParser(description='Cache tree DB for finegrain queries')
parser.add_argument('-cd', '--cache-dir', dest='cd', default=defcachepref)
parser.add_argument('-n', '--ncores', dest='ncores', default=1, help='Number of cores / threads to run')
parser.add_argument('--nsbins', dest='nsbins', default=8, help='Number of write / read stat bins')
parser.add_argument('-d', '--tree', dest='tree', help='Directory against which to launch the query')
parser.add_argument('--passwdfile', dest='passwdfile', help='passwd file')
parser.add_argument('--projmapfile', dest='projmapfile', help='projmap file')
parser.add_argument(dest='cache_files', nargs='+',  help='All cache files generated by gext_cache')
args = parser.parse_args()

prefixdir = args.tree
cachedir = args.cd
cfiles = args.cache_files
ncores = int(args.ncores)
nsbins = int(args.nsbins)
passwdfile = args.passwdfile
projmapfile = args.projmapfile

uidToUname( passwdfile )
xattrsToProjname( projmapfile )

res, total = getDataByFields(ncores, dataByUids, cfiles )
displayDataByKey( res, total, nsbins, "Uname/Uids" )

#res = getDataByFields(ncores, dataByProjs, cfiles )
#displayDataByKey( res, nsbins, "Projs" )

#res = getDataByFields(ncores, dataBySubdirs, cfiles )
#displayDataByKey( res, nsbins, "Subdirs" )
