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

parser=OptionParser(usage="usage: python sleepy_tranlator.py -i capture.sleepy", version= "0.1")
parser.add_option('-i', '--input',action='store',dest='input', default='capture.sleepy',help='input .sleepy file from Very Sleepy')
parser.add_option('-s', '--sourcepath',action='store',dest='sourcepath',help='Source path for spring source e.g. D:/springsource/',default = 'N:/engine_source/spring/')
parser.add_option('-d', '--dbgfile',action='store',dest='dbgfile',help='debug file to use',default ='spring.dbg')
parser.add_option('-a', '--addr2linekey', action = 'store', dest = 'addr2linekey', help ='A SANE BASE PATH IN THE addr2line_results.txt file', default = 'build/default/../../')

options, args=parser.parse_args()

print("Selected options:",options)

#Open the .sleepy file and unzip its contents
fh=open(options.input, 'rb')
z=zipfile.ZipFile(fh)
for name in z.namelist():
	print(name)
	z.extract(name, os.getcwd())

symbols=open('Symbols.txt')
sleepyfile=symbols.readlines()
symbols.close()


#collect the addresses we wish to translate with addr2line:
to_translate=[]
for sleepyline in sleepyfile:
	try:
		(sym, module, address, sourcefile, sourceline)=shlex.split(sleepyline.strip())#sym1473 "nvoglv32" "[687BAD05]" "" 0
		if 'spring' in module:
			to_translate.append(sym)
	except:
		print('Failed to parse line',sleepyline,'in',options.input,sleepyline.strip().split(' '))
		traceback.print_exc()
		pass

#Perform the address translation:
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
for i,sleepyline in enumerate(to_translate):
	addr2linefile.write(sleepyline + ' -->>> ' + translated[i] + '\n')
addr2linefile.close()

#parse the results of addr2line into a dict, and make sure we have the correct amount of entries in both:
result = {}
if len(to_translate) <= len(translated):
	for i in range(len(to_translate)):
		result[to_translate[i]] = translated[i]
else:
	print('Unmatched to_translate and tranlated lengths!',len(to_translate) , len(translated))

print('Query successful, stacktrace results', len(result))

#this janky function tries to make a guess whether a line is a function definition or not
def is_this_a_cpp_function_def(line):
	line = line.partition('//')[0].strip() #uncomment
	line = line.partition('/*')[0].strip() + line.partition('*/')[2].strip() #more uncomment
	words = line.split()
	if 'inline' in words: #pretty much the only real exception
		return 1
	if ';' in line: #functions are not terminated
		return -2
	if '=' in line: # cant have assignment ops in function
		return -3
	if len(line) < 16: # no really short func defs
		return -4
	if ('(' not in line): #func defs always have parenthesis for parameters
		return -5
	if 'if' in words: #no if's in funcs
		return -6
	if 'for' in words:
		return -7
	if 'while' in words:
		return -8
	if 'switch' in words:
		return -9
	if 'case' in words:
		return -10
	#print ('Func-like line:',line)
	if '::' in line: #
		return 11
	if line.startswith('void'):
		return 12
	return 1000


def getcodeline(path, i):
	#fetches line i of the code, removes double quotes, replace with singles, max length of 80 chars
	#also tries to guess the function name
	try:
		codefile=open(path)
		codelines=codefile.readlines()
		line=codelines[i-1] #because lines are indexed from 1!
		if 'lvm.cpp' in path:
			print ("look we have lvm.cpp here!")
		#try to find a function definition above this:
		funcdefline = i-1
		while((is_this_a_cpp_function_def(codelines[funcdefline]) < 0 ) and (funcdefline >1)):
			funcdefline = funcdefline -1
		
		funcdefdebug = is_this_a_cpp_function_def(codelines[funcdefline])
		if funcdefline <3:
			line = line.strip().replace('\"', '')
			line = line.replace('	', '')
			line = line.replace('\\', '')
			if len(line) > 75:
				line = line[0:74] + '...'
			# print 'got code line:',line
			if len(line) < 1:
				print('got suspiciosly short line', path, i, line)
			shortfuncdef = line
		else:
			print ('Found func (%i) def for line %i at %i %s -> %s'%(funcdefdebug,i-1,funcdefline,line,codelines[funcdefline]))
			#shorten funcdef sanely:
			shortfuncdef = codelines[funcdefline]
			shortfuncdef = shortfuncdef.partition('//')[0].strip()
			shortfuncdef = shortfuncdef.rpartition('(')[0].strip()
			shortfuncdef = shortfuncdef.rpartition(' ')[2].strip()
			print ('Shortfuncdef = ',shortfuncdef)

		codefile.close()
		return shortfuncdef
	except Exception as e:
		print('warning, cant fine code line',path,line)

		return ''

#rewrite the symbols.txt output
outf=open('Symbols.txt','w')
goodline=0
for sleepyline in sleepyfile:
	try:
		(sym, module, address, sourcefile, sourceline)=shlex.split(sleepyline.strip())
		shortaddr=address.strip('[]\"')
		if '439cbf' in sym:
			print ("WAIT A MINUTE")
		try:
			symint = int(sym,0)
			hexaddr = int('0x'+shortaddr,0)
			wtf =  int(0x932011)
			if hexaddr > wtf: #danger zone!
				wtf = wtf + 0
		except:
			pass
		if '?' in sleepyline:
			print ("?",sleepyline)
		if sym in result:
			goodline+=1
			newsourcefile=result[sym].rpartition(':')[0]
			newsourceline=result[sym].rpartition(':')[2]

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

				if 'skirmishAiCallback_DataDirs_getWriteableDir' in shortname:
					shortname = 'LIB:['+ newsourcefile + ':' + newsourceline+']'
				out_line = ' '.join([sym,'"'+module+'"','"'+shortname+'"','"'+path+'"',str(newsourceline)])+'\n'

				outf.write(out_line)
			else:
				if options.addr2linekey in newsourcefile:
					address = newsourcefile.partition(options.addr2linekey)[2]
				else:
					address = 'nosrc_LIB:['+ newsourcefile.rpartition('/')[2] + ':' + newsourceline+']'
				if 'skirmishAiCallback_DataDirs_getWriteableDir' in address:
					address = 'skirmishAiCallback_DataDirs_getWriteableDir_LIB:['+ newsourcefile + ':' + newsourceline+']'
				out_line = ' '.join([sym,'"'+module+'"','"'+address+'"','"'+newsourcefile+'"', newsourceline])+'\n'
				outf.write(out_line)
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
