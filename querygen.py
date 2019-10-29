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
    if len(per) >= 1:
       wpq.append(entity + ' ' + le + ' ' + str(per[0]))
    if len(per) == 2:
       wpq.append(entity + ' ' + ge + ' ' + str(per[1]))
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
    if bool(usrs) or bool(projs) or bool(wp) or bool(rp):
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


