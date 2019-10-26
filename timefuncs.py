
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


def procPeriod( perstr ):
    from datetime import datetime
    if perstr == None:
       return []
    lst = perstr.split('-')
    mn = 1; day = 1;
    lstn = []
    for e in lst:
       if len(e) > 0:
          yr = int(e[:4])
          if len(e) > 4:
             mn = int(e[4:6])
             if len(e) > 6:
                day = int(e[6:8])
          en = datetime(yr, mn, day).timestamp()
          lstn.append(en)
    return lstn

