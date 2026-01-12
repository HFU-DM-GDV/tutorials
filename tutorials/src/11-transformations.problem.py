# Tutorial #11
# ------------
#
# Geometric transformations a.k.a. image warping.

import numpy as np
import cv2

# Load image and resize for better display
img = cv2.imread("./tutorials/data/images/nl_clown.jpg", cv2.IMREAD_COLOR)
img = cv2.resize(img, (400, 400), interpolation=cv2.INTER_CUBIC)
rows, cols, dims = img.shape

# Define translation matrix for translation about 100 pixels to the right and 50 up
T_translation = np.float32([[1, 0, 100], [0, 1, 50]])

# A pretty print for the matrix:
print("\nTranslation\n", "\n".join(["\t".join(["%03.3f" % cell for cell in row]) for row in T_translation]))

# Apply translation matrix on image using cv2.warpAffine
dst_translation = cv2.warpAffine(img, T_translation, (cols + 100, rows + 50))

# Define anisotropic scaling matrix that stretches to double length horizontally
T_anisotropic_scaling = np.float32([[2, 0, 0], [0, 2, 0]])
# and squeezes vertically to the half height


print(
    "\nAnisotropic scaling\n",
    "\n".join(["\t".join(["%03.3f" % cell for cell in row]) for row in T_anisotropic_scaling]),
)

#  Apply anisotropic scaling matrix on image using cv2.warpAffine
dst_anisotropic_scaling = cv2.warpAffine(img, T_anisotropic_scaling, (int(cols*2), int(rows*2)))

# Define rotation matrix for 45° clockwise rotation
phi_deg = 45.0
phi_rad = (np.pi / 180.0) * phi_deg
T_rotation = np.float32([[np.cos(phi_rad), -np.sin(phi_rad), 0], [np.sin(phi_rad), np.cos(phi_rad), 0]])

print("\nRotation\n", "\n".join(["\t".join(["%03.3f" % cell for cell in row]) for row in T_rotation]))

# Apply rotatio matrix on image using cv2.warpAffine
dst_rotation = cv2.warpAffine(img, T_rotation, (cols, rows))

# Rotate around image center for 45° counterclockwise using cv2.getRotationMatrix2D
center = ((cols - 1) / 2.0, (rows - 1) / 2.0)
scale_factor = 1
T_rotation_around_center = cv2.getRotationMatrix2D(center, phi_deg, scale_factor)

print(
    "\nRotation around center\n",
    "\n".join(["\t".join(["%03.3f" % cell for cell in row]) for row in T_rotation_around_center]),
)

# Apply rotatio matrix on image using cv2.warpAffine
dst_rotation_around_center = cv2.warpAffine(img, T_rotation_around_center, (cols, rows))

# Show the original and resulting images
cv2.imshow("Original", img)
cv2.imshow("Translation", dst_translation)
cv2.imshow("Anisotropic scaling", dst_anisotropic_scaling)
cv2.imshow("Rotation", dst_rotation)
cv2.imshow("Rotation around center", dst_rotation_around_center)

# Keep images open until key pressed
cv2.waitKey(0)
cv2.destroyAllWindows()
