from PyQt4 import QtCore,QtGui
import urllib
from urllib import request, error
from http import client
import socket
#from multiprocessing import Process, Queue
import threading
import time


class scrapper():
    putFile = None
    threads = 0
    stop = False
    thre = {}
    printbackup = "\nProxy scrapper made by 3 sided square"
    def __init__(self, fileName, maxThreads, outputwindow=None, delay=0.2):
        self.delay = delay
        self.outputWindow = outputwindow
        if(fileName == ""):
            self.forceOutput("!File name can not be blank, aborted!")
            self.stop = True
            return
        if(maxThreads < 1):
            self.forceOutput("!Too few threads, aborted!")
            self.stop = True
            return
        if(delay <= 0):
            self.forceOutput("!OS delay is too low, aborted!")
            self.stop= True
            return
        self.threads = maxThreads
        self.forceOutput("\nStarting scrap on " + fileName)
        self.stop = False

    def output(self, String):
        if(self.outputWindow != None):
            self.printbackup+=String
            self.outputWindow.verticalScrollBar().setValue(self.outputWindow.verticalScrollBar().maximum())
        else:
            print(String)

    def forceOutput(self, string):
        if(self.outputWindow != None):
            self.outputWindow.append(string)
            self.outputWindow.verticalScrollBar().setValue(self.outputWindow.verticalScrollBar().maximum())
        else:
            print(string)

    def makeCall(self,string, putFile):
        self.output("Scrapping " + string[:-1] + "...")
        self.threads -=1
        col = string.find(":")
        ip = string[0:col]
        port = string[col+1:len(string)]
        try:
            proxy_handler = urllib.request.ProxyHandler({'http' : 'http://'+ip+":"+port})
            proxy_auth_handler = urllib.request.HTTPBasicAuthHandler()
            opener = urllib.request.build_opener(proxy_handler, proxy_auth_handler)
            opener.open("http://www.google.com")
            self.output("\nFound successful: " + string)
            self.threads+=1
        except urllib.error.URLError as detail:
            self.threads+=1
            self.output("\nCould not find " + string)
            return
        except urllib.error.HTTPError as detail:
            self.thread+=1
            self.output("\n" + string + " did not respond")
            return
        except http.client.BadStatusLine as detail:
            self.thread+=1
            self.output("\n" + string + " did not give a valid response")
            return
        except:
            self.thread+=1
            return
        
        while(not self.stop):
            try:
                putFile = open(putFile, 'a')
                putFile.write(string)
                putFile.close()
                return
            except:
                time.sleep(1)

    def scrapProxies(self, fileName):
        try:
            file = open(fileName, 'r')
            putFile = fileName.split(".")[0]+"_working.txt"
            put = open(putFile, 'w')
            put.close()
            self.output("file read...")
        except:
            self.output("\nFailed to read in file")
            self.stop = True
            return
        if(True):
            x = 0
            linelot = ""
            self.output("\nStarting check")
            for line in file:
                self.output("\nCueing " + line + "...")
                self.thre[x] = threading.Thread(target=self.makeCall, name=None, args=(line,putFile))
                while(not self.stop):
                    if(self.threads > 0):
                        try:
                            self.thre[x].start()
                            time.sleep(self.delay)
                            if(self.outputWindow != None):
                                self.outputWindow.append(self.printbackup)
                                self.printbackup=""
                            break
                        except:
                            time.sleep(self.delay)
                    time.sleep(self.delay)
                x += 1
            file.close()

    def stopScrap(self):
        time.sleep(0.5)
        timeBreak = self.threads * self.delay * 4
        self.forceOutput("\nForceing quit after " + str(timeBreak) + " Seconds.")
        self.stop=True
        for thread in self.thre:
            thread.stop()
        time.sleep(timeBreak)
        if(self.thre != {}):
            self.scary()

    def scary(self):
        exit()
