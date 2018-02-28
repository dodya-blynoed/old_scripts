import os
import string
from os.path import expanduser
from subprocess import Popen
import ctypes

homeDir = "C:\\"

#homeDir = os.environ['HOME']

def doTheCreep(productPath):    
    os.chdir(homeDir)
    absPath = os.path.join(homeDir, productPath)
		
    if os.path.exists(absPath) and os.path.isdir(absPath):
        print "Updating "+productPath
        os.chdir(absPath)
        list = os.popen('svn up').read()
        print list
        return list
    else:
        print "Unable to access " + absPath
        return ()
        
def gatherLocalConflicts(svnlist):
    result = ()
    for eachLine in svnlist:
        if eachLine[:1]=="!":
            result.__add__(eachLine)
    return result        

def Mbox(title, text, style):
    ctypes.windll.user32.MessageBoxA(0, text, title, style)
	
def comeAndGetIt():
    tupleOfHorror = ( "rx/", 
	#"rx/1.2.21.10/", "rx/1.2.22.10/",
    #"rx/1.2.23.10/","rx/1.2.24.10/",	"rx/1.2.25.10/",
	"tx/1.1.27.10",
	"tx/",
	"rx/1.2.26.20/",
    "rx/1.2.27.10/",
	"rx/1.2.28.10/",
	"rx/1.2.29.10/",
	"rx/1.2.30.10/"
	
	)
    conflictsList=()
    for eachProduct in tupleOfHorror:
        list = doTheCreep(eachProduct)
        conflictsList = conflictsList + (list,)     
    # conflicts = gatherLocalConflicts(conflictsList)
    # if len(conflicts)>0:
        # print "Check these files for conflicts:"
        # for eachConflict in conflicts:
            # print eachConflict 
    
#if __name__ == "__main__":
os.system("python C:\Users\\backup.py -p R -m A")
comeAndGetIt()
#p = Popen("C:\Users\\x_cute_rx.bat")
#stdout, stderr = p.communicate()
Mbox('rx update', 'Compilation complete!', 0)
#os.popen("kdialog --passivepopup 'SVN update complete!' '99999999999'")

