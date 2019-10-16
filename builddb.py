
import numpy as np
import timefuncs as tm

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



def getDataByFields(np, databyfields, cfiles ):
   from multiprocessing import Pool
   global activefunc
   activefunc = databyfields
   p = Pool(np)
   resfromtasks = p.map(parseNfill, cfiles)
   p.close()
   p.join()
   return conCatDataByKey( resfromtasks )


