import os

def usrProjPart( entity, ups ):
    """
    Given list of uids or pids (ups) and entity string ('uid' or 'xattrs')
    returns correponding query string for GUFI
    """
    tmp = list(map(lambda x: entity + ' = ' + str(x), ups))
    return '(' + " or ".join(tmp) + ')'

def periodToQry( entity, per ):
    """
    Given entity ('mtime', 'ctime' or 'atime') and period (list of
    1 or 2 integers, 2nd one less than the 1st in case of 2) returns
    query string on entity.
    """
    ge  = '>='; le  = '<=';
    wpq = []
    if not per[0] == -1:
       wpq.append(entity + ' ' + ge + ' ' + str(per[0]))
    if not per[1] == -1:
       wpq.append(entity + ' ' + le + ' ' + str(per[1]))
    return '(' + " and ".join(wpq) + ')'

def getQryStr( uids, pids, wp, wpname, rp, fields ):
    """ 
    Generate the query string for gufi_query given constraints of
     1. uids (restricting to the list of uids)
     2. pids (restricting to the list of pids)
     3. wp (restricting to the period during 
            which files were last written)
     4. rp (restrict to the period during
            which files were last read)
    fields are the list of columns to be extracted
    wpname can be 'mtime' (POSIX FS) or 'ctime' (HPSS)
    """ 
    sqt = '\''
    beg = 'SELECT ' + ','.join(fields) + ' FROM entries '
    if bool(uids) or bool(pids) or bool(wp) or bool(rp):
       totcons = []
       if bool(uids):
          totcons.append( usrProjPart( 'uid', uids ) )
       if bool(pids):
          totcons.append( usrProjPart( 'xattrs', pids ) )
       if bool(wp):
          totcons.append( periodToQry( wpname, wp ) )
       if bool(rp):
          totcons.append( periodToQry( 'atime', rp ) )
       totconsstr = "WHERE " + " and ".join(totcons)
       return sqt + beg + totconsstr + ';' + sqt
    else: 
       return sqt + beg + ';' + sqt

def setFields(  wpname ):
    """
    Translates fields to GUFI-speak, 
    sets defaults for grprt otherwise
    """
    if wpname == 'ctime':
       return ['size','uid',wpname,'atime','xattrs','name','path()']
    else:
       return ['size','uid',wpname,'atime','name','path()']

def getOutputFilename( cachedir, gufitree, remove=True ):
    """
    Returns full path of output filenames and creates the
    destination directory if not already present
    """
    wdir = os.path.join(cachedir, os.path.dirname( gufitree[8:] )) 
    basn = '__.' + os.path.basename( gufitree )
    filen = os.path.join( wdir, basn ) + '.dat'
    if not os.path.exists(wdir):
       os.system('mkdir -p ' + wdir)
    if remove:
       os.system('rm -f ' + filen + '.*')
    return filen

def getGufiQryCmd( uids, pids, wp, wpname, rp, cachedir, nthreads, gufitree ):
    """
    Given all the arguments above returns the gufi command to be
    executed in GUFI server.
    """
    fields = setFields( wpname )
    cmd = 'gufi_query'
    opts = '-P -p -e 1'
    delimopt = '-d x'
    nts = '-n ' + str(nthreads)
    filen = getOutputFilename( cachedir, gufitree )
    filopt = '-o ' + filen
    qry = getQryStr( uids, pids, wp, wpname, rp, fields )
    qryopt = '-E ' + qry
    fullcmd = ' '.join([cmd, opts, delimopt, nts, filopt, qryopt, gufitree])
    return fullcmd
