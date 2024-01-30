from cryptography.fernet import Fernet
import os
import json
import base64
import subprocess
import shlex

def command_run(cmd, verbose = False, *args, **kwargs):
    process = subprocess.Popen(
        cmd,
        stdout = subprocess.PIPE,
        stderr = subprocess.PIPE,
        text = True,
        shell = False
    )
    std_out, std_err = process.communicate()
    if verbose:
        print(std_out.strip(), std_err)
    return std_out
  

# Method to generate key for encryption and decryption. 
def get_key():
   
    if 'nt' in os.name:
        # key= str(subprocess.check_output('wmic csproduct get uuid'), 'utf-8').split('\n')[1].strip()
        key = command_run('wmic csproduct get uuid')
    else:
        key= command_run('cat /etc/machine-id')

    key=key[:32]
    key=key.encode()
    key=base64.urlsafe_b64encode(key)
    return key
   
# Method to encrypt data.
def json_encrypt(dbInfo):
    
    key= get_key()
    f = Fernet(key)
    encrypted = f.encrypt(dbInfo.encode('UTF-8'))
    return encrypted
    
# Method to decrypt data.
def json_decrypt(encrypted):
    
    key=get_key()
    f = Fernet(key)
    decrypted = f.decrypt(encrypted)
    return decrypted.decode('UTF-8')
