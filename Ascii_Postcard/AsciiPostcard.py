from PIL import Image
import cv2
from ImgToCanny import applyCannyEdgeDetection
import numpy as np

# Calculate the darkness of a certain range of pixels
def getDarkness(xStart, yStart, charWidth, charHeight, img, numPixelsCell):
    brightnessTotal = 0
    # Check each pixel and add it's value to brightness_total
    for x in range(xStart, xStart + charWidth):
        if(x < img.width):
            for y in range(yStart, yStart + charHeight):
                if(y < img.height):
                    brightness = img.getpixel((x, y))
                    brightnessTotal += brightness
    avgBrightness = brightnessTotal // numPixelsCell

    # Return the avg_brightness of the cell
    return 255 - avgBrightness

# Create and return darkness 
def getAsciiValuesMap(charWidth, charHeight, img, numPixelsCell):
    asciiMap = {}
    rowPanels = (img.height // charHeight)  # Number of characters that fit vertically
    colPanels = (img.width // charWidth)   # Number of characters that fit horizontally
    for y in range(rowPanels):
        for x in range(colPanels):
            # Add each row to the ascii darkness map
            asciiMap[(y,x)] = getDarkness(x * charWidth, y * charHeight, charWidth, charHeight, img, numPixelsCell)
    return asciiMap

# Function to map a brightness value (0-255) to an ASCII character
def brightnessToAscii(brightness):
    ascii_chars = "Ñ@#W$9876543210?!abc;:+=-,_."
    index = int(brightness / 255 * (len(ascii_chars) - 1))
    return ascii_chars[index]

def main():
    imagePath = "C:/Python_Projects/Ascii-Postcard/Ascii_Postcard/sunset.jpg"  # Change to the path of your image
    # Apply Canny edge detection
    edgeImage = applyCannyEdgeDetection(imagePath, 50, 150)

    if edgeImage is not None:
        # Display the edge image
        cv2.imshow('Canny Edge Detection', edgeImage)
        cv2.waitKey(0)  # Wait for a key press to close the displayed window
        cv2.destroyAllWindows()

        # Optionally, save the edge image
        cv2.imwrite("C:/Python_Projects/Ascii-Postcard/Ascii_Postcard/edges.jpg", edgeImage)
    img = Image.open("C:/Python_Projects/Ascii-Postcard/Ascii_Postcard/edges.jpg")
    # Convert OpenCV image to PIL Image
    edge_image_pil = Image.fromarray(np.uint8(edgeImage))  # Ensure it's in uint8 format
    pixelRow, pixelCol = img.size         # Get the size of the input image
    charWidth = 6
    charHeight = 12
    numPixelsCell = charWidth * charHeight
    # Store a tuple(row,col) with the darkness value
    ascii_values_map = getAsciiValuesMap(charWidth, charHeight, img, numPixelsCell)
    prevRow = -1
    asciiString = ""
    for (y, x), brightness in sorted(ascii_values_map.items()):
        if prevRow != y:
            if prevRow != -1:  # Avoid adding a newline on the first line
                asciiString += "\n"
            prevRow = y
        asciiString += brightnessToAscii(brightness)
    print(asciiString)


if __name__ == "__main__":
    main()
    
