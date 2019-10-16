import timefuncs as tm
import gmapfuncs as gm

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
   whist = tm.getDsplyIdx( row['wHist'], nh )
   rhist = tm.getDsplyIdx( row['rHist'], nh )
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



