import os
import sys
import argparse
import random

#global variables
filePath = ""	# path to the 'security' file
counter = 0	# global counter for filenames
log = False	# boolean for if we should log


def debug(str):
	if log:
		print(str)



# takes a directory list and removes @name and reinserts it with a different value. also renames the file
# @fileName = file to rename and reinsert
# @items = the list where we filter
# returns a new list
def resolveNameConflict(items,fileName):
	debug("\tConflict for: " + fileName)

	if (os.path.isdir(fileName)):
		print("error: a directory name is just a number.\n This is an edge case that is not yet handled.")
		sys.exit()

	# for a prefix, it will increment if the prefix + name is already taken
	prefixCounter = -1 # will be incremented before use
	prefix = "tmp" + str(prefixCounter) + "_"	

	path, newName = os.path.split(fileName)

	while (os.path.exists(os.path.join(path,newName))): # do till we find a free file name
		prefixCounter = prefixCounter + 1
		prefix = "tmp" + str(prefixCounter) + "_"

		newName = prefix + os.path.basename(fileName)
	
	debug("\tconflict solution: " + fileName + " -> " + os.path.join(path,newName))

	try:
		os.rename(fileName, os.path.join(path,newName)) # rename the file
	except IOError:
		print("could not rename, check if the progamm has permission, or if the file is in use")


	# update list
	if (fileName in items):
		items.remove(fileName)
	items.append(str(newName))
	
	return items


# randomizes all files in the directory set in 'path'
# @path = directory path for the files to be randomized
# returns an list of directories
def randomizer_work(path): # does the actual work
	
	global counter

	subdirs = []

	items = os.listdir(path)
	random.shuffle(items) # add randomness

	debug("\nfiles to rename: " + str(items) + "\n")

	while len(items) != 0: # for every item, but the items will change mid loop.
		item = os.path.join(path,items[0])

		if (os.path.isdir(item)):
			subdirs.append(item)

		if (os.path.basename(item) == "fileRandomizer.py" or os.path.basename(item) == ".FileRandomizerEnable"):
			items.remove(os.path.basename(item))
			continue

		if (os.path.isfile(item)):
			fileExtension = os.path.splitext(item)[1]

			newFileName = os.path.join(path, str(counter) + fileExtension)

			debug("preparing: " + item + " -> " + newFileName)
			if (item == newFileName): # edge case where file gets renamed to itself
				items.remove(os.path.basename(item))
				debug("\tNo change")
				continue

			if (os.path.exists(newFileName)): # if the file already exists, rename it
				items = resolveNameConflict(items,newFileName)

			debug("\texecuting: "+ item + " -> " + newFileName)
			
			try:
				os.rename(item, newFileName)
			except IOError:
				print("could not disable, check if the progamm has permission, or if the file is in use")

			counter = counter + 1
		
		items.remove(os.path.basename(item))



	print(path)
	return subdirs


# calls  "randomizer". used to handle recursion without killing the stack
# @path = directory path for the files to be randomized
# @recursive = boolean of if we also want to affect sub directories
# @noCheck = if we Check if the directory is enabled
# returns nothing
def randomizer(path, recursive, noCheck): 
	if (recursive == False):
		if (os.path.exists(filePath)):
			randomizer_work(path)
		else:
			print(path+" is not enabled for renaming")
		return None

	# recursive = true

	# todo in the future.
	# not sure if I will ever add it
	
	
	


def main():

	parser = argparse.ArgumentParser(
                    prog='File Name Randomizer',
                    description='Randomizes all filenames in a directory, only works on directories marked with a file, to minimize accidents.',
                    epilog='')
	
	parser.add_argument('directory', default='.')           # positional argument
	
	parser.add_argument('-nsec', 	'--noSecurity',	action='store_true', help='does not check for the \'security\' file')  # on/off flag
	parser.add_argument('-e', 	'--enable',	action='store_true', help='Enables this tool for the provided directory')  # on/off flag
	parser.add_argument('-d', 	'--disable',	action='store_true', help='Disables this tool for the provided directory')  # on/off flag
	parser.add_argument('-l', 	'--log',	action='store_true', help='Enables debug logs')  # on/off flag
	#parser.add_argument('-r', 	'--recursive',	action='store_true', help='includes subdirectories (but only if they are also enabled)')  # on/off flag

	args = parser.parse_args()

	global log
	log = args.log

	if not (os.path.isdir(args.directory)):
		print("error: directory parameter must be a directory!")

		sys.exit()


	# path to the 'security' file
	global filePath
	filePath = os.path.join(args.directory,".FileRandomizerEnable")

	if (args.enable == True):
		# create file, if it does not exist, and exit.

		try:
			file = open(filePath,'a+')
			file.close()
		except IOError:
			print("could not disable, check if the progamm has permission, or if the file is in use")
		sys.exit()

	if (args.disable == True):
		#delete file and exit

		if (os.path.exists(filePath)):
			try:
				os.remove(filePath)
			except IOError:
				print("could not disable, check if the progamm has permission, or if the file is in use")
		sys.exit()
			

	# run randomizer and exit
	#randomizer(args.directory, args.recursive, args.noSecurity)
	randomizer(args.directory, False, args.noSecurity)	
	sys.exit()


main()

