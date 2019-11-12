import numpy as np
import timefuncs as tm

fuidpid = []


def largestMatch( x, y ):
   minlxy = min(len(x),len(y))
   for i in range(minlxy):
      if x[i] != y[i]:
         return y[:i]
   return x[:minlxy]

def parseNfill( fl ):
   """
   Core function scheduled / map using multiprocessing module
   """
   import sys
   global activefunc, prefixdir, fuidpid
   if len(prefixdir) > 1:
      basedir = prefixdir
   else:
      basedir = ''
   ref = {}
   with open(fl, encoding = "ISO-8859-1") as fh:
      l = 0
      for line in fh:
         tmp = line.split('\x1E')
         try:
            size = int(tmp[0]); uid = int(tmp[1]); mtime = int(tmp[2]);
            atime = int(tmp[3]); 
            if len(tmp[4]) > 0:
               proj = int(tmp[4])
            else:
               proj = 0
            fname = tmp[5]; path = tmp[6];
            if atime < mtime:
               atime = mtime
            if not bool(fuidpid) or uid in fuidpid or proj in fuidpid:
               if len(prefixdir) == 1:
                  if len(basedir) == 0:
                     basedir = path
                  else:
                     basedir = largestMatch( basedir, path )
                  activefunc( ref, size, uid, mtime, atime, proj, fname, path )
               else:
                  if path.startswith(prefixdir):
                     basedir = largestMatch( basedir, path )
                     activefunc( ref, size, uid, mtime, atime, proj, fname, path )
         except:
            print("Discarded line:",l,"from: ",fl,"line: ",tmp, file=sys.stderr)
         l += 1
   return ref, basedir


def crEntry( ):
   """
   returns an initialized empty row
   """
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
   whidx = tm.tsToYrMnIdx( mtime )
   rhidx = tm.tsToYrMnIdx( atime )
   entry['wHist'][whidx] += size
   entry['rHist'][rhidx] += size

def dataByUids( ref, size, uid, mtime, atime, proj, fname, path ):
   """
   Function for storing rows per uid
   """
   global basedir, basedirlen
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
   global prefixdir
   lpref = len(prefixdir)
   tmp = path[lpref+1:].split('/')
   fillkey = tmp[0]
   fillData( ref, size, fillkey, mtime, atime, proj, fname, path )

def conCatDataByKey( resfromtasks ):
   """
   Gathers all the data from all multiprocessing tasks and sums those
   to that of task-0
   """
   totres, basedir = resfromtasks[0]
   for ent, tmpbasedir in resfromtasks[1:]:
      if len(ent) > 0:
         basedir = largestMatch( basedir, tmpbasedir )
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
   return totres, totrow, basedir



def getDataByFields(np, databyfields, cfiles ):
   from multiprocessing import Pool
   global activefunc
   activefunc = databyfields
   p = Pool(np)
   resfromtasks = p.map(parseNfill, cfiles)
   p.close()
   p.join()
   return conCatDataByKey( resfromtasks )


