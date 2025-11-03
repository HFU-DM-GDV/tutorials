# Tutorial #7
# -----------
#
# Counting colored objects by finding connected components in the binary image. Modify the binary image to improve the
# results.

from calendar import c
from turtle import lt
import cv2
import numpy as np

# Goal: Count the number of green smarties in the images
# define green in HSV
hue = 60  # 60 is pure green
hue_range = 10
saturation = 155
saturation_range = 100
value = 155
value_range = 100
lower_green = np.array([hue - hue_range, saturation - saturation_range, value - value_range])
upper_green = np.array([hue + hue_range, saturation + saturation_range, value + value_range])

# Load image
img = cv2.imread("./tutorials/data/images/smarties02.JPG", cv2.IMREAD_COLOR)
# Check if image is loaded fine
if img is None:
    raise Exception("Could not read image")
img = cv2.resize(img, (800, 600))

# Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Create a mask
mask = cv2.inRange(hsv, lower_green, upper_green)

# Morphological operations code
# Optional mapping of values with morphological shapes


def morph_shape(val):
    if val == 0:
        return cv2.MORPH_RECT
    elif val == 1:
        return cv2.MORPH_CROSS
    elif val == 2:
        return cv2.MORPH_ELLIPSE


# Dilation with parameters
def dilatation(img, size, shape):
    kernel = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1), (size, size))
    return cv2.dilate(img, kernel)


# Erosion with parameters
def erosion(img, size, shape):
    kernel = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1), (size, size))
    return cv2.erode(img, kernel)


# Opening with parameters
def opening(img, size, shape):
    kernel = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1), (size, size))
    return cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)


# Closing with parameters
def closing(img, size, shape):
    kernel = cv2.getStructuringElement(shape, (2 * size + 1, 2 * size + 1), (size, size))
    return cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)


# Debug mask images to illustrate morphological operations
# cv2.imshow('Mask image',mask)
# cv2.waitKey(0)

# Apply morphological operations
# See https://docs.opencv.org/master/db/df6/tutorial_erosion_dilatation.html
kernel_size = 3
kernel_shape = morph_shape(2)
mask = opening(mask, kernel_size, kernel_shape)
mask = closing(mask, kernel_size, kernel_shape)

# Find connected components
connectivity = 8
(numLabels, labels, stats, centroids) = cv2.connectedComponentsWithStats(mask, connectivity=connectivity, ltype=cv2.CV_32S)

# Helper variables for drawing and candidate rejection
red_BGR = (0, 0, 255)
green_BGR = (0, 255, 0)
circle_size = 10
circle_thickness = 5
min_size = 10
expected_roundness = 0.5
numRejected = 1

# Go through all (reasonable) found connected components
for i in range(1, numLabels):
    # Check size and roundness as plausibility
    x = stats[i, cv2.CC_STAT_LEFT]
    y = stats[i, cv2.CC_STAT_TOP]
    w = stats[i, cv2.CC_STAT_WIDTH]
    h = stats[i, cv2.CC_STAT_HEIGHT]

    if w < min_size or h < min_size:
        print("Found a too small component.")
        numRejected += 1
        continue  # Found component is too small to be correct
    if w > h:
        roundness = 1.0 / (w / h)
    elif h > w:
        roundness = 1.0 / (h / w)
    if roundness < expected_roundness:
        print("Found a component that is not round enough.")
        numRejected += 1

        # Ratio of width and height is not suitable
        continue

    # Find and draw center
    center = centroids[i]
    center = np.round(center)
    center = center.astype(int)
    cv2.circle(img, center, circle_size, red_BGR, circle_thickness)

    # Find and draw bounding box
    cv2.rectangle(img, (x, y), (x + w, y + h), green_BGR, 3)

# Print out number of connected components
print("We have found", str(numLabels - numRejected), "green smarties.")

# Show the original image with drawings in one window
cv2.imshow("Original image", img)

# Show the mask image in another window
cv2.imshow("Mask image", mask)
cv2.imwrite("mask.jpg", mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
