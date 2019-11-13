
def getProcFilename( gufitmp, ftype ):
    """
    returns data-time attached script-filename
    """
    import timefuncs as tm
    import os
#   from datetime import datetime
#   ts = datetime.fromtimestamp(time.time()).strftime('%Y%m%d_%H%M%S')
    ts = tm.getTsForFname( )
    if ftype == 'script':
       fn = ftype[:3] + '_' + ts + '.sh'
       wdir = os.path.join(gufitmp, 'scripts')
    elif ftype == 'report':
       fn = ftype[:3] + '_' + ts + '.dat'
       wdir = os.path.join(gufitmp, 'reports')
    elif ftype == 'hist':
       fn = ftype[:3] + '_' + ts + '.csv'
       wdir = os.path.join(gufitmp, 'reports')
    else:
       fn = ftype[:3] + '_' + ts + '.log'
       wdir = os.path.join(gufitmp, 'logs')
    if not os.path.exists(wdir):
       os.system('mkdir -p ' + wdir)
    fullfn = os.path.join(wdir, fn )
    return fullfn, wdir


