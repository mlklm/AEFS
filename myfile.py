__author__ = "mlklm"
__date__ = "$30 juil. 2015 09:59:26$"

import os
import re
class myfile:
    
    def __init__(self):
        self.base_path = os.path.dirname(__file__) + "/../uploads/"

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
    
