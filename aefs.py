# Configs
__HOST__ = '0.0.0.0'
__PORT__ = 1977
__THREADS__ = 10
__CERTS_FOLDER__ = "/etc/ssl/localcerts/"
__VERBOSE__ = "AEFS - "
__DOMAIN__ = "mlklm.net"

import base64
import cgi
import codecs
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from metafile import metafile
import mimetypes
from myfile import myfile
from queue import Queue
import re
import ssl
import threading
from urllib.parse import urlparse

# AEFS handler
class AEFS(BaseHTTPRequestHandler):
     
    def handle(self):
        #try:
            BaseHTTPRequestHandler.handle(self);
        #except:
           # print("handler failed")
           # self.forceSSL()
            
    def do_GET(self):
        content = self.content()
        if self.isBin is True:
            self.send_bin(content)
        else: 
            self.send_html(content)

    def do_POST(self):
        # retrieve post data
        form = cgi.FieldStorage(fp=self.rfile, headers=self.headers, enviheron={'REQUEST_METHOD':'POST'})
        filesize = len(form['fileToUpload'].value)
        amime = mimetypes.guess_all_extensions(form['fileToUpload'].headers['Content-Type'])
        if filesize > 0 and len(amime) > 0:
            ofile = myfile()
            # create encode file
            ofile.set_mime(amime[0])
            fname = ofile.generate_name()
            print(__VERBOSE__ + "Encrypt " + fname + " ...")
            data = ofile.encrypt(form['passphrase'].value, form['fileToUpload'].value)
            print(__VERBOSE__ + fname + " encrypted !")
            ofile.write_("ab", fname, data)
            # create encode filemeta
            mf = metafile()
            if 'burnafterreading' in form:
                mf.set_burnafterreading(1)
            if 'expiration' in form:    
                mf.set_expiration(form['expiration'].value)
                
            ofile.write_("a", fname + ".meta", mf.get_json_metafile())
            # send response
            data = {}
            data['url'] = self.make_url(ofile.get_file_name(), ofile.get_file_key())
            self.send_html(self.content(data))
        else:
            data = {}
            data['error_msg'] = "File empty !!"
            content = self.load_assets("error.html")
            content = content.replace('<%error_msg%>', data["error_msg"])
            self.send_html(content)


    def content(self, data={}):
        self.isBin = False
        # get url & params
        request = urlparse(self.path);
        path = request.path

        if path == "" or path == "/":
            path = "index"
            
        # if download page
        dlurl = re.split("/dl/", path)
        if len(dlurl) >= 2:
            filename = dlurl[1]
            qs = re.split('&', request.query)
            key = qs[0] if len(qs) >= 1 else ""# unique key
            pp = qs[1] if len(qs) >= 2 else ""# passphrase
            try:
                # open file
                ofile  = myfile()
                meta = ofile.read_("r", filename + ".meta")
                mf = metafile(meta)

                if mf.is_date_valid():
                    content = self.load_assets("error.html")
                    content = content.read() 
                    ofile.delete(filename)
                    ofile.delete(filename + ".meta")
                else: 
                    # decript
                    print(__VERBOSE__ + "Decrypt " + filename + " ...")
                    bin = ofile.read_("rb", filename)
                    content = ofile.decrypt(pp, key, bin)
                    print(__VERBOSE__ + filename + "Decrypted !!")
                    self.isBin = True

                if  mf.is_burafterreadingable():
                    ofile.delete(filename)
                    ofile.delete(filename + ".meta")

            except:
                data["error_msg"] = "File unavailable !!"
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
                data["error_msg"] = "Page  unavailable !!"
                content = self.load_assets("error.html")
                
        if len(data) and self.isBin is False:
            if "url" in data:
                content = content.replace('<%url%>', data["url"])

            if "error_msg" in data:    
                content = content.replace('<%error_msg%>', data["error_msg"])
          
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
    
    def forceSSL(self):
        self.requestline = ""
        self.request_version = "HTTP/1.0"
        self.send_response(301)
        self.send_header('Location', 'https://' + str(__DOMAIN__) + ":" + str(__PORT__))
        self.end_headers()
        
    def make_url(self, fname, key):
        port = str(__PORT__)
        return "http://" + __DOMAIN__ + ":" + port + "/dl/" + fname + "?" + key + "&"
    
    def log_request(self, code='-', size='-'):
        return
    def log_error(self, format, * args):
        return
    def log_message(self, format, * args):
        return
      
# AEFS HTTPServer
try:
    server = HTTPServer((__HOST__, __PORT__), AEFS)
    server.socket = ssl.wrap_socket(server.socket, certfile=__CERTS_FOLDER__+'aefs.pem', server_side=True)
    print(__VERBOSE__ + 'Started server ...')
    print(__VERBOSE__ + 'Listen on ' + str(__HOST__) + ':' + str(__PORT__))
    lock = threading.Lock()
    # The worker thread processes server_forever()
    def worker():
        while True:
            t = q.get()
            print(__VERBOSE__ + 'Start web instance on ' + t.getName())
            server.serve_forever()
            print('failed')
    # Create the queue/thread pool.
    q = Queue()
    for i in range(__THREADS__):
        t = threading.Thread(target=worker)
        t.daemon = True  
        t.start()
        q.put(t)
    q.join() 

except KeyboardInterrupt:
    print(__VERBOSE__ + '^C received, shutting down server')
    server.socket.close()