__author__ = "mlklm"
__date__ = "$30 juil. 2015 09:59:26$"

__NS__ = "AEFS"

import os
import random
import re
from simplecrypt import decrypt
from simplecrypt import encrypt
import uuid

class myfile:
    
    def __init__(self):
        self.base_path = os.path.dirname(__file__) + "/uploads/"

    def write_(self, type, filename, data):
        path = self.filename2path(filename)
        f = open(path, type)
        f.write(data)
        f.close()
        
    def read_(self, type, filename):
        path = self.filename2path(filename)
        data = open(path, type)
        return data.read()
    
    def delete(self, filename):
        path = self.filename2path(filename)
        os.remove(path);
    
    def filename2path(self, filename):
        auuid = re.split('\-', filename)
        loc = auuid[0][0:4] + "/" + auuid[0][4:8] + "/"
        self.check_dir(self.base_path + loc)
        return self.base_path + loc + filename
    
    def check_dir(self, dirname):
        if not os.path.exists(dirname):
            os.makedirs(dirname)
    
    def set_mime(self, mime):
        self.mime = mime
    
    def generate_name(self):
        fid = str(uuid.uuid4())
        if len(self.mime) > 0: 
            self.name = fid + self.mime
        else:
            self.name = fid + ".txt"
        
        return self.name

    def encrypt(self, pp, data):
        self.key = ''.join([random.choice('0123456789ABCDEF') for x in range(16)])
        data = encrypt((self.key + "&" + __NS__ + "&" + pp), data)
        return data
      
    def decrypt(self, pp, key, data):
        data = decrypt((key + "&" + __NS__ + "&" + pp), data)
        return data    
        
    def get_file_name(self):
        return self.name
    
    def get_file_key(self):
        return self.key
    