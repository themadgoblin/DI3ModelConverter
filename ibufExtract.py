import os
import struct
import sys
import numpy as np

vertexArray = []
uvArray = []
polyArray = []

numberOfVertex = 0

class PolyStruct:
    def __init__(self, bytes):
        self.first, self.second, self.third = struct.unpack('hhh',bytes)
        self.first=self.first+1
        self.second=self.second+1
        self.third=self.third+1
class UvStruct:
    def __init__(self, u, v):
        self.u = u
        self.v = 1-v

class VertexStruct:
    def __init__(self, bytes):
        self.x, self.y, self.z = struct.unpack('fff',bytes)
        # self.x, self.y, self.z , self.u, self.v, self.unknown, self.vertexcolor = struct.unpack('fffhhff',bytes)


ibufFilename=sys.argv[1]
vbufFilename=sys.argv[2]

# ibuf handling

print ("#Reading ibuf file")

file_length_in_bytes = os.path.getsize(ibufFilename)
print("#" + ibufFilename+" size:" + str(file_length_in_bytes) + " bytes")

with open(ibufFilename, "rb") as binary_file:
    binary_file.seek(0, 0)
    numberOfPolys = file_length_in_bytes / 6  # Each polygon is formed by 3 vertex. Each vertex id uses 2 bytes -> 6 bytes (firstVertexId, secondVertexId, thirdVertexId) Example from a triangle: 00 00 01 00 02 00
    for polyNumber in range(0,int(numberOfPolys)): # Since we dont know the number of vertex in the file, we just iterate through it and find the highest number
        chunk = binary_file.read(6)
        asd = PolyStruct(chunk) # We read a chunk of 6 bytes and transform it on a PolyStruct.
        polyArray.append(asd) # and we keep that poly struct on the polyarray
        #print ("f "+ str(asd.first) + "/" + str(asd.first) + " " + str(asd.second) + "/" + str(asd.second) + " " + str(asd.third) + "/" + str(asd.third))

        if asd.first>numberOfVertex:
            numberOfVertex=asd.first

        if asd.second>numberOfVertex:
            numberOfVertex=asd.second

        if asd.third>numberOfVertex:
            numberOfVertex=asd.third

print ("# Number of vertex found: " + str(numberOfVertex))   # HACK: we should read this from the .oct file instead


# vbuf handling
print ("#Reading vbuf file")

file_length_in_bytes = os.path.getsize(vbufFilename)
print("#" + vbufFilename+" size:" + str(file_length_in_bytes) + " bytes")

with open(vbufFilename, "rb") as binary_file:
    binary_file.seek(0, 0)
    #numberOfVertex = file_length_in_bytes / 16
    for polyNumber in range(0,int(numberOfVertex)):
        print ("#DEBUG vertex "+str(polyNumber)+" structure offset : " + str(binary_file.tell()) )
        chunk = binary_file.read(12) # 12 bytes that form the X,Y,Z coordinates of this vertex. Each coordinate is represented with a float (4 bytes)
        uCoords = binary_file.read(2) # READ THIS http://fpmurphy.blogspot.com/2008/12/half-precision-floating-point-format_14.html
        vCoords = binary_file.read(2) # READ THIS http://fpmurphy.blogspot.com/2008/12/half-precision-floating-point-format_14.html

        asd = VertexStruct(chunk)
        vertexArray.append(asd)

        asd = UvStruct(np.frombuffer(uCoords, dtype=np.float16)[0].astype(float),np.frombuffer(vCoords, dtype=np.float16)[0].astype(float)) # READ THIS http://fpmurphy.blogspot.com/2008/12/half-precision-floating-point-format_14.html
        uvArray.append(asd)

        # FOR DEBUG
        # print ("#" + chunk.hex())

        # MISTERY DATA
    for polyNumber in range(0,int(numberOfVertex)):
        #print ("#DEBUG Mistery "+str(polyNumber)+" structure offset : " + str(binary_file.tell()) )
        mistery1 = binary_file.read(4)
        mistery2 = binary_file.read(4)

        print("# Offset:" + str(binary_file.tell()) + " Mistery 1: " + mistery1.hex() + " Mistery 2: " + mistery2.hex())


print ("#Number of vertex: " + str(len(vertexArray)))
for vertex in range(0,len(vertexArray)):
    print ("v " + str(vertexArray[vertex].x) + " " + str(vertexArray[vertex].y) + " " + str(vertexArray[vertex].z) + " " )

print("")

print ("#Number of uv: " + str(len(uvArray)))
for vertex in range(0,len(uvArray)):
    print("vt " + str(uvArray[vertex].u) + " " + str(uvArray[vertex].v) + " 0") #HACK appending a - to negate the V coords

print("")

print ("#Number of polys: " + str(len(polyArray)))
for poly in range(0,len(polyArray)):
    print ("f "+ str(polyArray[poly].first) + "/" + str(polyArray[poly].first) + " " + str(polyArray[poly].second) + "/" + str(polyArray[poly].second) + " " + str(polyArray[poly].third) + "/" + str(polyArray[poly].third))
