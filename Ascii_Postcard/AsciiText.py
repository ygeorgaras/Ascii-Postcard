import pyfiglet
def createAsciiText(input):
    #available_fonts = pyfiglet.FigletFont.getFonts()
    #print(available_fonts)

    # Select a font that tends to produce larger text
    font_name = 'Default'  # This is just an example; try different fonts to see which one you like
    
    # Create a Figlet object with the selected font
    f = pyfiglet.Figlet(font=font_name, width=200)
    ascii_art = f.renderText(input)
    return ascii_art
