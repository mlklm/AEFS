__author__ = "mlklm"
__date__ = "$30 juil. 2015 13:46:05$"

import time
import json
class metafile :
    
    def __init__(self,jsonstr=None):
        if jsonstr is not None :
            djson = json.loads(jsonstr)
            self.burnafterreading = djson['burnafterreading']
            self.expiration = djson['expiration']
            self.dateupload= djson['dateupload']
        else : 
            self.burnafterreading = False
            self.expiration = None
            self.dateupload = int(time.time())
        
    def set_expiration(self,expiration):
        if(expiration == "hour"):
            self.expiration = self.dateupload + 3600
        if(expiration == "day"):
            self.expiration = self.dateupload + 864000
        if(expiration == "week"):
            self.expiration = self.dateupload + 6048000
        if(expiration == "month"):
            self.expiration = self.dateupload + 25920000
        if(expiration == "year"):
            self.expiration = self.dateupload + 31536000
        if(expiration == "never"):
            self.expiration = -1
            
    def set_burnafterreading(self,burnafterreading):
        self.burnafterreading = burnafterreading
        
    def get_json_metafile(self):
        return json.dumps(self,default=lambda o: o.__dict__)
    
    def is_date_valid(self):
        return time.time() > self.expiration and self.expiration > 0
        
        
    def is_burafterreadingable(self):
        return self.burnafterreading == 1 