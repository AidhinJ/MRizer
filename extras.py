import tkinter as tk
import os
import cv2


class CollapsibleFrame(tk.LabelFrame):
    def __init__(self, master, title, size=5, **kwargs):
        super().__init__(master, text=title+" >", **kwargs)

        self._is_open = False
        self._contents = tk.Frame(self)

        # If we collapse the widgets the size of the self._contents remains, this is a simple solution
        default_size = tk.Frame(self, width=size, height=size, bg='')
        default_size.pack()

        self.bind("<Button-1>", self._toggle)

    def _toggle(self, event):
        if self._is_open:
            self._contents.pack_forget()
            self._is_open = False
        else:
            self._contents.pack()
            self._is_open = True


            
def remove_emoji(text):
    str = ''
    for char in text:
        if char.isalnum() or char in '!@#$%^&*()_+-=[]{};:,./<>?`~\n':
            str += char
        else:
            str+=' '
    return str.strip()

def custom_paste(event):
    try:
        event.widget.delete("sel.first", "sel.last")  # Remove selected text
    except:
        pass
    clipboard_text = root.clipboard_get()
    event.widget.insert("insert", remove_emoji(clipboard_text))  # Paste from clipboard
    return "break"  # Prevent default paste behavior
            
def image_resize(dir=None, width_height=(1920, 1080)):
    """Resize chosen image."""
    image = cv2.imread(dir)
    if image is None:
        return
    height, width, channels = image.shape
    # Checks if aspect ratio is 16:9 kinda silly but works
    if (height / width) == 0.5625:
        # Resize to a specific width and height
        resized_image = cv2.resize(image, width_height, interpolation=cv2.INTER_CUBIC) 
        cv2.imwrite(dir, resized_image)

def detect_faces(image_path, imshow=False):
    # Load the pre-trained Haar cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier('/home/c3po/.local/lib/python3.8/site-packages/cv2/data/haarcascade_frontalface_default.xml')

    # Read the image in color
    img = cv2.imread(image_path)
    img = cv2.resize(img, None, fx=.1, fy=.1, interpolation=cv2.INTER_AREA)

    # Convert the image to grayscale (Haar cascade works better in grayscale)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect faces in the image
    faces = face_cascade.detectMultiScale(gray, 1.2, 4)

    if imshow:
        # Draw a rectangle around each detected face
        # Display the image with detected faces
        # Wait for a key press to quit
        # Close all open windows
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        cv2.imshow('Image with Faces', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    return faces


if __name__ == "__main__":
    d = detect_faces('/home/c3po/Desktop/Photos/MR634781 - Bank/R0023789.JPG', imshow=True)
    print(d)
