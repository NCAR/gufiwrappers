def getQryStr( usrs, projs, wp, rp, prefname, fields ):
    """ 
    Generate the query string for gufi_query given constraints of
     1. usrs (restricting to the list of users)
     2. projs (restricting to the list of projs)
     3. wp (restricting to the period during 
            which files were last written)
     4. rp (restrict to the period during
            which files were last read)
    fields are the list of columns to be extracted
    """ 
    sqt = '\''
    dqt = '\"'
    beg = 'SELECT ' + ','.join(fields) + ' FROM entries; '
    if bool(usrs) or bool(projs) or bool(wp) or bool(rp):
       totcons = []
       if bool(usrs):
          eachusrq = list(map(lambda x: 'uid = ' + dqt + x + dqt, usrs))
          usrq = '(' + " or ".join(eachusrq) + ')'
          totcons.append(usrq)
       if bool(projs):
          eachprojsq = list(map(lambda x: 'xattrs = ' + dqt + x + dqt, projs))
          projsq = '(' + " or ".join(eachprojsq) + ')'
          totcons.append(projsq)
       totconsstr = "WHERE " + " and ".join(totcons)
       return sqt + beg + totconsstr + sqt 
    else: 
       return sqt + beg + sqt 


