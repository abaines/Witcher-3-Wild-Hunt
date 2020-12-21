# Alan Baines

import glob
import hashlib
import io
import os
import random
import re
import shutil
import string
import sys
import threading
import time
import winsound
import ctypes


# config / settings / options

rootDirectory = "../gamesaves/"

globSearchPattern = "QuickSave_*.sav"

scanPeriod = 3.0



# code method definitions

# get the time a file was last modified from OS
def lastModified(filePath):
   return os.path.getmtime(filePath)

# get the sha1 hash of a raw bytes
def hashSha1(rawBytes):
   return hashlib.sha1(rawBytes).hexdigest()

# read an OS file into memory and get the sha1 hash of the file
def hashSha1File(filePath):
   with open(filePath,'rb') as bufferedReader:
      rawBytes = bufferedReader.read()
      return hashSha1(rawBytes)

# get absolute file OS path for a relative path
def absolutePath(filePath):
   return os.path.abspath(filePath)

# join two OS paths together
def joinPath(base,bonus):
   return os.path.join(base,bonus)

# full glob search text
fullGlobSearch = joinPath(absolutePath(rootDirectory),globSearchPattern)

# get list of files matching the glob search pattern
def getGlobFiles():
   return glob.glob(fullGlobSearch)

# copy OS file
def copyFile(source,destination):
   shutil.copy2(source,destination)

# OS sound beep
def beep(frequency, duration):
   winsound.Beep(frequency,duration)

def beep1():
   beep(120,60)

def beep2():
   beep(320,60)


# global cache for hash records
hashRecords = {}

# scan for any file changes among hash records
# trigger callback for any new or changed file
def scan(callback):
   #print(hashRecords)
   #print(fullGlobSearch)
   for file in getGlobFiles():
      fileHash = hashSha1File(file)

      if file not in hashRecords:
         if callback:
            callback(file,fileHash,"new")

      elif fileHash != hashRecords[file]:
         if callback:
            callback(file,fileHash,"diff")

      hashRecords[file] = fileHash

      time.sleep(0)

g_lastSave = -1

def getLastSaveText():
   if g_lastSave>0:
      delta = time.time() - g_lastSave
      return str(int(delta))
   else:
      return "!"


# callback for dealing with new or changed files
def callback(fileName,fileHash,cause):
   beep1()
   print("CALLBACK",cause,fileHash, fileName.rsplit('\\', 1)[-1] ) #TODO: make slash direction independent
   global g_lastSave
   g_lastSave = time.time()

   fileSplit = os.path.splitext(fileName)

   destination = fileSplit[0] + '.' + fileHash + fileSplit[1]

   print( destination.rsplit('\\', 1)[-1] ) #TODO: make slash direction independent

   hashRecords[destination] = fileHash

   copyFile(fileName, destination)

   print("")
   beep2()

def setTitle(titleText):
   ctypes.windll.kernel32.SetConsoleTitleW(titleText)


# polling loop for scanning
def threader():

   setTitle(getLastSaveText() + " +")
   try:
      scan(callback)
   except:
      pass

   setTitle(getLastSaveText() + " = = =")

   threading.Timer(scanPeriod,threader).start()


# Initialization

beep1()

scan(None)

threader()

beep2()

setTitle("Startup sequence complete")
print("Startup sequence complete")

