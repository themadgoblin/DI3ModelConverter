import os
import struct
import sys
import numpy as np

## READ THIS DUMBASS
## https://forum.xentax.com/viewtopic.php?t=11187
## BUGS TO FIX: UV coordinates on the index can be repeated. The converter will fail if all the vertex dont have their own UV unique coordinate. This means X vertex = X UV coordinate pairs.


objFilename=sys.argv[1]
ibufFilename=objFilename.split('.')[0] + "CONV.ibuf"
vbufFilename=objFilename.split('.')[0] + "CONV.vbuf"

vertexArray = []
vertexUvArray = []  # index array of UV coordinates that will be used for this polygon. It goes to the ibuf
uvArray = []

polyArray = []


print ("Reading obj file")
file_length_in_bytes = os.path.getsize(objFilename)
print("" + objFilename+" size:" + str(file_length_in_bytes) + " bytes")


# Parsing the OBJ file and filling the arrays
objFile = open(objFilename, 'r')
line = objFile.readline()
while line:
    #print(line)
    line = objFile.readline()
    if line.startswith("vt "):
        # print("#UV found")
        uvArray.append(line)
    if line.startswith("v "):
        # print("#Vertex found")
        vertexArray.append(line)
    if line.startswith("f "):
        # print("#Polygon found")
        polyArray.append(line)

print ("Closing obj file")
objFile.close()

# Show some stats about what was found
print("UVs:" + str(len(uvArray)))
print("Vertex:" + str(len(vertexArray)))
print("Polygons:" + str(len(polyArray)))


print ("Parsing and writing the ibuf file")

# Preparing to write the ibuf file on the go
with open(ibufFilename, "wb") as ibuf_File:


# Parsing the polygon array. v1 v2 v3 contain the vertex indexes used for creating the triangle. DANGER: We are assuming that the OBJ file ONLY uses triangles.
    for triangle in polyArray:
        # print(triangle)

        # Transforming "1/1 2/2 3/3" into 1 2 3. Also substracting 1 because vertexarrays start on 0
        triangleVertexList=triangle.split()
        print("Triangle")
        print(triangleVertexList)
        v1=int(triangleVertexList[1].split('/')[0])-1  # We start from 1 because 0 is 'f'
        uv1=int(triangleVertexList[1].split('/')[1])-1 # We start from 1 because 0 is 'f'

        v2=int(triangleVertexList[2].split('/')[0])-1
        uv2=int(triangleVertexList[2].split('/')[1])-1

        v3=int(triangleVertexList[3].split('/')[0])-1
        uv3=int(triangleVertexList[3].split('/')[1])-1

        #DEBUG
        print("Vertex index")
        print(v1)
        print(v2)
        print(v3)

        print("UV index")
        print(uv1)
        print(uv2)
        print(uv3)

        # print("UV Coordinates")
        # print("Vertex 1 UV:")
        # print(uvArray[uv1])
        # print("Vertex 2 UV:")
        # print(uvArray[uv2])
        # print("Vertex 3 UV:")
        # print(uvArray[uv3])

        # Appending the uvdata used by that vertex to the array
        vertexUvArray.append([uv1,uv2,uv3])

        # print("vertexUvArray Length")
        # print(len(vertexUvArray))

        # ibuf file format is basically an array of blocks with 3 shorts (2 bytes each) that point to the vertex number that is used for generating that triangle
        binaryData=struct.pack('hhh',v1,v2,v3)
        ibuf_File.write(binaryData)

ibuf_File.close()

print ("Parsing and writing the vbuf file")

# Preparing to write the vbuf file on the go

with open(vbufFilename, "wb") as vbuf_File:

    for position,vertex in enumerate(vertexArray):
        print("Vertex on OBJ file:" + vertex)

        # Transforming "v -0.05897863209247589 -0.6335211992263794 0.08117648959159851" into separate values for X Y Z
        vertexCoordinates=vertex.split()
        x=float(vertexCoordinates[1])
        y=float(vertexCoordinates[2])
        z=float(vertexCoordinates[3])

        print("Vertex number:" + str(position))
        print(x)
        print(y)
        print(z)

#        print("UV Index")
#        print(vertexUvArray[position][0])
#        print(vertexUvArray[position][1])
#        print(vertexUvArray[position][2])


#        print("Debug stuff")
#        print(uvArray[position])

        print("UV coordinates")
        # Retrieving the UV coordinates OLD
        uvCoordinates=uvArray[position].split()
        u=np.float16(float(uvCoordinates[1]))
        v=np.float16(1.0-float(uvCoordinates[2]))
        #v=np.float16(1.0-float(uvCoordinates[2]))
        print(uvCoordinates[1])
        print(uvCoordinates[2])
        print(u)
        print(v)



        #     def __init__(self, u, v):
                # self.u = u
                # self.v = 1-v <<<<<<<<<<<<<<<<<<<<<<<<<- THIS WILL BITE MY ASS <<<<<<<< (26/02/2021) Thanks madgoblin from the past
        #         asd = UvStruct(  np.frombuffer(uCoords, dtype=np.float16)[0].astype(float)    ,   np.frombuffer(vCoords, dtype=np.float16)[0].astype(float)  )


        # vbuf file structure is a block [[float x][float y][float z][half float U coordinates ][half float V coordinates]][RANDOM UNKNOWN STUFF HERE ARE DRAGONS]
        binaryData=struct.pack('fff',x,y,z) #writting the X Y Z Coords
        vbuf_File.write(binaryData)
        vbuf_File.write(u.tobytes())
        vbuf_File.write(v.tobytes())


    # writting the mistery stuff
    for vertex in range(0,len(vertexArray)):
        print(vertex)
        vbuf_File.write(b'0000000000000000')

vbuf_File.close()
