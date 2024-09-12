import glob, os
from pathlib import Path

def fixedHash(string : str):
  hash = 0
  for character in string:
    hash = (hash * 281 ^ ord(character) * 997) & 0xFFFFFFFF
  return hash

class AssetFilter:
    def __init__(self, directory, filter, root):
        self.directory = directory
        self.filter = filter
        self.root = root

class AssetLocation:
    def __init__(self, file, location):
        self.file = file
        self.location = location
        self.hash = fixedHash(self.location)

class AssetPacker:
    def __init__(self):
        self.output = ""
        self.filters = []
        self.files = []
        self.hash = 0

    def setOutput(self, output):
        self.output = output

    def add(self, directory, filter="*.*", root = "/"):
        self.filters += [AssetFilter(directory, filter, root)]

    def scan(self):
        self.files = []

        hashString = str(os.path.getmtime(__file__))

        for filter in self.filters:
            for file in glob.glob(filter.directory + "/**/*.*", recursive=True):
                relativeLocation = os.path.relpath(file, filter.directory)
                assetLocation = filter.root + relativeLocation
                assetLocation = assetLocation.replace("\\", "/")
                self.files += [AssetLocation(file, assetLocation)]
                hashString += str(os.path.getmtime(file))
                
        self.hash = fixedHash(hashString)

    def getFiles(self):
        return self.files
    
    def needsUpdate(self):
        outputExists = os.path.exists(self.output + ".hpp") and os.path.exists(self.output + ".cpp")
    
        hashSame = False
        hashFile = self.getCacheLocation()
        if os.path.exists(hashFile):
            f = open(self.getCacheLocation(), "r")
            hash = int(f.read())
            f.close()
            hashSame = hash == self.hash

        return not outputExists or not hashSame
    
    def getCacheLocation(self):
        directory = Path(self.output).parent
        filename = os.path.basename(self.output)
        return str(directory) + "/." + filename + ".assetcache"

    def generate(self):
        if not self.needsUpdate():
            return

        f = open(self.output + ".hpp", "w")
        f.write("#pragma once\n\n")
        f.write("typedef unsigned long AssetIdentifier;\n\n")
        f.write("extern AssetIdentifier getAssetCount();\n")
        f.write("extern const char* getAssetLocation(AssetIdentifier asset);\n")
        f.write("extern void* getAssetBuffer(AssetIdentifier asset);\n")
        f.write("extern unsigned long getAssetBufferSize(AssetIdentifier asset);\n")
        f.close()

        f = open(self.output + ".cpp", "w")
        f.write("#include \"" + os.path.basename(self.output) + ".hpp\"\n\n")

        for file in self.files:
            f.write("unsigned char assetBuffer" + str(abs(file.hash)) + "[] = {")

            size = 0
            fileStream = open(file.file, "rb") 
            while (byte := fileStream.read(1)):
                f.write("0x" + byte.hex() + ",")
                size += 1
            fileStream.close()
            f.write("};\n")
            f.write("unsigned long assetSize" + str(abs(file.hash)) + " = " + str(size) + ";\n")
           
        f.write("\nstruct Asset { const char* location; unsigned char* buffer; unsigned long bufferSize; };\n")
        
        for file in self.files:
            f.write("Asset asset" + str(abs(file.hash)) + " = { \"" + file.location + "\", assetBuffer" + str(abs(file.hash)) + ", assetSize" + str(abs(file.hash)) + " };\n")
        
        f.write("\nAssetIdentifier getAssetCount() { return " + str(len(self.files)) + "; }\n")
        f.write("Asset* assetList[] = {")
        for file in self.files:
            f.write("&asset" + str(abs(file.hash)) + ",")
        f.write("};\n")
       
        f.write("const char* getAssetLocation(AssetIdentifier id) { return assetList[id]->location; }\n")
        f.write("void* getAssetBuffer(AssetIdentifier id) { return assetList[id]->buffer; }\n")
        f.write("unsigned long getAssetBufferSize(AssetIdentifier id) { return assetList[id]->bufferSize; }\n")
        f.close()

        f = open(self.getCacheLocation(), "w")
        f.write(str(self.hash))
        f.close()
 