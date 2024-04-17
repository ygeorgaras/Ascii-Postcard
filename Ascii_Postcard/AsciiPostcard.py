from PIL import Image
from ImgToCanny import applyCannyEdgeDetection
import pyperclip
import time


ASCII_CHARS = "Ñ@#W$9876543210?!abc;:+=-,._ "
CHAR_HEIGHT = 4
CHAR_WIDTH = 2
NUM_PIXELS_PER_CELL = CHAR_HEIGHT * CHAR_WIDTH
IMAGE_PATH = "C:/Python_Projects/Ascii-Postcard/Ascii_Postcard/galata.jpg"
ROW_PANELS = 0
COL_PANELS = 0

def getDarkness(xStart, yStart, img):
    brightnessTotal = 0

    # Iterate over each pixel in the specified range
    for x in range(xStart, xStart + CHAR_WIDTH):
        if x < img.width:
            for y in range(yStart, yStart + CHAR_HEIGHT):
                if y < img.height:
                    brightness = img.getpixel((x, y))
                    brightnessTotal += brightness
    # Calculate the average brightness in the cell
    avgBrightness = brightnessTotal // NUM_PIXELS_PER_CELL
    return 255 - avgBrightness

def getAvgColor(xStart, yStart, image):
    # Initialize the sum of the colors
    red, green, blue = 0, 0, 0

    # Iterate over each pixel in the specified range
    for x in range(xStart, min(xStart + CHAR_WIDTH, image.width)):
        for y in range(yStart, min(yStart + CHAR_HEIGHT, image.height)):
            pixel = image.getpixel((x, y))
            red += pixel[0]
            green += pixel[1]
            blue += pixel[2]

    # Calculate the average color
    avg_r = red // NUM_PIXELS_PER_CELL
    avg_g = green // NUM_PIXELS_PER_CELL
    avg_b = blue // NUM_PIXELS_PER_CELL

    return (avg_r + avg_g + avg_b) / 3

#def getAsciiValuesMap(img):
#    asciiMapEdges = {}
#    for y in range(ROW_PANELS):
#        for x in range(COL_PANELS):
#            asciiMapEdges[(y, x)] = getDarkness(x * CHAR_WIDTH, y * CHAR_HEIGHT, img)
#    return asciiMapEdges

def getAsciiValuesMap(colorImage, edgeImage):
    asciiMapColor = {}
    asciiMapEdges = {}
    # Iterate over each cell in the grid defined by ROW_PANELS and COL_PANELS
    for y in range(ROW_PANELS):
        for x in range(COL_PANELS):
            # Calculate the top-left corner of the current cell in the color image
            # and get the average color and darkness to determine the ASCII character
            asciiMapColor[(y, x)] = getAvgColor(x * CHAR_WIDTH, y * CHAR_HEIGHT, colorImage)
            asciiMapEdges[(y, x)] = getDarkness(x * CHAR_WIDTH, y * CHAR_HEIGHT, edgeImage)
    return asciiMapColor, asciiMapEdges

def avgColorToAscii(brightness):
    index = int(brightness / 255 * (len(ASCII_CHARS) - 1))
    # Return the ASCII character at the index
    return ASCII_CHARS[index]

def createAsciiArt(colors, canny):
    prev_row = -1
    ascii_art = []
    for (y, x), brightness in sorted(colors.items()):
        if prev_row != y:
            if prev_row != -1:
                ascii_art.append("\n")
            prev_row = y
        # Check for edge
        if canny.get((y, x), 0) < 255:  # Assuming edge pixels are marked with 255
            # If there's an edge, use a darker ASCII character
            ascii_art.append(ASCII_CHARS[-1])
        else:
            # Otherwise, use the ASCII character corresponding to the brightness
            ascii_art.append(avgColorToAscii(brightness))
    return ''.join(ascii_art)

# TODO: Reduce aspect ratio if image is very large
def adjustAspectRatio(height, width):
    global CHAR_HEIGHT, CHAR_WIDTH, NUM_PIXELS_PER_CELL, ROW_PANELS, COL_PANELS
    # Check if the image is vertically or horizontally oriented
    if height > width:
        CHAR_HEIGHT = 4
        CHAR_WIDTH = 2
    elif height < width:
        CHAR_HEIGHT = 4
        CHAR_WIDTH = 3

    # Calculate the number of rows and columns of characters based on the adjusted character dimensions
    ROW_PANELS = height // CHAR_HEIGHT
    COL_PANELS = width // CHAR_WIDTH
    # Calculate the number of pixels per cell
    NUM_PIXELS_PER_CELL = CHAR_HEIGHT * CHAR_WIDTH

def main():
    edgeImage = applyCannyEdgeDetection(IMAGE_PATH, 50, 150)
    if edgeImage is not None:
        edgeImage = Image.fromarray(edgeImage)  # Convert numpy array to PIL Image
        cImage = Image.open(IMAGE_PATH)
        adjustAspectRatio(edgeImage.height, edgeImage.width) # Adjusts the aspect ratio depending on height & width
        asciiColorValuesMap, asciiValuesMap = getAsciiValuesMap(cImage, edgeImage) # Get the values for these dictionaries
        asciiString = createAsciiArt(asciiColorValuesMap, asciiValuesMap)
        pyperclip.copy(asciiString) # Copy to clipboard
        
if __name__ == "__main__":
    start_time = time.time()
    main()
    print(time.time() - start_time)

