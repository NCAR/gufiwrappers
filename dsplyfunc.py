import timefuncs as tm
import gmapfuncs as gm

def prtOneCharLine( char, n ):
   for i in range(n):
      print("%1s" % char, end="")
   print( )

def displayHeaders( nh, keyid, basedir ):
   """
   Given display key prints the headers
   """
   prtOneCharLine( "=", (43+nh*6) )
   print(" Base directory for this report: %s" % gm.searchToFsName(basedir))
   print("%34s %40s" % ("","% (Write / Read) stats over yymm"))
   print("%9s " % "Size(TB)", end=" ")
   print("%5s " % "%-age", end=" ")
   print("%5s " % "Cum-%", end=" ")
   print("%-9s  " % "Count", end=" ")
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
   print("%2s" % "W:", end=" ")
   whist = tm.getDsplyIdx( row['wHist'], row['size'], nh )
   rhist = tm.getDsplyIdx( row['rHist'], row['size'], nh )
   for ent in whist:
      print("%4s " % ent, end=" ")
   if keyid == "Uname/Uids":
      keyname = gm.getUname( uid )
   elif keyid == "Projs":
      keyname = gm.getPname( uid )
   else:
      keyname = uid
   print("%-s " % keyname)
   print("%33s" % "", end=" ")
   print("%2s" % "R:", end=" ")
   for ent in rhist:
      print("%4s " % ent, end=" ")
   print( )
   return cumperc


def displayDataByKey( results, totrow, basedir, nh, keyid ):
   global uid2uname
   displayHeaders( nh, keyid, basedir )
   uids = sorted(results.items(), key=lambda kv: kv[1]['size'], reverse=True)
   cumperc = 0.0
   displayRow( keyid, "Total", totrow, totrow, cumperc, nh )
   prtOneCharLine( "-", (43+nh*6) )
   for uid, row in uids:
      cumperc = displayRow( keyid, uid, row, totrow, cumperc, nh )


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
