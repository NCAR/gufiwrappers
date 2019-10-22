
def tsToYrMnIdx( tme ):
   """
   returns yr month index from unix time
   """
   from datetime import datetime
   yr, mn = datetime.fromtimestamp(tme).strftime('%Y,%m').split(',')
   yr = int(yr)
   mn = int(mn)
   return (yr - 1970)*12 + (mn - 1)

def yrMnIdxToTs( idx ):
   """
   Generates Unix time stamp from month inde since 01/01/1970
   """
   from datetime import datetime
   yr = int( idx / 12 )
   mn = (idx - 12*yr)
   return datetime((1970 + yr), (1 + mn), 1).timestamp()

def idxToYrMnStr( idx, fmt ):
   """Generates the yymm string from index"""
   from datetime import datetime
   ts = yrMnIdxToTs( idx )
   return datetime.fromtimestamp(ts).strftime( fmt )


def getDsplyIdx( hist, size, nh ):
   """ Returns an array of nh yrmn entries """
   frac = 10.**(-6)
   idxlst = []
   totf = 0.0
   for i in range(len(hist)):
      totf += (hist[i] / size)
      while totf > frac:
         idxlst.append( idxToYrMnStr( i, '%y%m' ))
         frac += 1./nh
   return idxlst
