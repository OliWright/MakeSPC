# MakeSPC
Python script to convert images to the .SPC format, which is popular on the Amstrad PCW8256 and friends.

You just need to provide a source image in any popular format. Be sure to crop your image to a 4:3 aspect ratio before running this tool though, because it assumes the image is already 4:3 and won't do any cropping.  But it will resize the image appropriately for you.

## Prerequisites
[Python](https://www.python.org/)

[Pillow](https://pillow.readthedocs.io/en/stable/)

## Usage
`python makespc.py <input image filename>`

The script will write out a preview image in the same format as the input, and it will write a .spc file that can be copied to a disk image for viewing on an Amstrad PCW8256 or similar.
