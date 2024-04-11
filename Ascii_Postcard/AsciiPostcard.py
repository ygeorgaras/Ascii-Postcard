from PIL import Image

# Generates and returns greyscale image
def genGreyscaleImage():
    tempImg = Image.open("thailand.png").convert('L')
    return tempImg

# Calculate the darkness of a certain range of pixels
def getDarkness(x_start, y_start):
    brightness_total = 0
    # Check each pixel and add it's value to brightness_total
    for x in range(x_start, x_start + char_width):
        for y in range(y_start, y_start + char_height):
            brightness = img.getpixel((x, y))
            brightness_total += brightness
    avg_brightness = brightness_total // num_pixels_cell

    # Return the avg_brightness of the cell
    return 255 - avg_brightness

img = genGreyscaleImage()
img.save("greyscale.png")
pixel_row, pixel_col = img.size         # Get the size of the input image
char_width = 12
char_height = 12
num_pixels_cell = char_width * char_height
rowPanels = (pixel_row // char_height)  # Number of characters that fit vertically
colPanels = (pixel_col // char_width)   # Number of characters that fit horizontally
ascii_values_map = {}                   # Store a tuple(row,col) with the darkness value

for i in range(rowPanels):
    next_row_size = i * char_width
    for j in range(colPanels):
        next_col_size = j * char_height
        # Add each row to the ascii darkness map
        ascii_values_map[(i,j)] = getDarkness(next_row_size, next_col_size)
