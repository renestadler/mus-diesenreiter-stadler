import requests
from pyzbar import pyzbar
import imutils
from tkinter import *
import cv2
from PIL import Image, ImageTk
from urllib.request import urlopen

# Define a video capture object
vid = cv2.VideoCapture(0)

# Declare the width and height in variables
width, height = 800, 600

# Set the width and height
vid.set(cv2.CAP_PROP_FRAME_WIDTH, width)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

# Create a GUI app
app = Tk()
app.geometry("620x600")
app.configure(background='white')
ico = Image.open('logos/logo_small_solo_cropped.png')
photo = ImageTk.PhotoImage(ico)
app.wm_iconphoto(False, photo)

# Bind the app with Escape keyboard to
# quit app whenever pressed
app.bind('<Escape>', lambda e: app.quit())

# Add a frame to set the size of the window
frame = Frame(app, relief='sunken')
frame.grid(sticky="we")
# Make the frame sticky for every case
frame.grid_rowconfigure(0, weight=1)
frame.grid_columnconfigure(0, weight=1)
# Make the window sticky for every case
app.grid_rowconfigure(0, weight=1)
app.grid_columnconfigure(0, weight=1)

# Load the image
image_path = "logos/logo_big.png"
image = Image.open(image_path)
photo = ImageTk.PhotoImage(image)

# Create a label and display it on app
img_lbl = Label(app, image=photo, bd=0)
img_lbl.image = photo
img_lbl.configure(highlightthickness=0)
img_lbl.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
img_lbl.grid_rowconfigure(1, weight=1)
img_lbl.grid_columnconfigure(1, weight=1)


def get_recycling_info(barcode):
    # request
    try:
        response = requests.get(f'http://localhost:8080/product?barcode={barcode.data.decode("utf-8")}')

        response = response.json()
        recycling_info = ''
    except:
        print("Could not establish connection to backend")
        recycling_info = "Server down"

    u = urlopen(response['image'])
    raw_data = u.read()
    u.close()

    photo = ImageTk.PhotoImage(data=raw_data)  # <-----

    # show recycling info
    img_lbl.configure(image=photo)
    img_lbl.configure(text=recycling_info)
    img_lbl.image = photo

    btn_scan.grid(row=1, column=0, padx=10, pady=10)


def scan_barcode():
    btn_scan.grid_forget()
    keep_looping = True
    # Capture frame from the camera
    ret, video_frame = vid.read()

    if ret:
        video_frame = imutils.resize(video_frame, width=600)
        # Convert the frame to grayscale
        gray = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)

        # Detect barcodes in the frame
        barcodes = pyzbar.decode(gray)

        # check if barcodes were found
        if barcodes:
            if len(barcodes) > 1:
                print("Found more than one barcode in the frame, try again")
            else:
                for barcode in barcodes:
                    barcode_data = barcode.data.decode("utf-8")
                    barcode_type = barcode.type
                    print("Barcode Type:", barcode_type)
                    print("Barcode Data:", barcode_data)
                    keep_looping = False

        # Draw a Region of Interest (ROI) rectangle on the frame
        roi_start_x = 100
        roi_start_y = 40
        roi_end_x = 500
        roi_end_y = 150
        cv2.rectangle(gray, (roi_start_x, roi_start_y), (roi_end_x, roi_end_y), (0, 255, 0), 2)

        # Convert the frame to PIL format
        img = Image.fromarray(gray)

        # Convert PIL image to Tkinter-compatible photoimage
        photo_image = ImageTk.PhotoImage(image=img)

        # Update the label with the new photoimage
        img_lbl.configure(image=photo_image)
        img_lbl.image = photo_image

        # Schedule the next frame processing and barcode scanning
        if keep_looping:
            img_lbl.after(10, scan_barcode)
        else:
            get_recycling_info(barcode)


# Create a button to open the camera in GUI app
btn_scan = Button(app, text="Scan barcode", height=3, width=20, command=scan_barcode)
btn_scan.grid(row=1, column=0, padx=10, pady=10)
btn_scan.grid_rowconfigure(1, weight=1)
btn_scan.grid_columnconfigure(1, weight=1)

# Create an infinite loop for displaying app on screen
app.mainloop()
