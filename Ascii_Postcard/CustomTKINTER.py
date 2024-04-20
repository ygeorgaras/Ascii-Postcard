import customtkinter as ctk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import StringVar
from AsciiPostcard import generateAsciiArt

TEXT_LOCATION_OPTIONS = ["Centered", "Top", "Left"]

# Function to open file dialog and update file name text box
def openFileDialog():
    # Open a file dialog and store the selected file path, allowing .jpg and .png files
    filePath = filedialog.askopenfilename(title="Select a File",
                                           filetypes=[("Image files", "*.jpg;*.jpeg;*.png"),
                                                      ("JPEG files", "*.jpg;*.jpeg"),
                                                      ("PNG files", "*.png")])
    if filePath:  # Check if a file was selected
        # Check if the file selected is a jpg or png file
        if filePath.lower().endswith(('.jpg', '.jpeg', '.png')):
            fileNameTextbox.configure(state="normal")  # Temporarily enable the textbox to edit
            generateButton.configure(state="normal")
            # Clear the current entry content and insert the new file name
            fileNameTextbox.delete(0, ctk.END)
            fileNameTextbox.insert(0, filePath)
            fileNameTextbox.configure(state="disabled")  # Temporarily enable the textbox to edit
        else:
            # If the selected file is not a jpg or png, show a message box
            messagebox.showwarning("Invalid File Type", "Please select only JPG or PNG files.")
            
# Function to generate the ASCII image (placeholder)
def generateAsciiImage():
    generateAsciiArt(fileNameTextbox.get(), customTextEntry.get(), textLocationDropdown.get())

# Callback function to enable/disable dropdown based on text entry content
def onTextEntryChange(*args):
    text = textEntryVar.get()
    if text:  # If there is text, enable the dropdown
        if len(text) == 20:
            textEntryVar.set(text[:-1])
        if textLocationDropdown._state == "disabled":
            textLocationDropdown.configure(state="normal")
            textLocationDropdown.set(TEXT_LOCATION_OPTIONS[0])
    else:  # If there is no text, disable the dropdown
        textLocationDropdown.set("")
        textLocationDropdown.configure(state="disabled")

# Set appearance mode and color theme
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

app = ctk.CTk()  # Create main window
app.title('ASCII Art Generator')
app.geometry('400x300')  # Define size of the window

# StringVar linked to the customTextEntry to track its content
textEntryVar = StringVar()
textEntryVar.trace("w", onTextEntryChange)  # Trace writes to the variable

# Button to select file
selectFileButton = ctk.CTkButton(app, text="Select File", command=openFileDialog, width=350)
selectFileButton.pack(pady=10)

# Textbox to display the file name
fileNameTextbox = ctk.CTkEntry(app, state="disabled", width=350)
fileNameTextbox.pack(pady=10)


# Description label for custom text entry
customTextLabel = ctk.CTkLabel(app, text="Enter custom text (20 chars max):")
customTextLabel.pack(pady=(0, 0))

# Custom text entry
customTextEntry = ctk.CTkEntry(app, textvariable=textEntryVar,  placeholder_text="Custom text", width=350)
customTextEntry.pack(pady=10)

# Description label for text location dropdown
textLocationLabel = ctk.CTkLabel(app, text="Choose text location in image:")
textLocationLabel.pack(pady=(0, 0))

# Drop-down menu for text location
textLocationDropdown = ctk.CTkComboBox(app, values=TEXT_LOCATION_OPTIONS, state="disabled", width=350)
textLocationDropdown.pack(pady=10)

# Button to generate ASCII image
generateButton = ctk.CTkButton(app, text="Generate ASCII Image", command=generateAsciiImage, state="disabled")
generateButton.pack(pady=10)

app.mainloop()  # Start main event loop
