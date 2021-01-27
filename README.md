# DI3ModelConverter
Scripts for transforming model files found on DI3 Gold PC (ibuf,vbuf...) to OBJ and back.

[Proof of it working](https://www.youtube.com/watch?v=t_7Tq_7TNe8)

**Requires Python3 and numpy**


**Disclaimer**
These scripts probably work ok for transforming ibuf+vbuf files to OBJ, but will **NOT** work directly for converting OBJ files to game files.
MODIFICATIONS MUST BE DONE TO MAKE THESE WORK


## Description



reader.py - Disney Infinity .oct .bent .banm .mer reader. Author: zzh8829

example.py - Example code for using half precision floating point numbers on python. Author: unknown

objConverter.py - Reads obj file to recreate ibuf and vbuf files. Author: Eidan Yoson. IT WILL NOT WORK UNLESS YOU KNOW WHAT ARE YOU DOING.

ibufExtract.py - Reads an ibuf and vbuf files and outputs in terminal an ascii OBJ file. Author: Eidan Yoson.  This file contains A LOT of debug information that can be useful to continue reversing the file format, just open it on a text editor.


## Usage:

python3 ibufExtract.py [ibufFilename] [vbufFilename] >output.obj 

Example: Dump the OBJ file into terminal. 

`python3 ibufExtract.py tdu_beachball/tdu_beachball_0.ibuf tdu_beachball/tdu_beachball_0.vbuf`

Example 2:

`python3 ibufExtract.py tdu_beachball/tdu_beachball_0.ibuf tdu_beachball/tdu_beachball_0.vbuf >tdu_beachball/tdu_beachball.obj`
