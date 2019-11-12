import timefuncs as tm
import gmapfuncs as gm

def prtOneCharLine( char, n, repfh ):
   for i in range(n):
      print("%1s" % char, end="", file=repfh)
   print(file=repfh)

def displayHeaders( nh, keyid, basedir, repfh ):
   """
   Given display key prints the headers
   """
   prtOneCharLine( "=", (43+nh*6), repfh )
   print(" Base directory for this report: %s" % gm.searchToFsName(basedir), file=repfh)
   print("%34s %40s" % ("","% (Write / Read) stats over yymm"), file=repfh)
   print("%9s " % "Size(TB)", end=" ", file=repfh)
   print("%5s " % "%-age", end=" ", file=repfh)
   print("%5s " % "Cum-%", end=" ", file=repfh)
   print("%-9s  " % "Count", end=" ", file=repfh)
   for i in range(nh):
      f = 100.0*float(i+1)/nh
      print("%4.1f " % f, end=" ", file=repfh)
   print("%-8s " % keyid, file=repfh)
   prtOneCharLine( "-", (43+nh*6), repfh )

def displayRow( keyid, uid, row, totrow, cumperc, nh, repfh ): 
   """
   Display each row
   """
   perc = 100.0*float(row['size'])/float(totrow['size'])
   cumperc += perc
   sizetb = float(row['size'])/float(10.**12)
   print("%9.3e " % sizetb, end=" ", file=repfh)
   print("%5.1f " % perc, end=" ", file=repfh)
   print("%5.1f " % cumperc, end=" ", file=repfh)
   print("%7.1e " % float(row['count']), end=" ", file=repfh )
   print("%2s" % "W:", end=" ", file=repfh)
   whist = tm.getDsplyIdx( row['wHist'], row['size'], nh )
   rhist = tm.getDsplyIdx( row['rHist'], row['size'], nh )
   for ent in whist:
      print("%4s " % ent, end=" ", file=repfh)
   if keyid == "Uname/Uids":
      keyname = gm.getUname( uid )
   elif keyid == "Projs":
      keyname = gm.getPname( uid )
   else:
      keyname = uid
   print("%-s " % keyname, file=repfh)
   print("%33s" % "", end=" ", file=repfh)
   print("%2s" % "R:", end=" ", file=repfh)
   for ent in rhist:
      print("%4s " % ent, end=" ", file=repfh)
   print( file=repfh)
   return cumperc


def displayDataByKey( results, totrow, basedir, nh, keyid, repfh ):
   global uid2uname
   displayHeaders( nh, keyid, basedir, repfh )
   uids = sorted(results.items(), key=lambda kv: kv[1]['size'], reverse=True)
   cumperc = 0.0
   displayRow( keyid, "Total", totrow, totrow, cumperc, nh, repfh )
   prtOneCharLine( "-", (43+nh*6), repfh )
   for uid, row in uids:
      cumperc = displayRow( keyid, uid, row, totrow, cumperc, nh, repfh )


def dumpHistByKey( results, keyid, fname ):
   """
   Dump the histogram data mostly for plotting
   """
   import builddb as bdb
   import numpy as np
   import pandas as pd
   dtarry = []
   for i in range(bdb.MAXHBINS):
      dtarry.append(tm.idxToYrMnStr(i, '%Y-%m' ))
   dtcol = np.array(dtarry)
   allhist = pd.DataFrame( {'Year-mon': dtcol} ) 
   uids = sorted(results.items(), key=lambda kv: kv[1]['size'], reverse=True)
   for uid, row in uids:
      if keyid == "Uname/Uids":
         keyname = gm.getUname( uid )
      elif keyid == "Projs":
         keyname = gm.getPname( uid )
      else:
         keyname = uid
      headw = keyname + '_w'
      headr = keyname + '_r'
      tmpdf = pd.DataFrame( {headw: row['wHist'], headr: row['rHist']} )
      allhist = pd.concat([allhist,tmpdf],axis=1)
   allhist.to_csv( fname )
