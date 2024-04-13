from PIL import Image
import numpy as np
from ImgToCanny import applyCannyEdgeDetection

ASCII_CHARS = [' ', '.', '`', '\'', ':', '-', '!', '~', '*', '=', '+', '<', '>', 'i', 'l', 't', 'f', 'x', 'n', 'o', 'a', 'e', 'r', 'u', 'v', 'w', 'z', 'X', 'Y', 'U', 'J', 'C', 'L', 'Q', '0', 'Z', 'm', 'q', 'p', 'd', 'b', 'k', 'h', 'A', 'R', 'O', 'P', 'G', 'B', '8', '&', '%', '$', '#', '@', ' ']

def get_darkness(x_start, y_start, char_width, char_height, img, num_pixels_cell):
    brightness_total = 0
    for x in range(x_start, x_start + char_width):
        if x < img.width:
            for y in range(y_start, y_start + char_height):
                if y < img.height:
                    brightness = img.getpixel((x, y))
                    brightness_total += brightness
    avg_brightness = brightness_total // num_pixels_cell
    return 255 - avg_brightness

def get_ascii_values_map(char_width, char_height, img, cimg, num_pixels_cell):
    ascii_map_edges = {}
    ascii_map_color = {}
    row_panels = img.height // char_height
    col_panels = img.width // char_width
    for y in range(row_panels):
        for x in range(col_panels):
            ascii_map_edges[(y, x)] = get_darkness(x * char_width, y * char_height, char_width, char_height, img, num_pixels_cell)
    return ascii_map_edges, ascii_map_color

def brightness_to_ascii(brightness):
    index = int(brightness / 255 * (len(ASCII_CHARS) - 1))
    return ASCII_CHARS[index]

def main():
    image_path = "C:/Python_Projects/Ascii-Postcard/Ascii_Postcard/sunset.jpg"
    (color_img, edge_image) = applyCannyEdgeDetection(image_path, 50, 150)
    if edge_image is not None:
        edgeImage = Image.fromarray(np.uint8(edge_image))  # Convert numpy array to PIL Image
        edgeImage.save("C:/Python_Projects/Ascii-Postcard/Ascii_Postcard/save.jpg")
        cImage = Image.open(image_path)
        char_width, char_height = 6, 12
        num_pixels_cell = char_width * char_height
        ascii_values_map, ascii_values_map_color = get_ascii_values_map(char_width, char_height, edgeImage, cImage, num_pixels_cell)
        ascii_string = create_ascii_art(ascii_values_map)
        #ascii_string = create_ascii_art(ascii_values_map_color)
        print(ascii_string)

def create_ascii_art(ascii_values_map):
    prev_row = -1
    ascii_string = ""
    for (y, x), brightness in sorted(ascii_values_map.items()):
        if prev_row != y:
            if prev_row != -1:
                ascii_string += "\n"
            prev_row = y
        ascii_string += brightness_to_ascii(brightness)
    return ascii_string

if __name__ == "__main__":
    main()
