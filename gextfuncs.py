
uid2uname = {}
uname2uid = {}

def getLatestHpssFile( fname ):
   """
   finds /etc/passwd and latest hpss dumps
   """
   import subprocess
   findcmd = ['find', '/gpfs/u/hpssusrs/HPSS', '-maxdepth', '2', '-name', fname]
   p1 = subprocess.Popen(findcmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
   out, err = p1.communicate()
   allfiles = []
   for ent in out.decode('utf-8').splitlines():
      allfiles.append(ent)
   p2 = subprocess.Popen(['ls', '-t'] + allfiles, stdout=subprocess.PIPE, 
             stderr=subprocess.PIPE)
   out, err = p2.communicate()
   for ent in out.decode('utf-8').splitlines():
      return ent


def fillUidUnameTable( fname ):
   """
   In case the maps are empty this is called to fill in the map
   between uid and uname either ways.
   """
   global uid2uname, uname2uid
   hpsspwdfile = getLatestHpssFile( fname )
   for pwdfile in ['/etc/passwd', getLatestHpssFile( 'passwd' )]:
      with open( pwdfile ) as fl:
          for line in fl:
              tmp = line.split(':')
              uid = int(tmp[2])
              uname = tmp[0]
              uid2uname[uid] = uname
              uname2uid[uname] = uid


def getUname( uid ):
   if not bool(uname2uid):
      fillUidUnameTable( 'passwd' )
   if uid in uid2uname:
      return uid2uname[uid]
   else:
      return uid


def getUid( uname ):
   if not bool(uid2uname):
      fillUidUnameTable( 'passwd' )
   if uname in uname2uid:
      return uname2uid[uname]
   else:
      return uname


pid2pname = {}
pname2pid = {}

def fillPidPnameTable( fname ):
   """
   In case the maps are empty this is called to fill in the map
   between uid and uname either ways.
   """
   global pid2pname, pname2pid
   with open( getLatestHpssFile( fname ) ) as fl:
      for line in fl:
         tmp = line.split(':')
         if len(tmp) == 5:
            pid = int(tmp[2])
            pname = tmp[3]
         else:
            pid = int(tmp[1])
            pname = tmp[2]
         pid2pname[pid] = pname
         pname2pid[pname] = pid



def getPname( pid ):
   if not bool(pname2pid):
      fillPidPnameTable( 'accounts' )
   if pid in pid2pname:
      return pid2pname[pid]
   else:
      return pid


def getPid( pname ):
   if not bool(pid2pname):
      fillPidPnameTable( 'accounts' )
   if pname in pname2pid:
      return pname2pid[pname]
   else:
      return pname


def fsnameToSearch( fsname ):
   if fsname.startswith('/gpfs/csfs1'):
      return '/search/campaign' + fsname[11:]
   elif fsname.startswith('/gpfs/fs1/p'):
      return '/search/p' + fsname[11:]
   elif fsname.startswith('/glade/p'):
      return '/search/p' + fsname[8:]
   else:
      return '/search/hpss' + fsname

def searchToFsname( sname ):
   if sname.startswith('/search/campaign'):
      return '/gpfs/csfs1' + sname[16:]
   elif sname.startswith('/search/p'):
      return '/glade/p' + sname[9:]
   else:
      return sname[12:]


