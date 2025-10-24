# Tutorial #6
# -----------
#
# Playing around with colors. We convert some values from RGB to HSV and then find colored objects in the image and mask
# them out. Includes a color picker on double-click now. The RGB version is meant to demonstrate that this does not work
# in RGB color space.

import numpy as np
import cv2

# Print keyboard usage
# NOTE: Had to change input mapping due to Linux-specific issue where key case is not detected.
string: str = """
This is a HSV color detection demo. Use the keys to adjust the selection color in HSV space. Circle in bottom left.
The masked image shows only the pixels with the given HSV color within a given range.
Use g/h to de-/increase the hue.
Use a/s to de-/increase the saturation.
Use c/v to de-/increase the (brightness) value.

Double-click an image pixel to select its color for masking.
"""

# Capture webcam image
cap: cv2.VideoCapture = cv2.VideoCapture(0)

# Get camera image parameters from get()
width: int = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height: int = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
codec: int = int(cap.get(cv2.CAP_PROP_CODEC_PIXEL_FORMAT))

string += f"""
Video properties:
Width: {width}
Height: {height}
Codec: {codec}
"""
print(string)

# Drawing helper variables
thick = 10
thin = 3
thinner = 2
font_size_large = 3
font_size_small = 1
font_size_smaller = 0.6
font = cv2.FONT_HERSHEY_SIMPLEX

blue: tuple = (255, 0, 0)
green: tuple = (0, 255, 0)
red: tuple = (0, 0, 255)

# Exemplary color conversion (only for the class), tests usage of cv2.cvtColor
hue = 120
hue_range = 10
saturation = 20
saturation_range = 100
value = 60
value_range = 100
cv2.namedWindow("Original", cv2.WINDOW_AUTOSIZE)

# Callback to pick the color on double click
def color_picker(event, x, y, flags, param):
    global hue, saturation, value
    if event == cv2.EVENT_LBUTTONDBLCLK:
        (h, s, v) = hsv[y, x]
        hue = int(h)
        saturation = int(s)
        value = int(v)
        print("New color selected:", (hue, saturation, value))


while True:
    # Get video frame (always BGR format!)
    ret, frame = cap.read()
    if not ret:
        print("Could not start video camera")
        break

    # Copy image to draw on
    img = frame.copy()

    # Compute color ranges for display
    min: np.ndarray = np.array([
        hue - hue_range, saturation - saturation_range, value - value_range
    ])
    max: np.ndarray = np.array([
        hue + hue_range, saturation + saturation_range, value + value_range
    ])

    # TODO Draw selection color circle and text for HSV values
    img = cv2.circle(img, (100, 40), thick, blue, -1)
    img = cv2.putText(img, f"H: {hue}", (10, 20), font, font_size_smaller, blue, thinner)
    img = cv2.putText(img, f"S: {saturation}", (10, 40), font, font_size_smaller, blue, thinner)
    img = cv2.putText(img, f"V: {value}", (10, 60), font, font_size_smaller, blue, thinner)

    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # TODO Create a bitwise mask

    # TODO Apply mask

    cv2.imshow("Original", img)

    # TODO Show the masked image in another window

    # TODO Show the mask image in another window

    # User Input
    key: int = cv2.waitKey(10)
    if key == ord("g") or key == ord("h"):
        hue += 1 if key == ord("h") else -1
    if key == ord("s") or key == ord("S"):
        saturation += 1 if key == ord("s") else -1
    if key == ord("v") or key == ord("V"):
        value += 1 if key == ord("v") else -1
    if key == ord("q") or key == ord("Q"):
        break

cap.release()
cv2.destroyAllWindows()
