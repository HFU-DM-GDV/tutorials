# Tutorial #10
# ------------
#
# Doing the Fourier Transform for images and back. This code is based on the stackoverflow answer from Fred Weinhaus:
# https://stackoverflow.com/a/59995542

import cv2
import numpy as np

# Global helper variables
window_width = 640
window_height = 480


def get_frequencies(image):
# Convert image to floats and do dft saving as complex output
    dft = cv2.dft(np.float32(image), flags= cv2.DFT_COMPLEX_OUTPUT)
    
# Apply shift of origin from upper left corner to center of image
    dft_shift = np.fft.fftshift(dft)
# Extract magnitude and phase images
    magnitude, phase = cv2.cartToPolar(dft_shift[:, :, 0], dft_shift[:, :, 1])
# Get spectrum for viewing only
    spec = (1 / 20) * np.log(magnitude)
# Return the resulting image (as well as the magnitude and phase for the inverse)
    return spec, magnitude, phase


def create_from_spectrum(magnitude, phase):
# Convert magnitude and phase into cartesian real and imaginary components
    real, fake= cv2.polarToCart(magnitude, phase)
# Combine cartesian components into one complex image
    back = cv2.merge([real, fake])
# Shift origin from center to upper left corner
    back_ishift = np.fft.ifftshift(back)
# Do idft saving as complex output
    img_back = cv2.idft(back_ishift)
# Combine complex components into original image again
    img_back = cv2.magnitude(img_back[:, :, 0], img_back[:, :, 1])
# Re-normalize to 8-bits
    min, max = np.amin(img_back, (0, 1)), np.amax(img_back, (0, 1))
    print(min, max)
    img_back = cv2.normalize(img_back, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    return img_back

# We use a main function this time: see https://realpython.com/python-main-function/ why it makes sense
def main():
    # Load an image, compute frequency domain image from it and display both or vice versa
    image_name = "./tutorials/data/images/chewing_gum_balls01.jpg"

    # Load the image.
    image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
    # check if img is loaded
    if image is None:
        raise Exception("Could not read the image.")
    image = cv2.resize(image, (window_width, window_height))

    # Show the original image
    # Note that window parameters have no effect on MacOS
    title_original = "Original image"
    cv2.namedWindow(title_original, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(title_original, window_width, window_height)
    cv2.imshow(title_original, image)

    # result = get_frequencies(image)
    # result = np.zeros((window_height, window_width), np.uint8)
    result, magnitude, phase = get_frequencies(image)

    # Show the resulting image
    # Note that window parameters have no effect on MacOS
    title_result = "Frequencies image"
    cv2.namedWindow(title_result, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(title_result, window_width, window_height)
    cv2.imshow(title_result, result)

    # back = create_from_spectrum(??)
    # back = np.zeros((window_height, window_width), np.uint8)
    back = create_from_spectrum(magnitude, phase)
    
    # And compute image back from frequencies
    # Note that window parameters have no effect on MacOS
    title_back = "Reconstructed image"
    cv2.namedWindow(title_back, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(title_back, window_width, window_height)
    cv2.imshow(title_back, back)

    key = cv2.waitKey(0)
    cv2.destroyAllWindows()


# Starting the main function
if __name__ == "__main__":
    main()

