# Tutorial #7
# -----------
#
# Counting colored objects by finding connected components in the binary image. Modify the binary image to improve the
# results.

import cv2
import numpy as np

# Goal: Count the number of green smarties in the images
# Define green in HSV
hue = 60  # 60 is pure green
hue_range = 10
saturation = 155
saturation_range = 100
value = 155
value_range = 100
lower_green = np.array(
    [hue - hue_range, saturation - saturation_range, value - value_range]
)
upper_green = np.array(
    [hue + hue_range, saturation + saturation_range, value + value_range]
)

# Load image
img = cv2.imread("./tutorials/data/images/smarties01.JPG", cv2.IMREAD_COLOR)
# Check if image is loaded fine
if img is None:
    raise Exception("Could not read image")
img = cv2.resize(img, (800, 600))

# Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Create a mask
mask = cv2.inRange(hsv, lower_green, upper_green)

# TODO Modify the mask image with dilation or erosion 
# in order to avoid very small connected components
# See https://docs.opencv.org/master/db/df6/tutorial_erosion_dilatation.html
# for morphological operations in OpenCV

# TODO Find connected components, see 
# https://docs.opencv.org/4.x/d3/dc0/group__imgproc__shape.html#ga107a78bf7cd25dec05fb4dfc5c9e765f for documentation

# TODO Loop over all (reasonable) found connected components

# TODO (Optional) check size and roundness as plausibility

# TODO Find and draw center

# TODO Find and draw bounding box

# TODO end loop here

# TODO Print out number of connected components
print("We have found x green smarties.")

# Show the original image with drawings in one window
cv2.imshow("Original image", img)

# Show the mask image in another window
cv2.imshow("Mask image", mask)
# cv2.imwrite('mask.jpg',mask)

cv2.waitKey(0)
cv2.destroyAllWindows()
