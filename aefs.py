__author__ = "mlklm"
__date__ = "$28 juil. 2015 11:35:31$"

from simplecrypt import decrypt
from simplecrypt import encrypt
from urllib.parse import urlparse
from myfile import myfile

import cgi
import codecs
import http.server
import json
import mimetypes
import random
import re
import time
import uuid

PORT = 1977

class MyHandler(http.server.BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.isBin = False
        content = self.content([])
        if self.isBin is True:
            self.send_bin(content)
        else: 
            self.send_html(content)

    def do_POST(self):
        # retrieve post data
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, environ={'REQUEST_METHOD':'POST', 'CONTENT_TYPE':self.headers['Content-Type']})
        # create file name
        amime = mimetypes.guess_all_extensions(form['fileToUpload'].headers['Content-Type'])
        fid = str(uuid.uuid4())
        # check file mime
        if len(amime) > 0: 
            fname = fid + amime[0]
        else:
            fname = fid + ".txt"
            
        # filemeta
        dfilemeta = {}
        if 'burnafterreading' in form:
            dfilemeta["burafterreading"] = 1
        dfilemeta["uploaddate"] = int(time.time())    
        if 'expiration' in form:    
            if(form['expiration'].value == "hour"):
                dfilemeta["expiration"] = dfilemeta["uploaddate"] + 3600
            if(form['expiration'].value == "day"):
                dfilemeta["expiration"] = dfilemeta["uploaddate"] + 864000
            if(form['expiration'].value == "week"):
                dfilemeta["expiration"] = dfilemeta["uploaddate"] + 6048000
            if(form['expiration'].value == "month"):
                dfilemeta["expiration"] = dfilemeta["uploaddate"] + 25920000
            if(form['expiration'].value == "year"):
                dfilemeta["expiration"] = dfilemeta["uploaddate"] + 31536000
            if(form['expiration'].value == "never"):
                dfilemeta["expiration"] = -1
        
        dfilemeta["uploaddate"] = int(time.time())
        jsonfilemeta = json.dumps(dfilemeta)
        # make keys
        key = ''.join([random.choice('0123456789ABCDEF') for x in range(16)])
        pp = form['passphrase'].value
        # bytes
        file = encrypt((key + pp), form['fileToUpload'].value)
        # write file
        ofile  = myfile()
        ofile.write_("a",fname + ".meta", jsonfilemeta)
        ofile.write_("ab",fname, file)
        # send response
        data = {}
        data['uri'] = self.make_url(fname, key)
        self.send_html(self.content(data))


    def content(self, data):
        # get url & params
        request = urlparse(self.path);
        path = request.path

        if path == "" or path == "/":
            path = "index"
            
        # if download page
        dluri = re.split("/dl/", path)

        if len(dluri) >= 2:
            filename = dluri[1]
            print(filename)
            # split prams
            qs = re.split('&', request.query)
            # unique key
            key = qs[0] if len(qs) >= 1 else ""
            # passphrase
            pp = qs[1] if len(qs) >= 2 else ""
            try:
                # open file
                ofile  = myfile()
                meta = ofile.read_("r",filename + ".meta")
                dmeta = json.loads(meta)

                if time.time() > dmeta["expiration"]:
                    content = self.load_assets("error.html")
                    content = content.read() 
                    ofile.delete(filename)
                    ofile.delete(filename + ".meta")
                else: 
                    # decript
                    bin = ofile.read_("rb",filename)
                    content = decrypt((key + pp), bin)
                    # send binary
                    self.isBin = True

                if "burafterreading" in dmeta:
                    ofile.delete(filename)
                    ofile.delete(filename + ".meta")

            except:
                content = self.load_assets("error.html")
        else:
            try:
                # get extension
                ext = re.split('\.', path)
                if len(ext) <= 1:
                    content = self.load_assets(ext[0] + ".html")
                else:
                    if ext[1] == "png":
                        content = self.load_assets_bin(ext[0] + "." + ext[1])
                    else:
                        content = self.load_assets(ext[0] + "." + ext[1])
            except:
                content = self.load_assets("404.html")

            if len(data):
                if "uri" in data:
                    content = content.replace('<%url%>', data["uri"])
          
        return content
        
    def load_assets(self, assetname):
        content = codecs.open("assets/" + assetname, "r", "utf-8")
        content = content.read()   
        return content
    
    def load_assets_bin(self, assetname):
        self.isBin = True;
        content = codecs.open("assets/" + assetname, "rb")
        content = content.read()   
        return content
    
    def send_html(self, htmlstr):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(htmlstr.encode('utf-8'))    
        
    def send_bin(self, bin):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(bin) 
    
    def make_url(self, fname, key):
        clt_adress, inport = self.client_address
        port = str(PORT)
        return "http://" + clt_adress + ":" +port+ "/dl/" + fname + "?" + key + "&"
        
if __name__ == '__main__':
    try:
        server = http.server.HTTPServer(('', PORT), MyHandler)
        print('Started http server on port : ', PORT)
        server.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down server')
        server.socket.close()