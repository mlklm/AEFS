# AEFS

# /!\ THIS IS A DEVELOP APPS - USE IT WITH LOGICS 

AEFS is an encrypt/decrypt file sharing python apps.  

  - Encrypt file with AES 256 bits
  - Genrate a unique and volatile url
  - Add a passphrase to increase the encryption
  - Decrypt with the url
  - Simple customization
 
### Version
0.0.1

### Tech

Develop with/for [Python3.4](https://www.python.org/download/releases/3.4.0/)

### Installation

You need to use so command :

```sh
$ aptitude install python3 python3-pip git openssl
$ pip3-2 install simple-crypt
$ mkdir /etc/ssl/localcerts
$ openssl req -new -x509 -keyout /path/to/certificates.pem -out /path/to/certificates.pem -days 365 -nodes
$ git clone https://github.com/mlklm/AEFS.git
$ cd AEFS/
$ python3 aefs.py
```

### Development

Want to contribute? Great!
Send me a mail : mlklm@mail.com

### Licence

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
