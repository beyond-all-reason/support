import os
import sys
import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument('-f','--filter', type =str, help = 'Which imagemagick resize filter to use, default Lanczos, see: https://legacy.imagemagick.org/Usage/filter/#windowed', default = 'Lanczos')
parser.add_argument('-i','--input', type=list, nargs = '+' ,action = 'store', help = 'Which files to process, default cor_color.png cor_other.png cor_normal.png', default = ['arm_color.tga','arm_other.tga', 'arm_normal.tga'])
parser.add_argument('-s', '--size', type = int, help = "Size of the image to determine number of mipmaps default 4096", default = 4096)
parser.add_argument('-d', '--ddsformat', type = str, help = "Which DDS format to use, one of [dxt5, dxt1] etc, default dxt5", default = 'dxt5')
parser.add_argument('-a', '--alpha', type = str, help = "Use alpha or not, [on,off] , default on", default = 'on')
parser.add_argument('-c', '--chain', action = 'store_true', help = "Resize stepwise, with the next mip coming from the previous one, default off")
parser.add_argument('-v', '--vflip', action = 'store_true', help = "Vertically flip image, default off")

args = parser.parse_args()
print("Arguments", str(args))

ddsformat = '-define dds:compression='+args.ddsformat
ddsmips = '-define dds:mipmaps=fromlist '

inext = 'png'
outext = 'tga'
nmips = math.ceil(math.log(args.size,  2))

flip = '-flip'
if args.vflip:
	flip = '-flip'

filt = args.filter
#notes on filters:
#https://legacy.imagemagick.org/Usage/filter/#windowed
#Lanczos: quite good, near identical on chain and non-chain

alpha = "-alpha "+args.alpha

def execute(cmd):
	print('Executing: ' + cmd)
	os.system(cmd)
	
def converttodds(fname,args):
	infile = fname.rpartition('.')[0]
	inext =  fname.rpartition('.')[2]
	print (f'Processing {infile} chain = {args.chain}')
	# regular resize
	imsize = args.size
	if args.chain == False:
		for i in range(nmips+1):
			execute(f'magick convert {infile}.{inext} {alpha} -channel RGBA -separate -filter {filt} -resize {imsize}x{imsize} -combine {infile}_mips_{filt}_{i:02d}.{outext}')
			imsize = imsize // 2 

		# assemble unchained:
		execute('magick convert '+ ' '.join([f'{infile}_mips_{filt}_{i:02d}.{outext}' for i in range(nmips+1)]) + f' {flip} {ddsformat} {ddsmips} {infile}.dds')

	else:	
		# chain resize
		#make first one in chain:
		execute(f'magick convert {infile}.{inext} {alpha} -filter {filt} {infile}_mips_{filt}_chain_00.{outext}')
		for i in range(nmips): 
			execute(f'magick convert {infile}_mips_{filt}_chain_{i:02d}.{outext} {alpha}  -channel RGBA -separate -filter {filt} -resize 50% -combine {infile}_mips_{filt}_chain_{(i+1):02d}.{outext}')

		#assemble chained:
		execute('magick convert '+ ' '.join([f'{infile}_mips_{filt}_chain_{i:02d}.{outext}' for i in range(nmips+1)]) + f' {flip} {ddsformat} {ddsmips} {infile}_{filt}_chain.dds')

for img in args.input:
	converttodds(img, args)

