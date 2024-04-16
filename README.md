# Ascii Postcard
 Generate an Ascii Postcard

+ Using Pillow we can generate a greyscale image from an input image
+ We segment the image into panels
+ Calculate the darkness of a panel by counting each pixel
+ Store the darkness in a map((x,y) darkness) to use later
+ Create ascii darkness scale
+ Use darkness vals to generate ascii string
+ Generate ascii art image
+ Investigating OpenCV to smooth edges for better result
+ Creating Canny image to find edges of input image
+ Use the regular image along with the canny image to generate a better ascii art template

- Increasing resolution of image to have a higher quality art in the end
- Add custom text option
- Add location placement for text