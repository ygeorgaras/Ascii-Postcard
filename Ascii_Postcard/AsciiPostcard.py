from PIL import Image

# Generates and returns greyscale image
def genGreyscaleImage():
    tempImg = Image.open("C:/Python_Projects/Ascii-Postcard/Ascii_Postcard/sunset.jpg").convert('L')
    return tempImg

# Calculate the darkness of a certain range of pixels
def getDarkness(xStart, yStart):
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
def getAsciiValuesMap():
    asciiMap = {}
    rowPanels = (img.height // charHeight)  # Number of characters that fit vertically
    colPanels = (img.width // charWidth)   # Number of characters that fit horizontally
    for y in range(rowPanels):
        for x in range(colPanels):
            # Add each row to the ascii darkness map
            asciiMap[(y,x)] = getDarkness(x * charWidth, y * charHeight)
    return asciiMap

# Function to map a brightness value (0-255) to an ASCII character
def brightnessToAscii(brightness):
    index = int(brightness / 255 * (len(ascii_chars) - 1))
    return ascii_chars[index]

img = genGreyscaleImage()
#img.save("greyscale.png")
pixelRow, pixelCol = img.size         # Get the size of the input image
charWidth = 6
charHeight = 12
numPixelsCell = charWidth * charHeight
ascii_values_map = getAsciiValuesMap()# Store a tuple(row,col) with the darkness value
ascii_chars = [' ', '.', '`', '\'', ':', '-', '!', '~', '*', '=', '+', '<', '>', 'i', 'l', 't', 'f', 'x', 'n', 'o', 'a', 'e', 'r', 'u', 'v', 'w', 'z', 'X', 'Y', 'U', 'J', 'C', 'L', 'Q', '0', 'Z', 'm', 'q', 'p', 'd', 'b', 'k', 'h', 'A', 'R', 'O', 'P', 'G', 'B', '8', '&', '%', '$', '#', '@']
asciiString = ""
prevRow = -1

for (y, x), brightness in sorted(ascii_values_map.items()):
    if prevRow != y:
        if prevRow != -1:  # Avoid adding a newline on the first line
            asciiString += "\n"
        prevRow = y
    asciiString += brightnessToAscii(brightness)