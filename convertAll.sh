#! /bin/bash

folder=$1

python.exe ibufExtract.py $1/$1_0.ibuf $1/$1_0.vbuf >$1/$1_0.obj
python.exe reader.py $1/$1.oct >$1/$1.oct.dec
python.exe reader.py $1/$1.mer >$1/$1.mer.dec

