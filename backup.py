import ctypes
import os
import argparse
import time
import string
import shutil

def makeList(actionDir,mode):
	os.chdir(actionDir)
	fileList = os.popen('svn st' + mode).read()
	newList = string.split(fileList, '\n')
	return newList


def lookThrough(newList,dst, text_file):
	for eachFile in newList:
		if eachFile[:1]=='!':
			conflictMsg='\t\t ***  Check this file for conflicts: '+eachFile
			print conflictMsg
			text_file.writelines(conflictMsg)
		f = eachFile[1:].strip()
		
		if os.path.exists(f) and os.path.isfile(f) and (f[-3:]<>'jar') :
			try:
				ef="\n\n"+eachFile
				print ef
				text_file.writelines(ef)
				fileName = (f).split('\\')[len(f.split('\\'))-1]
				if os.path.exists(os.path.join(dst, fileName)) :
					newFile=(fileName).split('.')[len(fileName.split('.'))-2]
					extension=(fileName).split('.')[len(fileName.split('.'))-1]
					i=1
					while True:
						new_name = os.path.join(dst, newFile + "_" + str(i) + "." + extension)
						#existing_path=os.path.join(dst, fileName)
						copying_file=f
						if not os.path.exists(new_name):
							shutil.copy(copying_file, new_name)
							copyMsg= "\nRenamed copy of " +  str(copying_file)+ " as "+ str(new_name)
							print copyMsg
							text_file.write(copyMsg)
							break
						i += 1
				else:		
					shutil.copy(f,dst)
					regCopyMsg="\nRegular copy from  "+f + " to " + dst
					print regCopyMsg
					text_file.write(regCopyMsg)
				
			except shutil.Error as e:
				print('Error: %s' % e)
				text_file.write(e)

def calcDirs(homeDir):
	parser = argparse.ArgumentParser()
	parser.add_argument('-p', dest='dir', default=os.path.join(homeDir,'temp_radix'))
	parser.add_argument('-m', dest='mode', default='')
	args = parser.parse_args()
	tempDir=""
	actionDir=""
	if args.dir=='T' or args.dir=='TX':
		print 'Backup TX:'
		tempDir=os.path.join(homeDir,'temp_TX')
		actionDir = os.path.join(homeDir,'TX\\')
	else:
		print 'Backup rx:'
		tempDir=os.path.join(homeDir,'temp_rx')
		actionDir = os.path.join(homeDir,'rx\\')
	if not os.path.isdir(tempDir):
		print "Hey, you have no temp dir for backup in your home directory!"
	mode=''
	if args.mode=='M':
		mode=' | grep ^M'
	else:
		mode=''            
	return (tempDir, actionDir, mode)
            
    
def createTempDir(tempDirPath):
	now = time.ctime().replace(":","_")
	print "NOW = " + now
	os.chdir(tempDirPath)    
	os.mkdir(now)
	dst = os.path.abspath(now) 
	if os.path.exists(now) and os.path.isdir(now):
		print "Backup directory: " + dst
	else:
		print "Oh no! I could not create backup directory! :("
	return dst        

if __name__ == "__main__":
	homeDir = "C:\\"
	os.chdir(homeDir)
	args = calcDirs(homeDir)  
	dst = createTempDir(args[0])  
	list = makeList(args[1], args[2])
	text_file = open(os.path.join(dst,"info.txt"), "w")
	text_file.write("Home directory: " + homeDir+"\nBackup directory: " + dst)
	
	lookThrough(list,dst,text_file)  
	text_file.close()
	#os.popen("kdialog --passivepopup 'Backup complete!' '99999999999'")  linux
	#ctypes.windll.user32.MessageBoxA(0, "Backup complete!", dst, 1) windows
