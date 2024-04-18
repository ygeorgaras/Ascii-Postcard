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
+ Added adjustAspectRatio to imrpove resolution
+ Add window to show ASCII during runtime
+ Add custom text option
+ Using pyfiglet to generate text

- Create UI
    - Select image
    - Add text
    - Select text location
    - Select font
- Add location placement for text
- If image is very large use Pillow to reduce the size of the image and text
