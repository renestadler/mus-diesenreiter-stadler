from tkinter import ttk
import textwrap
import requests
from pyzbar import pyzbar
import imutils
from tkinter import *
import cv2
from PIL import Image, ImageTk
from urllib.request import urlopen

# PROPERTIES
vid_width, vid_height = 400, 600
info_label_width = 60
t1 = textwrap.fill("Just click the \"Scan\" button and aim the barcode of any product at the camera.", width=65)
t2 = textwrap.fill("Waste Wizard will swiftly identify the item and provide you  with essential information on how to "
                   "dispose of it responsibly.", width=65)
welcome_text = "\n\nMake a difference and reduce waste and become an eco-warrior!\n\n\n" + t1 + "\n" + t2 + "\n"

scanning_text = "\n\nMake sure to match the barcode to the box"
scanning_error_text = "\n\nWe found more than one barcode, make sure to scan only one at a time"

# Define a video capture object
vid = cv2.VideoCapture(0)
vid.set(cv2.CAP_PROP_FRAME_WIDTH, vid_width)
vid.set(cv2.CAP_PROP_FRAME_HEIGHT, vid_height)

# Create a GUI app
app = Tk()

# Configure the default style for ttk elements
style = ttk.Style()
style.theme_use('default')
style.configure('TFrame', background='white')
style.configure('TLabel', background='white')

# Set the window icon + title
ico = Image.open('logos/logo_small_solo_cropped.png')
photo = ImageTk.PhotoImage(ico)
app.wm_iconphoto(False, photo)
app.title("Waste Wizard")

# Add a frame to set the size of the window
outer_frame = ttk.Frame(app, padding=(3, 3, 12, 12))

# Add a frame to display images
left_frame = ttk.Frame(outer_frame, borderwidth=5, width=620, height=600)  # relief="ridge", width=620, height=600)

# Define the logo to be displayed as the first image, within a label in the image frame
img_logo = Image.open("logos/logo_big.png")
photo = ImageTk.PhotoImage(img_logo)
img_lbl = Label(left_frame, image=photo, bd=0)
img_lbl.image = photo
img_lbl.configure(highlightthickness=0)
img_lbl.pack()
app.update()
print("logo: (", photo.height(), photo.width(), ")")

# Define a label to display recycling info
info_lbl = ttk.Label(outer_frame, text=welcome_text, width=info_label_width)  # , wraplengt=info_label_width*6)


# LOGIC
def get_recycling_info(barcode):
    # enable scan button
    # scan_btn.grid(column=0, row=3, sticky=(N, W), padx=10)
    recycling_info_text = "Getting your info's ..."
    info_lbl.config(text=recycling_info_text)

    # request
    try:
        response = requests.get(f'http://localhost:8080/product?barcode={barcode.data.decode("utf-8")}')

        response = response.json()
        recycling_info_text = "TODO: build recycling info text"
    except:
        print("Can not establish connection to backend")
        recycling_info_text = "Server down"

    try:
        # TODO response checken, falls artikel nicht gefunden wurde -> not_found image + text
        u = urlopen(response['image'])
        raw_data = u.read()
        u.close()
        # TODO resize image
        photo = ImageTk.PhotoImage(data=raw_data)
    except:
        print("Can not open product image")
        img_not_found = Image.open("logos/no_image.png")
        photo = ImageTk.PhotoImage(img_not_found)

    # show recycling info
    img_lbl.configure(image=photo)
    img_lbl.image = photo
    info_lbl.config(text=recycling_info_text)


def scan_barcode():
    # disable scan button
    scan_btn["state"] = "disabled"
    info_lbl.config(text=scanning_text)

    keep_looping = True
    # Capture frame from the camera
    ret, video_frame = vid.read()

    if ret:
        video_frame = imutils.resize(video_frame, width=500)
        # print("video: ", video_frame.shape)
        # Convert the frame to grayscale
        gray = cv2.cvtColor(video_frame, cv2.COLOR_BGR2GRAY)

        # Detect barcodes in the frame
        barcodes = pyzbar.decode(gray)

        # check if barcodes were found
        if barcodes:
            if len(barcodes) > 1:
                print("Found more than one barcode in the frame, try again")
                info_lbl.config(text=scanning_error_text)
            else:
                for barcode in barcodes:
                    barcode_data = barcode.data.decode("utf-8")
                    barcode_type = barcode.type
                    print("Barcode Type:", barcode_type)
                    print("Barcode Data:", barcode_data)
                    keep_looping = False

        # TODO redo roi
        # Draw a Region of Interest (ROI) rectangle on the frame
        roi_start_x = 10
        roi_start_y = 40
        roi_end_x = 490
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


# Define the scan button
scan_btn = ttk.Button(outer_frame, text="Scan barcode", command=scan_barcode)

# Place all within the main window
outer_frame.grid(column=0, row=0, sticky=(N, S, E, W))
left_frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
info_lbl.grid(column=3, row=0, columnspan=2, sticky=(N, W))
scan_btn.grid(column=0, row=3, sticky=(N, W), padx=10)
app.columnconfigure(0, weight=1)
app.rowconfigure(0, weight=1)
outer_frame.columnconfigure(0, weight=3)
outer_frame.columnconfigure(1, weight=3)
outer_frame.columnconfigure(2, weight=3)
outer_frame.columnconfigure(3, weight=1)
outer_frame.columnconfigure(4, weight=1)
outer_frame.rowconfigure(1, weight=1)

app.mainloop()
