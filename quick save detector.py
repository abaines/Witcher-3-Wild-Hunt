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


# config / settings / options

rootDirectory = "../gamesaves/"

globSearchPattern = "QuickSave_*.sav"



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

# global cache for hash records
hashRecords = {}

# scan for any file changes among hash records
# trigger callback for any new or changed file
def scan(callback):
   #print(hashRecords)
   print(fullGlobSearch)
   for file in getGlobFiles():
      fileHash = hashSha1File(file)

      if file not in hashRecords:
         if callback:
            callback(file,"new")
         
      elif fileHash != hashRecords[file]:
         if callback:
            callback(file,"diff")

      hashRecords[file] = fileHash

# callback for dealing with new or changed files
def callback(fileName,cause):
   print("CALLBACK",cause,fileName)

# temp space

scan(callback)
scan(callback)
scan(None)
scan(callback)
scan(callback)
scan(callback)

print("Startup sequence complete")

