import numpy as np
import timefuncs as tm
import re
import time

fuidpid = []
fwp = []
frp = []
basedirdepth = 0

def fixWpRpList( ):
   global fwp, frp
   if bool(fwp):
      if fwp[0] == -1:
         fwp = 0
      if fwp[1] == -1:
         fwp = time.time()
   if bool(frp):
      if frp[0] == -1:
         frp = 0
      if frp[1] == -1:
         frp = time.time()


def largestMatch( x, y ):
   minlxy = min(len(x),len(y))
   if minlxy == 0:
      return y
   for i in range(minlxy):
      if x[i] != y[i]:
         return y[:i]
   return x[:minlxy]

def parseNfill( fl ):
   """
   Core function scheduled / map using multiprocessing module
   """
   import sys
   global activefunc, fuidpid, fwp, frp
   ref = {}
   with open(fl, encoding = "ISO-8859-1") as fh:
      l = 0
      for line in fh:
         tmp = line.split('\x1E')
         try:
            size = int(tmp[0]); uid = int(tmp[1]); mtime = int(tmp[2]);
            atime = int(tmp[3]); 
            if len(tmp) == 8:
               proj = int(tmp[4])
               fname = tmp[5]; path = tmp[6];
            else:
               proj = 0
               fname = tmp[4]; path = tmp[5];
            path = re.sub('/{2,}', '/', path)
            if atime < mtime:
               atime = mtime
            if bool(fwp) and (mtime < fwp[0] or mtime > fwp[1]):
               continue
            if bool(frp) and (atime < frp[0] or atime > frp[1]):
               continue
            if not bool(fuidpid) or uid in fuidpid or proj in fuidpid:
               activefunc( ref, size, uid, mtime, atime, proj, fname, path )
         except:
            print("Discarded line:",l,"from: ",fl,"line: ",tmp, file=sys.stderr)
         l += 1
   return ref


def crEntry( ):
   """
   returns an initialized empty row
   """
   return {'size': 0.0, 'count': 0,
           'wHist': np.zeros(MAXHBINS),
           'rHist': np.zeros(MAXHBINS),
           'rMinw': np.zeros(MAXHBINS)}


def fillData( ref, size, uid, mtime, atime, proj, fname, path ):
   """
   """
   if uid not in ref:
      ref[uid] = crEntry( )
   entry = ref[uid]
   entry['size'] += size
   entry['count'] += 1
   whidx = tm.tsToYrMnIdx( mtime )
   rhidx = tm.tsToYrMnIdx( atime )
   entry['wHist'][whidx] += size
   entry['rHist'][rhidx] += size
   entry['rMinw'][rhidx-whidx] += size

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


def dataBySubDirs( ref, size, uid, mtime, atime, proj, fname, path ):
   """
   Function for storing rows per subdirs
   """
   paths = path.split('/')
   if len(paths) <= gufitreedepth:
      fillkey = '.'
   else:
      fillkey = paths[gufitreedepth]
   fillData( ref, size, fillkey, mtime, atime, proj, fname, path )

def conCatDataByKey( resfromtasks ):
   """
   Gathers all the data from all multiprocessing tasks and sums those
   to that of task-0
   """
   totres = resfromtasks[0]
   for ent in resfromtasks[1:]:
      if len(ent) > 0:
         for key in ent.keys():
            entuid = ent[key]
            if key in totres:
               tot = totres[key]
               for attr in tot.keys():
                  tot[attr] += entuid[attr]
            else:
               totres[key] = entuid
   totrow = crEntry( )
   for key in totres.keys():
      tot = totres[key]
      for attr in tot.keys():
          totrow[attr] += tot[attr]
   return totres, totrow

def getDirDepth( path ):
   """
   Returns depth of path
   """
   path = re.sub('/{2,}', '/', path)
   if path.endswith('/'):
      path = path[:-1]
   return len(path.split('/'))


def getDataByFields(gufitree, np, databyfields, cfiles ):
   from multiprocessing import Pool
   global activefunc, gufitreedepth
   gufitreedepth = getDirDepth( gufitree )
   activefunc = databyfields
   p = Pool(np)
   resfromtasks = p.map(parseNfill, cfiles)
   p.close()
   p.join()
   return conCatDataByKey( resfromtasks )
