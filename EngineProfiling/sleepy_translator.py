description='HOW TO USE: \nCapture spring  with very sleepy CS, save .sleepy file\nDownload and unzip next to script the debug symbols from\n http://springrts.com/dl/buildbot/default/develop/101.0.1-63-g5ebf047/win32/ \nDownload engine source files from github\nRun script with -i [inputfile].sleepy -s C:/spring_source/spring/ \nOpen [inputfile_translated].sleepy in very sleepy CS'

print(description)


from optparse import OptionParser
import traceback
# import datetime, os, re, xmlrpclib
# from xmlrpclib import ServerProxy, Error
import zipfile
import os
import sys
import shlex
from subprocess import Popen, PIPE

parser=OptionParser(usage="usage: python sleepy_tranlator.py -i capture.csv", version= "0.1")
parser.add_option('-i', '--input',action='store',dest='input', default='capture.sleepy',help='input csv file from Very Sleepy')
parser.add_option('-s', '--sourcepath',action='store',dest='sourcepath',help='Source path for spring source e.g. D:/springsource/',default = 'N:/engine_source/spring/')
parser.add_option('-d', '--dbgfile',action='store',dest='dbgfile',help='debug file to use',default ='spring.dbg')
parser.add_option('-a', '--addr2linekey', action = 'store', dest = 'addr2linekey', help ='A SANE BASE PATH IN THE addr2line_results.txt file', default = 'build/default/../../')

options, args=parser.parse_args()
sleepytype='csv'
print(options)

dbgmax=100000000
cnt=0

if '.sleepy' in options.input:
	fh=open(options.input, 'rb') 
	z=zipfile.ZipFile(fh)
	for name in z.namelist():
		print(name)
		z.extract(name, os.getcwd())

	symbols=open('Symbols.txt')
	sleepyfile=symbols.readlines()
	symbols.close()
else:
	print('failed to open',options.input)




address_count=0
to_translate=[]
for sleepyline in sleepyfile:
	#print sleepyline
	try:
		(sym, module, address, sourcefile, sourceline)=shlex.split(sleepyline.strip())#sym1473 "nvoglv32" "[687BAD05]" "" 0
		#print name, module,inpercent
		# print "module, address",module, address
		if module=='spring' and '[' in address:
			if cnt<dbgmax:
				cnt+=1
				oldaddr=address
				# print address
				# print address.strip('\"[]')
				to_translate.append(address.strip('\"[]'))
				address_count+=1		

	except:
		print('Failed to parse line',sleepyline,'in',options.input,sleepyline.strip().split(' '))
		traceback.print_exc()
		pass
		
# print 'addresses:',to_translate
cmd = ['addr2line.exe', '-e', options.dbgfile]
print('Command line: ' + ' '.join(cmd))
addr2line = Popen(cmd, stdin = PIPE, stdout = PIPE, stderr = PIPE,encoding='utf8')
if addr2line.poll() == None:
	stdout, stderr = addr2line.communicate('\n'.join(to_translate))
else:
	stdout, stderr = addr2line.communicate()
if stderr:
	print('%s stderr: %s' % (ADDR2LINE, stderr))
if addr2line.returncode != 0:
	print(' fatal : %s exited with status %s' % (ADDR2LINE, addr2line.returncode))
print ('\t\t[OK]')
# print stdout
translated = stdout.split('\n')
addr2linefile = open('addr2line_results.txt','w')
addr2linefile.write(stdout)
addr2linefile.close()
result = {}
if len(to_translate) <= len(translated):
	for i in range(len(to_translate)):
		result[to_translate[i]] = translated[i]
else:
	print('Unmatched to_translate and tranlated lengths!',len(to_translate) , len(translated))

print('Query successful, stacktrace results', len(result))


def getcodeline(path, i): #fetches line i of the code, removes double quotes, replace with singles, max length of 80 chars
	try:
		codef=open(path)
		codelines=codef.readlines()
		line=codelines[i-1] #because lines are indexed from 1!
		line=line.strip().replace('\"','')
		line=line.replace('	','')
		line=line.replace('\\','')
		if len(line)>75:
			line=line[0:74]+'...'
		#print 'got code line:',line
		if len(line)<1:
			print('got suspiciosly short line',path,i,line)
		return line
	except:
		print('warning, cant fine code line',path,line)
		pass
		return ''
	
outf=open('Symbols.txt','w')
goodline=0
for sleepyline in sleepyfile:
	#print sleepyline
	try:
		(sym, module, address, sourcefile, sourceline)=shlex.split(sleepyline.strip())
		shortaddr=address.strip('[]\"') 
		if '?' in sleepyline:
			print ("?",sleepyline)
		if shortaddr in result:
			goodline+=1
			newsourcefile=result[shortaddr].rpartition(':')[0]
			newsourceline=result[shortaddr].rpartition(':')[2]
			if '?' in newsourceline:
				newsourceline = '0'
			if options.sourcepath and options.addr2linekey in newsourcefile:
				
				rawsourcefile = newsourcefile.partition(options.addr2linekey)[2]
				if '?' in sleepyline:
					print('rawsourcefile',rawsourcefile)
				path=options.sourcepath+rawsourcefile
				shortname='<'+rawsourcefile.rpartition('/')[2]+'> ' # so we only have the filename like Unit.cpp
				codeline=getcodeline(path, int(newsourceline))
				if codeline !='':
					if '/' in rawsourcefile:
						shortname=shortname+codeline
				shortname.replace('"','')
				#shortname= 'dunno'
				out_line = ' '.join([sym,'"'+module+'"','"'+shortname+'"','"'+path+'"',str(newsourceline)])+'\n'
				outf.write(out_line)
			else:
				if options.addr2linekey in newsourcefile:
					address = newsourcefile.partition(options.addr2linekey)[2]
				outf.write(' '.join([sym,'"'+module+'"','"'+address+'"','"'+newsourcefile+'"', newsourceline])+'\n')
		else:
			outf.write(sleepyline)
	except:
		print('Failed to translate line',sleepyline,'in',options.input)
		traceback.print_exc()
		outf.write(sleepyline)
		pass
print('Good lines=',goodline,' out of ', len (result))
outf.close() # GOD FUCKING DAMMIT!


outfname=options.input.partition('.sleepy')[0]+'_translated.sleepy'

cmd = 'del '+outfname
print(cmd)
os.system(cmd)
# THE ORDER IN WHICH THESE FILES ARE ZIPPED DECIDES EVERYTHING!!!!!!!!!!!!!!!!!!
cmd='zip -1 '+outfname+' Stats.txt Symbols.txt IPCounts.txt Callstacks.txt "Version 0.90 required"'
print(cmd)
os.system(cmd)
print('Done zipping')



#Sleepy line format:
#0. Name (or address, if unable to resolve)
#1. Exclusive time
#2. Inclusive time
#3. Exclusive %
#4. Inclusive 
#5. module (check for spring and hex in NAME field!)
#6. source file (blank for stuff we want)
#7. source line (default 0 for unknown source files)
#free,12.500104,12.500104,40.476944,40.476944,msvcrt,[unknown],0
#[008053AF],0.050003,0.050003,0.161916,0.161916,spring,,0
