# MIT License
#
# Copyright (c) 2020 Oli Wright <oli.wright.github@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# makespc.py
#
# Simple script to convert images to the Stop Press Canvas .SPC format which
# is used on Amstrad PCW8256 and friends.

import os
import array
from PIL import Image

def convert_to_spc(input_filename, preview_filename, output_filename):
	# Load the image.
	im = Image.open(input_filename)

	# Resize it to the size of the PCW8256 screen.
	print("Converting")
	kXDim = 720
	kYDim = 256
	im = im.resize( (kXDim, kYDim) )

	# Convert to 1-bit dithered
	im = im.convert("1")

	# Make a preview image by doubling the height, otherwise it's squashed
	preview_im = im.resize( (kXDim, kYDim * 2) )
	print("Writing " + preview_filename)
	preview_im.save(preview_filename)

	# Create an array of bytes that will be our binary file image.
	data = array.array('B') # B means unsigned byte

	# Stop Press Canvas .SPC format is simply a dump of the PCW's video memory.
	# This code walks the 1-bit image to append the bytes in the correct order.
	kXDimDiv8 = kXDim >> 3
	kYDimDiv8 = kYDim >> 3;
	for y0 in range(kYDimDiv8):
		for x0 in range(kXDimDiv8):
			for y1 in range(8):
				byte = 0
				for bit in range(8):
					y = (y0 << 3) + y1;
					x = (x0 << 3) + (7 - bit);
					if im.getpixel((x,y)) != 0:
						byte = byte | (1 << bit)
				data.append( byte )

	# Now we just dump the binary array to the output file.
	print("Writing " + output_filename)
	f = open(output_filename, 'wb')
	data.tofile(f)
	f.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
	    print("Usage: makespc.py <input_image_filename>")
    else:
        input_filename = sys.argv[1]
        basename, extension = os.path.splitext(full_input_filename)
        preview_filename = basename + ".png"
        output_filename = basename + ".spc"
        convert_to_spc(input_filename, preview_filename, output_filename)
