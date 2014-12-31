import sys
import urllib
from urllib import request
import time
import os
from multiprocessing import Process
import time

def s ():
    string = sys.argv[1]
            
    col = string.find(":")
    ip = string[0:col]
    port = string[col+1:len(string)]

    proxy_handler = urllib.request.ProxyHandler({'http' : 'http://'+ip+":"+port})
    proxy_auth_handler = urllib.request.HTTPBasicAuthHandler()
    opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
    opener.open("http://www.google.com")

    while(True):
        try:
            putFile = open(sys.argv[2], 'a')
            putFile.write(sys.argv[1])
            putFile.close()
            return
        except:
            print("Waiting due to failure to save")
            time.sleep(1)

if __name__ == '__main__':
    p = Process(target=s)
    p.start()
    p.join()
    p.terminate()
