import argparse

from sys import platform

from pathlib import Path
import subprocess

print('''This is a script to generate Shared Library for F#.
It will be used to generate the F# Shared Library for FABGen.
You can retrieve the Shared Library from the FABGen/output/CMakeFiles folder.''')

parser = argparse.ArgumentParser(description='FABGen')
parser.add_argument('--fsharp', help='Generate Shared Library F#', action='store_true')
parser.add_argument('--cpp', help='Name of your C++ file', required=True)
parser.add_argument('--h', help='Name of your Header file', required=True)

args = parser.parse_args()

if args.cpp:
    directory = Path(__file__).parent.parent
    with open('{}/FABgen/lib/cMakeBuild/cppFile.txt'.format(directory), 'w') as f:
        f.write(args.cpp)
    
if args.h:
    directory = Path(__file__).parent.parent
    with open('{}/FABgen/lib/cMakeBuild/hFile.txt'.format(directory), 'w') as f:
        f.write(args.h)

if args.fsharp:
	directory = Path(__file__).parent.parent
	if platform == "win32":
		subprocess.call(['{}/FABgen/lib/cMakeBuild/gen_DLL.bat'.format(directory)])
	else:
		subprocess.call(['{}/FABgen/lib/cMakeBuild/gen_DYLIB.sh'.format(directory)])