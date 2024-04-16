from PIL import Image
from ImgToCanny import applyCannyEdgeDetection
import pyperclip


ASCII_CHARS = "Ñ@#W$9876543210?!abc;:+=-,._ "

def getDarkness(xStart, yStart, charWidth, charHeight, img, numPixelsCell):
    brightnessTotal = 0
    for x in range(xStart, xStart + charWidth):
        if x < img.width:
            for y in range(yStart, yStart + charHeight):
                if y < img.height:
                    brightness = img.getpixel((x, y))
                    brightnessTotal += brightness
    avgBrightness = brightnessTotal // numPixelsCell
    return 255 - avgBrightness

def getAvgColor(xStart, yStart, width, height, image):

    # Initialize the sum of the colors
    red, green, blue = 0, 0, 0

    # Iterate over each pixel in the specified range
    for x in range(xStart, min(xStart + width, image.width)):
        for y in range(yStart, min(yStart + height, image.height)):
            pixel = image.getpixel((x, y))
            red += pixel[0]
            green += pixel[1]
            blue += pixel[2]

    # Calculate the number of pixels in the range
    numPixels = (min(xStart + width, image.width) - xStart) * (min(yStart + height, image.height) - yStart)

    # Calculate the average color
    avg_r = red // numPixels
    avg_g = green // numPixels
    avg_b = blue // numPixels

    return (avg_r + avg_g + avg_b) / 3

def getAsciiValuesMap(charWidth, charHeight, img, numPixelsCell):
    asciiMapEdges = {}
    rowPanels = img.height // charHeight
    colPanels = img.width // charWidth
    for y in range(rowPanels):
        for x in range(colPanels):
            asciiMapEdges[(y, x)] = getDarkness(x * charWidth, y * charHeight, charWidth, charHeight, img, numPixelsCell)
    return asciiMapEdges

def getColorAsciiValuesMap(charWidth, charHeight, img, numPixelsCell):
    asciiMapColor = {}
    rowPanels = img.height // charHeight
    colPanels = img.width // charWidth
    for y in range(rowPanels):
        for x in range(colPanels):
            asciiMapColor[(y, x)] = getAvgColor(x * charWidth, y * charHeight, charWidth, charHeight, img)
    return asciiMapColor

def brightnessToAscii(brightness):
    index = int(brightness / 255 * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[index]

def main():
    imagePath = "C:/Python_Projects/Ascii-Postcard/Ascii_Postcard/thailand.png"
    edgeImage = applyCannyEdgeDetection(imagePath, 50, 150)
    if edgeImage is not None:
        edgeImage = Image.fromarray(edgeImage)  # Convert numpy array to PIL Image
        edgeImage.save("C:/Python_Projects/Ascii-Postcard/Ascii_Postcard/save.jpg")
        cImage = Image.open(imagePath)
        charWidth, charHeight = 6, 12
        numPixelsCell = charWidth * charHeight
        asciiValuesMap = getAsciiValuesMap(charWidth, charHeight, edgeImage, numPixelsCell)
        number_of_keys = len(asciiValuesMap)
        print(number_of_keys)
        asciiColorValuesMap = getColorAsciiValuesMap(charWidth, charHeight, cImage, numPixelsCell)   
        number_of_keys = len(asciiColorValuesMap)
        print(number_of_keys)     
        asciiString = createAsciiArt(asciiColorValuesMap, asciiValuesMap)
        pyperclip.copy(asciiString)


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
            ascii_art.append(brightnessToAscii(brightness))
    return ''.join(ascii_art)

if __name__ == "__main__":
    main()
