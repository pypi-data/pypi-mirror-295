import os, argparse
from pathlib import Path
from AssetPacker import AssetPacker

# Parse arguments from commandline
argument_parser = argparse.ArgumentParser(description='')

argument_parser.add_argument('-output', nargs=1, help="")
argument_parser.add_argument('-include', nargs="+",  help="")
arguments = argument_parser.parse_args()

absolutePath = os.path.abspath(arguments.output[0])
parentPath = Path(absolutePath).parent
os.makedirs(parentPath, exist_ok=True)

packer = AssetPacker()
packer.setOutput(absolutePath)

if arguments.include != None:
    for include in arguments.include:
        absoluteInclude = os.path.abspath(include)
        packer.add(absoluteInclude)

packer.scan()

for file in packer.getFiles():
    print(file.location + " (" + file.file + ")")

if packer.needsUpdate():
    print("Generating...")
    packer.generate()
    print("Done")
else:
    print("No update needed")
