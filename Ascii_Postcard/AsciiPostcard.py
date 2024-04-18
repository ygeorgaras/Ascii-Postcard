from PIL import Image
from ImgToCanny import applyCannyEdgeDetection
from DisplayAsciiArt import displayAsciiArt
from AsciiText import createAsciiText
import pyperclip
import time


ASCII_CHARS = "Ñ@#W$9876543210?!abc;:+=-,._ "
CHAR_HEIGHT = 4
CHAR_WIDTH = 2
NUM_PIXELS_PER_CELL = CHAR_HEIGHT * CHAR_WIDTH
IMAGE_PATH = "C:/Python_Projects/Ascii-Postcard/Ascii_Postcard/sunset.jpg"
ROW_PANELS = 0
COL_PANELS = 0
UPPER_SCORE, UPPER_SCORE_INDEX = '‾', 256
VERTICAL_BAR, VERTICAL_BAR_INDEX = '|', 257
UNDER_SCORE, UNDER_SCORE_INDEX = '_', 258
TEXT_AREA = 260

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

def createAsciiArt(colors, canny, text, textBoarder):
    prev_row = -1
    ascii_art = []
    for (y, x), brightness in sorted(colors.items()):
        if prev_row != y:
            if prev_row != -1:
                ascii_art.append("\n")
            prev_row = y
        # Check for edge
        if canny[(y, x)] < 255:  # Assuming edge pixels are marked with 255
            # If there's an edge, use a darker ASCII character
            ascii_art.append(ASCII_CHARS[-1])
        else:
            if colors[(y,x)] == UPPER_SCORE_INDEX:
                ascii_art.append(UPPER_SCORE)
            elif colors[(y,x)] == VERTICAL_BAR_INDEX:
                ascii_art.append(VERTICAL_BAR)
            elif colors[(y,x)] == UNDER_SCORE_INDEX:
                ascii_art.append(UNDER_SCORE)
            elif colors[(y,x)] == TEXT_AREA:
                text_x = x - textBoarder[0] - 1
                text_y = y - textBoarder[1] - 1
                if 0 <= text_x < textBoarder[2] and 0 <= text_y < textBoarder[3]:
                    ascii_art.append(text[(text_y, text_x)])
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

def selectLocation(x, y, textRows, textCols):

    minLeftX = x - (textCols // 2) 
    minLeftY = y - (textRows // 2) 
    maxRightX = x + (textCols // 2)
    maxRightY = y + (textRows // 2)
    return (minLeftX, minLeftY, maxRightX, maxRightY)

def analyzeAsciiArt(ascii_art):
    rows = ascii_art.strip().split('\n')  # Strip to remove any leading/trailing whitespace and split by newline
    num_rows = len(rows)
    num_cols = len(rows[0]) if num_rows > 0 else 0  # Assume all rows have the same number of columns

    # Create an empty dictionary for the art_map
    art_map = {}

    # Dimensions expanded by 3 for the border
    expanded_num_rows = num_rows + 3
    expanded_num_cols = num_cols + 3

    # Fill the art_map with border and art
    for y in range(expanded_num_rows):
        for x in range(expanded_num_cols):
            if y == 0 or y == expanded_num_rows - 1:
                art_map[(y, x)] = '-'  # Top and bottom border
            elif x == 0 or x == expanded_num_cols - 1:
                art_map[(y, x)] = '|'  # Left and right border
            else:
                if y-1 < num_rows and x-1 < len(rows[y-1]):
                    art_map[(y, x)] = rows[y-1][x-1]
                else:
                    art_map[(y, x)] = ' '  # Fill in any gaps

    return art_map, expanded_num_rows, expanded_num_cols

def insertTextArea(map):
    ascii_text = createAsciiText("Testing")
    
    textMap, textRows, textCols = analyzeAsciiArt(ascii_text)

    #TODO: Modify to select locations
    middleX = COL_PANELS // 2
    middleY = ROW_PANELS // 2

    topLeftX, topLeftY, botRightX, botRightY =  selectLocation(middleX, middleY, textRows, textCols)
    
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

def main(sTime):
    edgeImage = applyCannyEdgeDetection(IMAGE_PATH, 50, 150)
    if edgeImage is not None:
        edgeImage = Image.fromarray(edgeImage)  # Convert numpy array to PIL Image
        cImage = Image.open(IMAGE_PATH)
        adjustAspectRatio(edgeImage.height, edgeImage.width) # Adjusts the aspect ratio depending on height & width
        asciiColorValuesMap, asciiValuesMap = getAsciiValuesMap(cImage, edgeImage) # Get the values for these dictionaries
        asciiColorTextValuesMap, textMap, textBoarder = insertTextArea(asciiColorValuesMap)
        asciiString = createAsciiArt(asciiColorTextValuesMap, asciiValuesMap, textMap, textBoarder)
        pyperclip.copy(asciiString) # Copy to clipboard
        displayAsciiArt(asciiString)
        
if __name__ == "__main__":
    start_time = time.time()
    main(start_time)
    print(time.time() - start_time)

