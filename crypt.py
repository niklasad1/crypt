
# usage python crypt.py {--encrypt|decrypt|} {--file|folder}

#!/usr/bin/env python
import sys
import gnupg
import os
import time
import platform
import codecs
from gnupg import GPG

def generate_random(chars):
  print ( codecs.encode ( os.urandom(int(chars)), 'hex') )

def find_gpg_keys():
  os_name =  platform.system().lower()
  gpg_dir = ""
  if ( os_name.startswith('linux') == True or os_name.startswith('darwin') == True):
    gpg_dir = os.path.expanduser('~') + '/.gnupg'
  elif ( os_name.startswith('windows') == True):
    gpg_dir = os.path.expanduser('~') + '\\AppData\\Roaming\gnupg'
  else:
    print 'ERROR OS not supported'
    sys.exit(1)
  if ( os.path.exists(gpg_dir + '/pubring.gpg')):
    return gpg_dir
  else:
    return ''

def encrypt(file):
  gpg_home = find_gpg_keys()
  if ( gpg_home == ''):
    print 'GPG keys not found'
    sys.exit(1)
  gpg = GPG(gnupghome=gpg_home, use_agent=True)
  public_keys = gpg.list_keys()
  key_id = public_keys[0]['keyid']

  if ( os.path.isfile(file)):
      if ( file.endswith('.gpg')):
        print file + ' is already encrypted'
      else:
        stream = open(file, "rb")
        status = gpg.encrypt_file(stream, key_id, passphrase='default_key', armor=False, always_trust=True,
                         output=file+'.gpg', symmetric=False)
        stream.close()
        if ( status.ok):
          os.remove(file)
          print file , ' successfully encrypted'
  elif (os.path.isdir(file)):
    for root, dirs, files in os.walk(file, topdown=True):
      for name in files:
        current_file = (os.path.join(root, name))
        if ( current_file.endswith('.gpg') ):
          print current_file + ' : is already encrypted'
        else:
          stream = open(current_file, "rb")
          status = gpg.encrypt_file(stream, key_id, armor=True, always_trust=True, symmetric=False, output=current_file+'.gpg')
          stream.close()
          if ( status.ok ):
            os.remove(current_file)
            print current_file + ' successfully encrypted'
  else:
    print 'ERROR, file or directory not found'

def decrypt(file):
  gpg_home = find_gpg_keys()
  if ( gpg_home == ''):
    print 'GPG keys not found'
    sys.exit(1)
  gpg = GPG(gnupghome=gpg_home, use_agent=True)
  public_keys = gpg.list_keys()
  key_id = public_keys[0]['keyid']
  if ( os.path.isfile(file)):
      if ( file.endswith('.gpg')):
        stream = open(file, 'rb')
        status = gpg.decrypt_file(stream, output=file[:-4])
        if ( status.ok):
          os.remove(file)
          print file[:-4] + ' succesfully decrypted'
      else:
        print file + ' not encrypted'
  elif ( os.path.isdir(file) ):
    for root, dirs, files in os.walk(file, topdown=True):
      for name in files:
        current_file = (os.path.join(root, name))
        if ( current_file.endswith('.gpg')):
          stream = open(current_file, "rb")
          status = gpg.decrypt_file(stream, output=current_file[:-4])
          if ( status.ok ):
            os.remove(current_file)
            print current_file[:-4] + ' successfully decrypted'
        else:
          print current_file + ' not encrypted'
  else:
    print 'ERROR: file or directory not found'

def main():
  operation = ""
  target = ""
  if len(sys.argv) != 3:
    print 'usage python crypt.py {encrypt|decrypt} {file|folder}'
    sys.exit(1)
  else:
    operation = sys.argv[1]
    target = sys.argv[2]

  print (operation + ' ' + target)
  if ( operation == 'encrypt'):
    encrypt(target)
  elif ( operation == 'decrypt'):
    decrypt(target)
  elif ( operation == 'random'):
    generate_random(target)
  else:
    print 'usage python crypt.py {encrypt|decrypt|random} {file|folder|size}'
    sys.exit(1)

if __name__ == "__main__":
  start_time = time.time()
  main()
  print("--- %s seconds ---" % (time.time() - start_time))
