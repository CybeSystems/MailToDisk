###################################################################
# MailToDisk Freezer - Using cx_freeze
###################################################################

name = 'MailToDisk'
version = '1.0'

Win32ConsoleName = 'MailToDisk.exe'
#Win32WindowName = 'MailToDisk-Win32.exe'

copyRuntime = True
killTasks = False

###################################################################
# Import Libs, detect x86/x64
###################################################################

import re
import urllib.request, urllib.parse, urllib.error, configparser
from distutils.core import setup
import sys, os, shutil, datetime, zipfile, subprocess, fnmatch,glob

import platform
sys.path.insert(0, os.path.join(os.path.realpath(os.path.dirname(sys.argv[0])), 'lib'))

if platform.architecture()[0] == '64bit':
    sys.path.insert(0, os.path.join(os.path.realpath(os.path.dirname(sys.argv[0])), 'libX64'))
    x86x64 = 'X64'
    x86x64BuildPath = "exe.win-amd64-3.4"
else:
    sys.path.insert(0, os.path.join(os.path.realpath(os.path.dirname(sys.argv[0])), 'libX86'))
    x86x64 = 'X86'
    x86x64BuildPath = "exe.win32-3.4"

from cx_Freeze import setup, Executable
import distutils.dir_util
import win32api

scriptpath = os.path.realpath(os.path.dirname(sys.argv[0])).replace('\\','/')
scriptpathParentFolder = os.path.dirname(scriptpath)

###################################################################
# Set Version
###################################################################

config = configparser.ConfigParser()
config.optionxform=str
config.read("AppInfo/appinfo.ini")
config.set('Version', 'DisplayVersion', version)
with open("AppInfo/appinfo.ini", 'w') as configfile:
    config.write(configfile)

###################################################################
# Kill running Process before Build, delete old builds
###################################################################

sys.argv.append('build')

#Kill process if running
if killTasks == True:
    os.system("taskkill /im " + Win32ConsoleName + " /f")
    #os.system("taskkill /im " + Win32WindowName + " /f")

# clear the dist dir
#if os.path.isfile("dist/%s" % Win32WindowName):
#    os.remove("dist/%s" % Win32WindowName)
if os.path.isfile("dist/%s" % Win32ConsoleName):
    os.remove("dist/%s" % Win32ConsoleName)
#if os.path.isfile("%s" % Win32WindowName):
#    os.remove("%s" % Win32WindowName)
if os.path.isfile("%s" % Win32ConsoleName):
    os.remove("%s" % Win32ConsoleName)
if os.path.isfile("python27.dll"):
    os.remove("python27.dll")

shutil.rmtree('dist',ignore_errors=True)
shutil.rmtree('librarys',ignore_errors=True)
shutil.rmtree('build',ignore_errors=True)

###################################################################
# cx_freeze
###################################################################

includefiles = []
includes = []
excludes = []
packages = []

path = []

bin_path_includes=['libs']

# Create GUI Version
# GUI Version not needed
'''Win32Exe = Executable(
    script = "MailToDisk.py",
    initScript = None,
    base = 'Win32GUI',
    targetName = Win32WindowName,
    compress = True,
    copyDependentFiles = True,
    appendScriptToExe = True,
    appendScriptToLibrary = False,
    icon = "AppInfo/appicon.ico"
)

setup(
    version = "0.1",
    description = "MailToDisk Win32",
    author = "CybeSystems.com",
    name = "MailToDisk",
    options = {"build_exe": {"includes": includes,
                             "excludes": excludes,
                             "packages": packages,
                             "include_msvcr": True,   #skip error msvcr100.dll missing
                             'include_files':includefiles,
                             "bin_path_includes":    bin_path_includes,
                             "path": path
    }
    },
    executables = [Win32Exe]
)
'''

#Create Console Version
ConsoleExe = Executable(
    script = "MailToDisk.py",
    initScript = None,
    base = 'Console',
    targetName = Win32ConsoleName,
    compress = True,
    copyDependentFiles = True,
    appendScriptToExe = True,
    appendScriptToLibrary = False,
    icon = "AppInfo/appicon.ico"
)

setup(
    version = "0.1",
    description = "MailToDisk Console",
    author = "CybeSystems.com",
    name = "MailToDisk",
    options = {"build_exe": {"includes": includes,
                             "excludes": excludes,
                             "packages": packages,
                             "include_msvcr": True,   #skip error msvcr100.dll missing
                             'include_files':includefiles,
                             "bin_path_includes":    bin_path_includes,
                             "path": path
    }
    },

    executables = [ConsoleExe]
)

###################################################################
# Copy needed files for release
###################################################################

print ("########################################")
print ("Copy Files")
print ("########################################")

os.makedirs('build/' + x86x64BuildPath + '/lib' + x86x64)

listOfFiles = os.listdir('build/' + x86x64BuildPath)
for f in listOfFiles:
    if os.path.isfile('build/' + x86x64BuildPath + '/' + f):
        shutil.copy('build/' + x86x64BuildPath + '/' + f, 'build/' + x86x64BuildPath + '/lib' + x86x64 + '/' + f)
        os.remove('build/' + x86x64BuildPath + '/' + f)


#shutil.copy('build/' + x86x64BuildPath + '/lib' + x86x64 + '/' + Win32WindowName, 'build/' + x86x64BuildPath + '/' + Win32WindowName)
shutil.copy('build/' + x86x64BuildPath + '/lib' + x86x64 + '/' + Win32ConsoleName, 'build/' + x86x64BuildPath + '/' + Win32ConsoleName)
shutil.copy('build/' + x86x64BuildPath + '/lib' + x86x64 + '/library.zip', 'build/' + x86x64BuildPath + '/library.zip')

shutil.copyfile('build/' + x86x64BuildPath + '/lib' + x86x64 + '/python34.dll', 'build/' + x86x64BuildPath + '/python34.dll')
shutil.copyfile('build/' + x86x64BuildPath + '/lib' + x86x64 + '/msvcr100.dll', 'build/' + x86x64BuildPath + '/msvcr100.dll')

os.remove('build/' + x86x64BuildPath + '/lib' + x86x64 + '/python34.dll')
os.remove('build/' + x86x64BuildPath + '/lib' + x86x64 + '/msvcr100.dll')

#Drop unneeded files
os.remove('build/' + x86x64BuildPath + '/lib' + x86x64 + '/library.zip')
#os.remove('build/' + x86x64BuildPath + '/lib' + x86x64 + '/' + Win32WindowName)
os.remove('build/' + x86x64BuildPath + '/lib' + x86x64 + '/' + Win32ConsoleName)

shutil.copyfile('build/' + x86x64BuildPath + '/library.zip', 'build/' + x86x64BuildPath + '/lib' + x86x64 + '/libraries.zip')
shutil.copyfile('config.ini', 'build/' + x86x64BuildPath + '/config.ini')
os.remove('build/' + x86x64BuildPath + '/library.zip')

#Prepare Portable Version
shutil.rmtree('!RELEASE_' + x86x64 ,ignore_errors=True)
distutils.dir_util.copy_tree('build/' + x86x64BuildPath, '!RELEASE_' + x86x64 + '/App')
#shutil.copytree('AppInfo', '!RELEASE_' + x86x64 + '/App/AppInfo')

def fancyLogoWin():
    return r"""
   ____      _          ____            _
  / ___|   _| |__   ___/ ___| _   _ ___| |_ ___ _ __ ___  ___
 | |  | | | | '_ \ / _ \___ \| | | / __| __/ _ \ '_ ` _ \/ __|
 | |___ |_| | |_) |  __/___) | |_| \__ \ |_  __/ | | | | \__ \
  \____\__, |_.__/ \___|____/ \__, |___/\__\___|_| |_| |_|___/
       |___/                  |___/
"""
curFancyLogo = fancyLogoWin()
print (curFancyLogo)
print ("")
print ("########################################")
print ("Build SUCCESSFUL !!")
print ("########################################")
print ("")
