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

searchPattern = "QuickSave_*.sav"



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



# temp space

sp = joinPath(absolutePath(rootDirectory),searchPattern)

print(sp)

for file in glob.glob(sp):
   print(hashSha1File(file),file)

   print("")
   print("")

print("Startup sequence complete")

