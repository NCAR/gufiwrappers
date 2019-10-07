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


def dataByUid( ref, size, uid, mtime, atime, proj, fname, path ):
   """
   """
   if atime < mtime:
      atime = mtime
   if uid not in ref:
      ref[uid] = {'size': 0.0, 'count': 0, 
                  'wHist': np.zeros(MAXHBINS), 
                  'rHist': np.zeros(MAXHBINS)} 
   entry = ref[uid]
   entry['size'] += size
   entry['count'] += 1
   whidx = tsToYrMnIdx( mtime )
   rhidx = tsToYrMnIdx( atime )
   entry['wHist'][whidx] += size
   entry['rHist'][rhidx] += size

def conCatDataByUid( resfromtasks ):
   totres = resfromtasks[0]
   for ent in resfromtasks[1:]:
      for uid in ent.keys():
         entuid = ent[uid]
         if uid in totres:
            tot = totres[uid]
            tot['size'] += entuid['size']
            tot['count'] += entuid['count']
            tot['wHist'] += entuid['wHist']
            tot['rHist'] += entuid['rHist']
         else:
            totres[uid] = entuid
   for uid in totres.keys():
      tot = totres[uid]
      tot['wHist'] /= tot['size']
      tot['rHist'] /= tot['size']
   return totres

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
         
def displayDataByUid( results, nh ):
   global uid2uname
   uids = sorted(results.items(), key=lambda kv: kv[1]['size'], reverse=True)
   prtOneCharLine( "=", (43+nh*6) )
   totsz = 0.0
   totct = 0
   for uid, vals in uids:
      totsz += float(vals['size'])
      totct += 1
   print("%34s %40s" % ("","(Write / Read) stats over yymm"))
   print("%-8s " % "Unm/id", end=" ")
   print("%9s " % "Size(TB)", end=" ")
   print("%5s " % "%-age", end=" ")
   print("%5s " % "Cum-%", end=" ")
   print("%5s  " % "Count", end=" ")
   for i in range(nh):
      f = 100.0*float(i+1)/nh
      print("%4.1f " % f, end=" ")
   print( )
   prtOneCharLine( "-", (43+nh*6) )
   cumperc = 0.0
   for uid, vals in uids:
      sizetb = float(vals['size'])/float(10.**12)
      perc = 100.0*float(vals['size'])/totsz
      cumperc += perc
      if uid in uid2uname:
         uname = uid2uname[uid]
      else:
         uname = str(uid)
      print("%-8s " % uname, end=" ")
      print("%9.3e " % sizetb, end=" ")
      print("%5.1f " % perc, end=" ")
      print("%5.1f " % cumperc, end=" ")
      print("%7.1e " % float(vals['count']), end=" " )
      whist = getDsplyIdx( vals['wHist'], nh )
      rhist = getDsplyIdx( vals['rHist'], nh )
      for ent in whist:
         print("%4s " % ent, end=" ")
      print( )
      print("%43s" % "", end=" ")
      for ent in rhist:
         print("%4s " % ent, end=" ")
      print( )


def getDataByUid(np, cfiles ):
   global activefunc
   activefunc = dataByUid
   p = Pool(np)
   resfromtasks = p.map(parseNfill, cfiles)
   p.close()
   p.join()
   return conCatDataByUid( resfromtasks )

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

tree = args.tree
cachedir = args.cd
cfiles = args.cache_files
ncores = int(args.ncores)
nsbins = int(args.nsbins)
passwdfile = args.passwdfile
projmapfile = args.projmapfile

uidToUname( passwdfile )
xattrsToProjname( projmapfile )
res = getDataByUid(ncores, cfiles )
displayDataByUid( res, nsbins )
