import tkinter as tk
from tkinter import scrolledtext
from tkinter.font import Font

def displayAsciiArt(asciiArt):
    # Create a new tkinter window
    root = tk.Tk()
    root.title("ASCII Art Display")

    # Maximize the window
    root.state('zoomed')  # This maximizes the window but keeps the window frame intact

    # Define a custom font: name, size, and style
    custom_font = Font(family="Courier New", size=2)
    
    # Create a scrolled text widget
    text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=custom_font)
    text_area.pack(fill=tk.BOTH, expand=True)

    # Insert the ASCII art into the text widget
    text_area.insert(tk.INSERT, asciiArt)
    text_area.config(state=tk.DISABLED)

    # Start the tkinter event loop
    root.mainloop()