# Ascii Postcard
 Generate an Ascii Postcard

+ Using Pillow we can generate a greyscale image from an input image
+ We segment the image into panels
+ Calculate the darkness of a panel by counting each pixel
+ Store the darkness in a map((x,y) darkness) to use later
+ Create ascii darkness scale
+ Use darkness vals to generate ascii string
+ Generate ascii art image

- Investigating OpenCV to smooth edges for better result
- Add custom text option
- Add location placement for text