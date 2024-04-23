import customtkinter as ctk

def displayAsciiArt(ascii_art):
    # Set the theme to dark mode
    ctk.set_appearance_mode("dark")

    # Create a new customTkinter window
    app = ctk.CTk()
    app.title("ASCII Art Display")

    # Define a custom font for the text area
    custom_font = ctk.CTkFont(family="Courier New", size=4)  # Adjust the font size if necessary

    # Create a text widget to display the ASCII art
    text_area = ctk.CTkTextbox(app, text_color="white", fg_color="#222222", wrap="word", font=custom_font)
    text_area.pack(fill="both", expand=True, padx=10, pady=10)
    text_area.insert("end", ascii_art)  # Insert ASCII art into the text widget
    text_area.configure(state="disabled")  # Make the text area read-only

    # Maximize the window (not full-screen, retains window chrome)
    app.state('zoomed')
