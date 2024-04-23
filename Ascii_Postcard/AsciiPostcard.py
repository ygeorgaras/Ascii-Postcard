from PIL import Image
from ImgToCanny import applyCannyEdgeDetection
from DisplayAsciiArt import displayAsciiArt
from AsciiText import createAsciiText
import pyperclip

ASCII_CHARS = "Ñ@#W$9876543210?!abc;:+=-,._ "
CHAR_HEIGHT = 0
CHAR_WIDTH = 0
NUM_PIXELS_PER_CELL = CHAR_HEIGHT * CHAR_WIDTH
ROW_PANELS = 0
COL_PANELS = 0
UPPER_SCORE, UPPER_SCORE_INDEX = '‾', 256
VERTICAL_BAR, VERTICAL_BAR_INDEX = '|', 257
UNDER_SCORE, UNDER_SCORE_INDEX = '_', 258
TEXT_AREA = 260
TEXT_LOCATION_OPTIONS = {
    "Centered" : (0.5,0.5),
    "Top" : (0.5,0.25), 
    "Bottom" : (0.5,0.75),
    "Left" : (0.25, 0.5),
    "Right" : (0.75, 0.5),
    "Top-Left" : (0.25,0.25),
    "Bot-Left" : (0.25,0.75),
    "Top-Right" : (0.75,0.25),
    "Bot-Right" : (0.75,0.75)
    }

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
    if image.mode == 'L':
        return 0
    # Iterate over each pixel in the specified range
    for x in range(xStart, min(xStart + CHAR_WIDTH, image.width)):
        for y in range(yStart, min(yStart + CHAR_HEIGHT, image.height)):
            pixel = image.getpixel((x, y))
            red += pixel[0]
            green += pixel[1]
            blue += pixel[2]

    # Calculate the average color
    avgRed = red // NUM_PIXELS_PER_CELL
    avgGreen = green // NUM_PIXELS_PER_CELL
    avgBlue = blue // NUM_PIXELS_PER_CELL

    return (avgRed + avgGreen + avgBlue) / 3

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

def createAsciiArt(colorsMap, cannyMap, textMap = {}, textBoarder = {}):
    prevRow = -1
    asciiArt = []
    for (y, x), brightness in sorted(colorsMap.items()):
        if prevRow != y:
            if prevRow != -1:
                asciiArt.append("\n")
            prevRow = y

        if colorsMap[(y,x)] == UPPER_SCORE_INDEX:
            asciiArt.append(UPPER_SCORE)
        elif colorsMap[(y,x)] == VERTICAL_BAR_INDEX:
            asciiArt.append(VERTICAL_BAR)
        elif colorsMap[(y,x)] == UNDER_SCORE_INDEX:
            asciiArt.append(UNDER_SCORE)
        elif colorsMap[(y,x)] == TEXT_AREA:
            textX = x - textBoarder[0] - 1
            textY = y - textBoarder[1] - 1
            if 0 <= textX < textBoarder[2] and 0 <= textY < textBoarder[3]:
                asciiArt.append(textMap[(textY, textX)])
                # Check for edge
        elif cannyMap[(y, x)] < 255:  # Check cannyAssuming edge pixels are marked with 255
            # If there's an edge, use a darker ASCII character
            asciiArt.append(ASCII_CHARS[-1])
        else:
            # Otherwise, use the ASCII character corresponding to the brightness
            asciiArt.append(avgColorToAscii(brightness))

    return ''.join(asciiArt)

# TODO: Reduce aspect ratio if image is very large
def adjustAspectRatio(height, width):
    global CHAR_HEIGHT, CHAR_WIDTH, NUM_PIXELS_PER_CELL, ROW_PANELS, COL_PANELS
    # Check if the image is vertically or horizontally oriented
    if height == width:
        CHAR_HEIGHT = 12
        CHAR_WIDTH = 6
    if height > width:
        CHAR_HEIGHT = 4
        CHAR_WIDTH = 2
    elif height < width:
        CHAR_HEIGHT = 5
        CHAR_WIDTH = 3

    # Calculate the number of rows and columns of characters based on the adjusted character dimensions
    ROW_PANELS = height // CHAR_HEIGHT
    COL_PANELS = width // CHAR_WIDTH
    # Calculate the number of pixels per cell
    NUM_PIXELS_PER_CELL = CHAR_HEIGHT * CHAR_WIDTH

def selectLocation(x, y, textRows, textCols):

    minLeftY = y - (textRows // 2) 
    maxRightY = y + (textRows // 2)

    minLeftX = x - (textCols // 2) 
    maxRightX = x + (textCols // 2)

    if maxRightX > COL_PANELS:
        inBoundsOffset = maxRightX - COL_PANELS + 1
        maxRightX -= inBoundsOffset
        minLeftX -= inBoundsOffset

    return (minLeftX, minLeftY, maxRightX, maxRightY)

def analyzeAsciiArt(asciiArt):
    rows = asciiArt.strip().split('\n')  # Strip to remove any leading/trailing whitespace and split by newline
    numRows = len(rows)
    numCols = len(rows[0]) if numRows > 0 else 0  # Assume all rows have the same number of columns

    # Create an empty dictionary for the artMap
    artMap = {}

    # Dimensions expanded by 3 for the border
    expandedNumRows = numRows + 3
    expandedNumCols = numCols + 3

    # Fill the artMap with border and art
    for y in range(expandedNumRows):
        for x in range(expandedNumCols):
            if y == 0 or y == expandedNumRows - 1:
                artMap[(y, x)] = '-'  # Top and bottom border
            elif x == 0 or x == expandedNumCols - 1:
                artMap[(y, x)] = '|'  # Left and right border
            else:
                if y-1 < numRows and x-1 < len(rows[y-1]):
                    artMap[(y, x)] = rows[y-1][x-1]
                else:
                    artMap[(y, x)] = ' '  # Fill in any gaps

    return artMap, expandedNumRows, expandedNumCols

def getTextLocation(textLocation):
    y = 0
    x = 0
    if textLocation in TEXT_LOCATION_OPTIONS:
        y,x = TEXT_LOCATION_OPTIONS[textLocation]
        return int(COL_PANELS * y), int(ROW_PANELS * x)
    
    return y,x

def insertTextArea(map, text, textLocation):
    asciiText = createAsciiText(text)
    textMap, textRows, textCols = analyzeAsciiArt(asciiText)
    middleTextY, middleTextX= getTextLocation(textLocation)
    topLeftX, topLeftY, botRightX, botRightY =  selectLocation(middleTextY, middleTextX, textRows, textCols)
    
    for y in range(topLeftY, botRightY + 1):
        for x in range(topLeftX, botRightX + 1):
            if(x == topLeftX or x == botRightX):
                map[(y,x)] = VERTICAL_BAR_INDEX
            elif(y == topLeftY):
                map[(y,x)] = UPPER_SCORE_INDEX
            elif(y == botRightY):
                map[(y,x)] = UNDER_SCORE_INDEX
            else:
                map[(y,x)] = TEXT_AREA
    return map, textMap, [topLeftX, topLeftY, botRightX, botRightY]

def generateAsciiArt(imagePath, text, textLocation):
    edgeImage = applyCannyEdgeDetection(imagePath, 50, 150)
    if edgeImage is not None:
        edgeImage = Image.fromarray(edgeImage)  # Convert numpy array to PIL Image
        cImage = Image.open(imagePath)
        adjustAspectRatio(edgeImage.height, edgeImage.width) # Adjusts the aspect ratio depending on height & width
        asciiColorValuesMap, asciiValuesMap = getAsciiValuesMap(cImage, edgeImage) # Get the values for these dictionaries
        if text != "":
            asciiColorTextValuesMap, textMap, textBoarder = insertTextArea(asciiColorValuesMap, text, textLocation)
            asciiString = createAsciiArt(asciiColorTextValuesMap, asciiValuesMap, textMap, textBoarder)
        else:
            asciiString = createAsciiArt(asciiColorValuesMap, asciiValuesMap, {}, {})
        pyperclip.copy(asciiString) # Copy to clipboard
        displayAsciiArt(asciiString)