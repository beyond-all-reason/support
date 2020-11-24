#!/usr/bin/env python

from s3o import *
import vertex_cache
import sys
from Tkinter import *
import tkFileDialog
import math
import os

howtoemit=('''const unsigned int count = piece->GetVertexCount();

	if (count == 0) {
		pos = mat.GetPos();
		dir = mat.Mul(float3(0.0f, 0.0f, 1.0f)) - pos;
	} else if (count == 1) {
		pos = mat.GetPos();
		dir = mat.Mul(piece->GetVertexPos(0)) - pos;
	} else if (count >= 2) {
		float3 p1 = mat.Mul(piece->GetVertexPos(0));
		float3 p2 = mat.Mul(piece->GetVertexPos(1));

		pos = p1;
		dir = p2 - p1;
	} else {
		return false;
	}\	//! we use a 'right' vector, and the positive x axis points to the left
	pos.x = -pos.x;
	dir.x = -dir.x;

	return true;
''')


def sizeof_fmt(num):
    for x in ['bytes', 'KB', 'MB', 'GB']:
        if abs(num) < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0
    return "%3.1f%s" % (num, 'TB')



class App:
	def __init__(self, master):
		self.initialdir=os.getcwd()
		master.title('OBJ <--> S3O - By Beherith - Thanks to Muon\'s wonderful s3o library!')
		frame = Frame(master)
		objtos3oframe = Frame(master, bd=1, relief = SUNKEN)
		s3otoobjframe = Frame(master, bd=3, relief = SUNKEN)
		opts3oframe   = Frame(master, bd=3, relief = SUNKEN)

		clearaoframe   = Frame(master, bd=3, relief = SUNKEN)
		printaoframe   = Frame(master, bd=3, relief = SUNKEN)
		generateaoframe   = Frame(master, bd=3, relief = SUNKEN)
		xnormalframe = Frame(generateaoframe, bd=3, relief = SUNKEN)
		aooptsframe = Frame(generateaoframe, bd=3, relief = SUNKEN)
		aooptsframe2 = Frame(generateaoframe, bd=3, relief = SUNKEN)

		swaptexframe   = Frame(master, bd=3, relief = SUNKEN)

		frame.pack()
		objtos3oframe.pack(side=TOP,fill=X)
		s3otoobjframe.pack(side=TOP,fill=X)
		opts3oframe.pack(side=TOP,fill=X)
		clearaoframe.pack(side=TOP,fill=X)
		printaoframe.pack(side=TOP,fill=X)
		generateaoframe.pack(side=TOP,fill=X)
		xnormalframe.pack(side=TOP,fill=X)
		aooptsframe.pack(side=TOP,fill=X)
		aooptsframe2.pack(side=TOP,fill=X)

		swaptexframe.pack(side=TOP,fill=X)
		Button(frame, text="QUIT", fg="red", command=frame.quit).pack(side=TOP)
		
		self.prompts3ofilename=IntVar()
		Button(opts3oframe , text='Optimize s3o', command=self.optimizes3o).pack(side=LEFT)

		#-----AO stuff----
		Button(clearaoframe , text='Clear AO s3o', command=self.clearaos3o).pack(side=LEFT)
		Label(clearaoframe, text='Reset all AO data, or list pieces to remove from:').pack(side=LEFT)
		self.clearaopiecelist = StringVar()
		Entry(clearaoframe,width=32,textvariable=self.clearaopiecelist).pack(side=LEFT)
		self.ao_zerolevel = StringVar()
		self.ao_zerolevel.set("200")
		Label(clearaoframe, text='Set to:').pack(side=LEFT)
		Entry(clearaoframe,width=4,textvariable=self.ao_zerolevel).pack(side=LEFT)


		Button(printaoframe , text='Print AO information', command=self.printaos3o).pack(side=LEFT)

		self.xnormalpath = StringVar()
		self.xnormalpath.set("C:\\Program Files\\xNormal\\3.19.3\\x64\\xNormal.exe")
		Label(xnormalframe, text='Path to xNormal:').pack(side=LEFT)
		Entry(xnormalframe,width=84,textvariable=self.xnormalpath).pack(side=LEFT)

		Label(aooptsframe, text='Groundplate:').pack(side=LEFT)
		self.aotype_building = IntVar()
		Checkbutton(aooptsframe, text='Building (big)', variable=self.aotype_building).pack(side=LEFT)
		self.aotype_flying = IntVar()
		Checkbutton(aooptsframe, text='Flying (none)', variable=self.aotype_flying).pack(side=LEFT)

		self.ao_explode = IntVar()
		Checkbutton(aooptsframe, text='Explode all piecewise', variable=self.ao_explode).pack(side=LEFT)

		self.ao_minclamp = StringVar()
		self.ao_minclamp.set("0")

		Label(aooptsframe, text='Clamp:').pack(side=LEFT)
		Entry(aooptsframe, width=4, textvariable=self.ao_minclamp).pack(side=LEFT)

		self.ao_bias = StringVar()
		self.ao_bias.set("0.0")

		Label(aooptsframe, text='Bias:').pack(side=LEFT)
		Entry(aooptsframe, width=4, textvariable=self.ao_bias).pack(side=LEFT)

		self.ao_gain = StringVar()
		self.ao_gain.set("1.0")

		Label(aooptsframe, text='Gain:').pack(side=LEFT)
		Entry(aooptsframe, width=4, textvariable=self.ao_gain).pack(side=LEFT)

		self.ao_explodepieceslist = StringVar()
		Label(aooptsframe2, text='List of pieces to explode').pack(side=LEFT)
		Entry(aooptsframe2, width=76, textvariable=self.ao_explodepieceslist).pack(side=LEFT)

		Button(aooptsframe2 , text='Get', command=self.getpiecelist).pack(side=LEFT)



		Button(generateaoframe , text='Bake AO with above parameters for (multiple) units', command=self.bakeao).pack(side=BOTTOM)


		#--- end AO stuff

		Label(opts3oframe,text='Removes redundant vertices and performs vertex cache optimization').pack(side=LEFT)
		
		Button(swaptexframe , text='Override texture', command=self.swaptex).pack(side=LEFT)
		Label(swaptexframe,text='Tex1:').pack(side=LEFT)
		self.tex1=StringVar()
		Entry(swaptexframe,width=20,textvariable=self.tex1).pack(side=LEFT)
		Label(swaptexframe,text='Tex2:').pack(side=LEFT)
		self.tex2=StringVar()
		Entry(swaptexframe,width=20,textvariable=self.tex2).pack(side=LEFT)
		
		Button(objtos3oframe , text='Convert OBJ to S3O', command=self.openobj).pack(side=LEFT)
		Checkbutton(objtos3oframe,text='Prompt output filename', variable=self.prompts3ofilename).pack(side=LEFT)
		
		
		Button(s3otoobjframe , text='Convert S3O to OBJ', command=self.opens3o).pack(side=LEFT)		
		self.optimize_for_wings3d=IntVar()
		self.optimize_for_wings3d.set(1)
		
		Checkbutton(s3otoobjframe,text='Optimize for Wings3d', variable=self.optimize_for_wings3d).pack(side=LEFT)

		self.promptobjfilename=IntVar()

		Checkbutton(s3otoobjframe,text='Prompt output filename', variable=self.promptobjfilename).pack(side=LEFT)
		
		self.transform=IntVar()
		Checkbutton(objtos3oframe,text='Transform UV coords:', variable=self.transform).pack(side=LEFT)
		
		Label(objtos3oframe,text='U=').pack(side=LEFT)
		self.transformA=StringVar()
		Entry(objtos3oframe,width=4,textvariable=self.transformA).pack(side=LEFT)
		self.transformA.set('1')
		
		Label(objtos3oframe,text='* U +').pack(side=LEFT)
		self.transformB=StringVar()
		Entry(objtos3oframe,width=4,textvariable=self.transformB).pack(side=LEFT)
		self.transformB.set('0')
		
		Label(objtos3oframe,text='    V=').pack(side=LEFT)
		self.transformC=StringVar()
		Entry(objtos3oframe,width=4,textvariable=self.transformC).pack(side=LEFT)
		self.transformC.set('1')
		
		Label(objtos3oframe,text='* V +').pack(side=LEFT)
		self.transformD=StringVar()
		Entry(objtos3oframe,width=4,textvariable=self.transformD).pack(side=LEFT)
		self.transformD.set('0')
		Label(frame,wraplength=600, justify=LEFT, text ='Instructions and notes:\n1. Converting S3O to OBJ:\n Open an s3o file, and the obj file will be saved with the same name and an .obj extension\n The name of each object in the .obj file will reflect the naming and pieces of the s3o file. All s3o data is retained, and is listed as a series of parameters in the object\'s name.\nExample:\no base,ox=-0.00,oy=0.00,oz=0.00,p=,mx=-0.00,my=4.00,mz=0.00,r=17.50,h=21.00,t1=tex1.png,t2=tex2.png\n ALL s3o info is retained, including piece hierarchy, piece origins, smoothing groups, vertex normals, and even degenerate pieces with no geometry used as emit points and vectors. These emit pieces will be shown as triangles with their correct vertex ordering.\n2. Converting OBJ to S3O:\n The opened .obj file will be converted into s3o. If the piece names contain the information as specified in the above example, the entire model hierarchy will be correctly converted. If it doesnt, then the program will convert each object as a child piece of an empty base object.').pack(side=BOTTOM)

	def openobj(self):
		self.objfile = tkFileDialog.askopenfilename(initialdir= self.initialdir, filetypes = [('Object file','*.obj'),('Any file','*')],multiple = True)
		self.objfile = string2list(self.objfile) 
		for file in self.objfile:
			if 'obj' in file.lower():
				self.initialdir=file.rpartition('/')[0]
				if self.prompts3ofilename.get()==1:
					outputfilename=tkFileDialog.asksaveasfilename(initialdir= self.initialdir,filetypes = [('Spring Model file (S3O)','*.s3o'),('Any file','*')])
					if '.s3o' not in outputfilename.lower():
						outputfilename+='.s3o'
				else:
					outputfilename=file.lower().replace('.obj','.s3o')
				transform=self.transform.get()
				a=b=c=d=0
				if transform==1:
					try:
						a=float(self.transformA.get())
						b=float(self.transformB.get())
						c=float(self.transformC.get())
						d=float(self.transformD.get())
						print '[INFO]','Using an UV space transform U=%.3f * U + %.3f  V=%.3f * V + %.3f'%(a,b,c,d)
					except ValueError:
						print '[WARN]','Failed to parse transformation parameters, ignoring transformation!'
						transform=0
				OBJtoS3O(file, transform,outputfilename,a,b,c,d)

	def opens3o(self):
		self.s3ofile = tkFileDialog.askopenfilename(initialdir= self.initialdir,filetypes = [('Spring Model file (S3O)','*.s3o'),('Any file','*')], multiple = True)
		self.s3ofile = string2list(self.s3ofile) 
		for file in self.s3ofile:
			if 's3o' in file.lower():
				self.initialdir=file.rpartition('/')[0]
				if self.promptobjfilename.get()==1:
					outputfilename=tkFileDialog.asksaveasfilename(initialdir= self.initialdir,filetypes = [('Object file','*.obj'),('Any file','*')])
					if '.obj' not in outputfilename.lower():
						outputfilename+='.obj'
				else:
					outputfilename=file.lower().replace('.s3o','.obj')
				S3OtoOBJ(file,outputfilename,self.optimize_for_wings3d.get()==1)

	def optimizes3o(self):
		self.s3ofile = tkFileDialog.askopenfilename(initialdir= self.initialdir,filetypes = [('Spring Model file (S3O)','*.s3o'),('Any file','*')], multiple = True)
		self.s3ofile = string2list(self.s3ofile) 
		for file in self.s3ofile:
			if 's3o' in file.lower():
				self.initialdir=file.rpartition('/')[0]
				optimizeS3O(file)

	def clearaos3o(self):
		self.s3ofile = tkFileDialog.askopenfilename(initialdir= self.initialdir,filetypes = [('Spring Model file (S3O)','*.s3o'),('Any file','*')], multiple = True)
		self.s3ofile = string2list(self.s3ofile)
		piecelist = self.clearaopiecelist.get()
		piecelist = piecelist.strip().lower().split(',')
		if piecelist == ['']:
			piecelist = []
		ao_zerolevel = float(self.ao_zerolevel.get())
		for file in self.s3ofile:
			if 's3o' in file.lower():
				print '[INFO]','Clearing AO for',file,'piecelist:',piecelist
				clearAOS3O(file, piecelist=piecelist, zerolevel=ao_zerolevel)

	def printaos3o(self):
		self.s3ofile = tkFileDialog.askopenfilename(initialdir= self.initialdir,filetypes = [('Spring Model file (S3O)','*.s3o'),('Any file','*')], multiple = True)
		self.s3ofile = string2list(self.s3ofile)
		piecelist = self.clearaopiecelist.get()
		piecelist = piecelist.strip().lower().split(',')
		ao_zerolevel = float(self.ao_zerolevel.get())
		for file in self.s3ofile:
			if 's3o' in file.lower():
				self.initialdir=file.rpartition('/')[0]
				print '[INFO]','Clearing AO for',file,'piecelist:',piecelist
				printAOS3O(file)

	def swaptex(self):
		self.s3ofile = tkFileDialog.askopenfilename(initialdir= self.initialdir,filetypes = [('Spring Model file (S3O)','*.s3o'),('Any file','*')], multiple = True)
		self.s3ofile = string2list(self.s3ofile) 
		for file in self.s3ofile:
			if 's3o' in file.lower():
				self.initialdir=file.rpartition('/')[0]
				swaptex(file,self.tex1.get(),self.tex2.get())

	def getpiecelist(self):
		self.s3ofile = tkFileDialog.askopenfilename(initialdir= self.initialdir,filetypes = [('Spring Model file (S3O)','*.s3o'),('Any file','*')], multiple = True)
		self.s3ofile = string2list(self.s3ofile)
		datafile = open(
		self.s3ofile[0], 'rb')
		data = datafile.read()
		datafile.close()
		model = S3O(data)
		def recurse_piecenames(piece):
			r = [piece.name]
			for child in piece.children:
				r += recurse_piecenames(child)
			return r
		piecenamelist = recurse_piecenames(model.root_piece)
		self.ao_explodepieceslist.set(','.join(piecenamelist))

	def bakeao(self):
		self.s3ofile = tkFileDialog.askopenfilename(initialdir=self.initialdir,
													filetypes=[('Spring Model file (S3O)', '*.s3o'), ('Any file', '*')],
													multiple=True)
		self.s3ofile = string2list(self.s3ofile)
		explodepiecelist = self.ao_explodepieceslist.get().strip().lower().split(',')
		if explodepiecelist == ['']:
			explodepiecelist = []
		for file in self.s3ofile:
			if 's3o' in file.lower():
				bakeAOS3O(file,
						  self.xnormalpath.get(),
						  isbuilding=bool(self.aotype_building.get()),
						  isflying=bool(self.aotype_flying.get()),
						  explode=bool(self.ao_explode.get()),
						  minclamp=float(self.ao_minclamp.get()),
						  bias = float(self.ao_bias.get()),
						  gain = float(self.ao_gain.get()),
						  explodepieces=explodepiecelist)

def string2list(input_string):
	if '{' not in input_string:# and input_string.count(':')>1:
		return input_string
	input_string = input_string.lstrip('{')
	input_string = input_string.rstrip('}')
	output = input_string.split('} {')
	return output

def S3OtoOBJ(filename,outputfilename,optimize_for_wings3d=True):
	if '.s3o' in filename.lower():
		data=open(filename,'rb').read()
		model=S3O(data)
		model.S3OtoOBJ(outputfilename,optimize_for_wings3d)
		print '[INFO]',"Succesfully converted", filename,'to',outputfilename

def OBJtoS3O(objfile,transform,outputfilename,a,b,c,d):
	if '.obj' in objfile.lower():
		data = open(objfile).readlines()
		if transform==1:
			for line in range(len(data)):
				if data[line][0:2]=='vt':
					s=data[line].split(' ')
					data[line]=' '.join([s[0],str(float(s[1])*a+b),str(float(s[2])*c+d)])
		isobj=True
		model = S3O(data,isobj)
		recursively_optimize_pieces(model.root_piece)
		optimized_data = model.serialize()
		output_file=open(outputfilename,'wb')
		output_file.write(optimized_data)
		output_file.close()
	#	if (self.tex1.get()!='' and self.tex2.get()!=''):
	#		swaptex(outputfilename, self.tex1.get(),self.tex2.get())
		print '[INFO]',"Succesfully converted", objfile,'to',outputfilename
		
def swaptex(filename,tex1,tex2):
	datafile=open(filename,'rb')
	data=datafile.read()
	model=S3O(data)
	model.texture_paths=[tex1,tex2]
	datafile.close()
	print '[INFO]','Changed texture to',tex1,tex2
	output_file=open(filename,'wb')
	output_file.write(model.serialize())
	output_file.close()
	print '[INFO]',"Succesfully optimized", filename

def optimizeS3O(filename):
	datafile=open(filename,'rb')
	data=datafile.read()
	model=S3O(data)
	pre_vertex_count=countvertices(model.root_piece)
	recursively_optimize_pieces(model.root_piece)
	optimized_data = model.serialize()
	datafile.close()
	print '[INFO]','Number of vertices before optimization:',pre_vertex_count,' after optimization:',countvertices(model.root_piece)
	output_file=open(filename,'wb')
	output_file.write(optimized_data)
	output_file.close()
	#allbins = model.root_piece.recurse_bin_vertex_ao()
	#print 'bin\t' + '\t'.join(sorted(allbins.keys()))

	#for i in range(0, 256 / 4):
	#	print '%i\t' % i + '\t'.join(['%04d' % allbins[k][i] for k in sorted(allbins.keys())])

	print '[INFO]',"Succesfully optimized", filename

def printAOS3O(filename):
	datafile = open(filename, 'rb')
	data = datafile.read()
	datafile.close()
	model = S3O(data)
	print '[INFO]', 'AO data in:',filename
	model.root_piece.recurse_bin_vertex_ao()
	print '[INFO]', "Printing done for", filename

def clearAOS3O(filename,piecelist = [], zerolevel = 200):
	datafile = open(filename, 'rb')
	data = datafile.read()
	model = S3O(data)
	pre_vertex_count = countvertices(model.root_piece)
	print '[INFO]', 'AO data before clearing:'
	model.root_piece.recurse_bin_vertex_ao()
	model.root_piece.recurse_clear_vertex_ao(piecelist = piecelist,zerolevel=zerolevel)
	print '[INFO]', 'AO data after clearing:'
	model.root_piece.recurse_bin_vertex_ao(piecelist = piecelist)
	recursively_optimize_pieces(model.root_piece)
	optimized_data = model.serialize()
	datafile.close()
	print '[INFO]', 'Number of vertices before optimization:', pre_vertex_count, ' after optimization:', countvertices(
		model.root_piece)
	output_file = open(filename, 'wb')
	output_file.write(optimized_data)
	output_file.close()
	print '[INFO]', "Succesfully optimized", filename

def delimit(str,a,b):
	return str.partition(a)[2].partition(b)[0]

def bakeAOS3O(filepath, xnormalpath, isbuilding = False, isflying = False, explode = False, minclamp = 0.0, bias = 0.0, gain = 1.0,explodepieces = []):
	basename = filepath.rpartition('.')[0]
	print '=========================working on', basename, '==============================='
	# check if the unit has a unitdef and if that unit is not a flying unit.
	# also, make bigger plates for buildings :)

	mys3o = S3O(open(filepath, 'rb').read())
	objfile = basename + '.obj'
	mys3o.S3OtoOBJ(objfile, optimize_for_wings3d=False)
	print basename, 'flying:', isflying, 'building:', isbuilding
	if not isflying:
		objfilehandle = open(objfile)
		objlines = objfilehandle.readlines()
		objfilehandle.close()
		vertex_cnt = 0
		vnormal_cnt = 0
		uv_cnt = 0
		boundingbox = [0, 0, 0, 0, 0, 0]  # xmin, xmax, ymin, ymax, zmin, zmax

		def bind(coords, boundingbox):
			for axis in range(3):
				boundingbox[2 * axis] = min(boundingbox[2 * axis], coords[axis])
				boundingbox[2 * axis + 1] = max(boundingbox[2 * axis + 1], coords[axis])
			return boundingbox

		for line in objlines:
			if line[0:2] == 'v ':
				boundingbox = bind([float(f) for f in line[2:].strip().split(' ')], boundingbox)
				vertex_cnt += 1
			if line[0:3] == 'vn ':
				vnormal_cnt += 1
			if line[0:3] == 'vt ':
				uv_cnt += 1
		for axis in range(3):  # expand the bounding box by 1 in each direction.
			xz_expand = 1
			if isbuilding and axis != 1:  # dont expand y axis
				xz_expand = 12
			boundingbox[2 * axis] = boundingbox[2 * axis] - xz_expand
			boundingbox[2 * axis + 1] = boundingbox[2 * axis + 1] + xz_expand
		for vertex in ([(boundingbox[0], boundingbox[2], boundingbox[4]),
						(boundingbox[0], boundingbox[2], boundingbox[5]),
						(boundingbox[1], boundingbox[2], boundingbox[5]),
						(boundingbox[1], boundingbox[2], boundingbox[4])]):
			objlines.append('v %f %f %f\n' % vertex)
		for i in range(4):
			objlines.append('vn %f %f %f\n' % (0, 1, 0))
			objlines.append('vt %f %f\n' % (0, 0))
		objlines.append(
			'f ' + ' '.join(['%i/%i/%i' % (vertex_cnt + i, uv_cnt + i, vnormal_cnt + i) for i in [1, 2, 3]]) + '\n')
		objlines.append(
			'f ' + ' '.join(['%i/%i/%i' % (vertex_cnt + i, uv_cnt + i, vnormal_cnt + i) for i in [3, 4, 1]]) + '\n')
		objfilehandle = open(objfile, 'w')
		objfilehandle.write(''.join(objlines))
		objfilehandle.close()
	if explode:
		print 'Separating', basename, 'into pieces for AO bake to avoid excessive darkening on hidden pieces'
		objfilehandle = open(objfile)
		objlines = objfilehandle.readlines()
		objfilehandle.close()
		piececount = -1
		for line_index in range(len(objlines)):
			oldline = objlines[line_index]
			if 'v ' == oldline[0:2]:
				oldline = oldline.split(' ')  # we are only gonna replace the Y coords with origY+piececount*100
				objlines[line_index] = 'v %s %f %s' % (
				oldline[1], float(oldline[2]) + 100.0 * piececount, oldline[3])
			if 'o ' == oldline[0:2]:
				piececount += 1

		objfilehandle = open(objfile, 'w')
		objfilehandle.write(''.join(objlines))
		objfilehandle.close()


	# DO THE XNORMAL:
	xnormalcmd = '""%s" -aogpu "%s" 0 1.0 pv "%s" 512 512 2048 0.008 0.0 1.0 1.0 1.0 0 2 cpu true 172.0 0.0 0.0 0.0"'%(
		xnormalpath,
		basename+'.obj',
		basename+'.ovb'
	)
	print "[INFO]",'xNormal command is:',xnormalcmd
	os.system(xnormalcmd)

	aovalues = {}

	def parse_ovb_triplet(line):
		line = line.strip().replace('\"', '').strip('<>/').split(' ')
		vertex = []
		for coord in line[1:]:
			vertex.append(float(coord.partition('=')[2]))
		return vertex


	print  'Working on:', filepath
	vertdata = []
	aodata = []
	ovbfile = open(basename+'.ovb').readlines()
	aobins = [0 for i in range(256)]
	vcount = 0

	for line in ovbfile:
		if '<VPos' in line:
			vertdata.append(parse_ovb_triplet(line))
		if '<VCol' in line:
			aodata.append(parse_ovb_triplet(line))
	aomax = 0
	for ao in aodata:
		aobins[int(sum(ao) / 3)] += 1
		aomax = max(aomax, aobins[int(sum(ao) / 3)])

	#for aoval in range(256):  # just display it
		#print aoval, 'O' * int(math.ceil(80 * aobins[aoval] / aomax))
	print "Number of vertices in each AO bin:",aomax, aobins, 'total=',sum(aobins)
	# ao

	olds3ofile = open(basename +  '.s3o', 'rb')
	olds3o = S3O(olds3ofile.read())
	olds3ofile.close()
	for i in range(len(aodata)):
		aodata[i] = sum(aodata[i]) / 3.0

	def recursefoldaoterm(piece, vertex_offset, ignore_these):
		# global ignorepieces
		print 'folding ao terms for', piece.name, 'current offset=', vertex_offset
		ignore = False
		if piece.name.lower() in ignore_these:
			print 'ignoring', piece.name
			ignore = True
		folded_vert_indices = []
		for vertex_i in range(len(piece.indices)):
			if piece.indices[vertex_i] in folded_vert_indices:
				# print 'already did',piece.indices[vertex_i]
				continue
			else:
				folded_vert_indices.append(piece.indices[vertex_i])
				vertex = piece.vertices[piece.indices[vertex_i]]
				# print vertex_offset,len(folded_vert_indices), vertex_i, len(aodata), vertex

				# dont use the entire range, because rounding errors might screw us over later, use only the range from 5-250
				vertex_ao_value = aodata[len(folded_vert_indices) - 1 + vertex_offset]
				vertex_ao_value = min(max(minclamp,vertex_ao_value*gain + bias),255)
				if ignore:
					vertex_ao_value = 200
				newuv = (math.floor(vertex[2][0] * 16384.0) / 16384.0 + 1 / 16384.0 * ((vertex_ao_value + 5) / 266.0),
						 vertex[2][1])
				# print newuv, vertex
				vertex = (vertex[0], vertex[1], newuv)
				piece.vertices[piece.indices[vertex_i]] = vertex
		print 'finished folding ao terms for', piece.name, 'unique vertex count=', len(folded_vert_indices)
		vertex_offset += len(folded_vert_indices)
		for child in piece.children:
			childoffset = recursefoldaoterm(child, vertex_offset, ignore_these)
			print 'in child, vertex offset=', vertex_offset, 'child_offset=', childoffset
			vertex_offset = childoffset
		return vertex_offset

	# parse bos for spin pieces
	ignorepieces = explodepieces
	recursefoldaoterm(olds3o.root_piece, 0, ignorepieces)
	news3ofile = open(basename + '.s3o', 'wb')
	news3ofile.write(olds3o.serialize())
	news3ofile.close()
	print '[INFO]',"Ding, fries are done!"

def countvertices(piece):
	numverts=len(piece.vertices)
	for child in piece.children:
		numverts+=countvertices(child)
	return numverts

#def swaptex(filename,tex1,tex2):
chickenlist = """chicken2b.s3o	chicken_apex_m_color.dds	chicken_m_other.png
h_chickenq.s3o	chicken_apex_large_color.dds	chicken_large_other.png
chickenc.s3o	chicken_aqua_m_color.dds	chicken_m_other.png
big_chicken_dodo.s3o	chicken_black_m_color.dds	chicken_m_other.png
chickenc2.s3o	chicken_black_m_color.dds	chicken_m_other.png
chicken_listener.s3o	chicken_black_m_color.dds	chicken_m_other.png
epic_chickenq.s3o	chicken_black_large_color.dds	chicken_large_other.png
chickenr.s3o	chicken_blue_s_color.dds	chicken_s_other.png
chickenr.s3o	chicken_blue_s_color.dds	chicken_s_other.png
chicken_colonizer.s3o	chicken_blue_l_color.dds	chicken_l_other.png
e_chickenq.s3o	chicken_brown_l_color.dds	chicken_l_other.png
chicken.s3o	chicken_1_s_color.dds	chicken_s_other.png
chicken_pidgeon.s3o	chicken_1_m_color.dds	chicken_m_other.png
chicken1b.s3o	chicken_1b_s_color.dds	chicken_s_other.png
chicken_pidgeonb.s3o	chicken_1b_m_color.dds	chicken_m_other.png
chicken1c.s3o	chicken_1c_s_color.dds	chicken_s_other.png
chicken_pidgeonc.s3o	chicken_1c_m_color.dds	chicken_m_other.png
chicken1d.s3o	chicken_1d_s_color.dds	chicken_s_other.png
chicken_pidgeond.s3o	chicken_1d_m_color.dds	chicken_m_other.png
chicken1x.s3o	chicken_1x_s_color.dds	chicken_s_other.png
chicken1y.s3o	chicken_1y_s_color.dds	chicken_s_other.png
chicken1z.s3o	chicken_1z_s_color.dds	chicken_s_other.png
chickenc3.s3o	chicken_c3_s_color.dds	chicken_s_other.png
chickenc3b.s3o	chicken_c3b_s_color.dds	chicken_s_other.png
chickenc3c.s3o	chicken_c3c_s_color.dds	chicken_s_other.png
s_chicken_white.s3o	chicken_crimson_s_color.dds	chicken_s_other.png
chickenq.s3o	chicken_crimson_large_color.dds	chicken_large_other.png
chickens.s3o	chicken_green_m_color.dds	chicken_m_other.png
spiker_gunship.s3o	chicken_green_m_color.dds	chicken_m_other.png
s_chickenboss_white.s3o	chicken_multi_l_color.dds	chicken_l_other.png
chicken2.s3o	chicken_pink_m_color.dds	chicken_m_other.png
chicken_dodo.s3o	chicken_red_s_color.dds	chicken_s_other.png
chickena.s3o	chicken_red_l_color.dds	chicken_l_other.png
chickenab.s3o	chicken_redb_l_color.dds	chicken_l_other.png
chickena2b.s3o	chicken_redb_l_color.dds	chicken_l_other.png
s_chickenboss2_white.s3o	chicken_redb_l_color.dds	chicken_l_other.png
chickenac.s3o	chicken_redc_l_color.dds	chicken_l_other.png
chickena2.s3o	chicken_redc_l_color.dds	chicken_l_other.png
brain_bug.s3o	chicken_redhead4_l_color.dds	chicken_l_other.png
chicken_crow.s3o	chicken_vcrimson_m_color.dds	chicken_m_other.png
vh_chickenq.s3o	chicken_vcrimson_large_color.dds	chicken_large_other.png
ve_chickenq.s3o	chicken_white_large_color.dds	chicken_large_other.png
chickenf1.s3o	chicken_white_m_color.dds	chicken_m_other.png
chicken_drone.s3o	chicken_white_s_color.dds	chicken_s_other.png
chicken_droneb.s3o	chicken_whitehc_s_color.dds	chicken_s_other.png
chickenf.s3o	chicken_yellow_l_color.dds	chicken_l_other.png
chickens2.s3o	chicken_yellow_m_color.dds	chicken_m_other.png
chickenf1b.s3o	chicken_yellowb_l_color.dds	chicken_l_other.png"""

flyers = """chicken_crow.s3o
chicken_pidgeon.s3o
chicken_pidgeonb.s3o
chicken_pidgeonc.s3o
chicken_pidgeond.s3o
chickenf1.s3o
chickenf1b.s3o
spiker_gunship.s3o
chickenf.s3o"""
'''
flyers = flyers.split('\n')
for line in chickenlist.split('\n'):
	linesp = line.strip().split('\t')
	path = ("C:/Users/Peti/Documents/my games/Spring/games/Beyond-All-Reason.sdd/objects3d/Chickens/"+linesp[0])
	swaptex(path, linesp[1],linesp[2])
	bakeAOS3O(path,"C:\\Program Files\\xNormal\\3.19.3\\x64\\xNormal.exe",isflying= (linesp[0] in flyers))
exit(1)
'''
root = Tk()
app = App(root)
root.mainloop()