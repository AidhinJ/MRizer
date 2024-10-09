import cv2
import numpy as np

# Read HDR image
hdr_image = cv2.imread('DSCN1990.JPG', cv2.IMREAD_ANYDEPTH)

# Convert HDR image to float32
hdr_image_float = hdr_image.astype(np.float32)

# Apply Reinhard tonemapping
tonemapped_image = cv2.createTonemapReinhard().process(hdr_image_float)

# Convert tonemapped image to uint8
tonemapped_image_uint8 = tonemapped_image.astype(np.uint8)

# Display original HDR image and tonemapped image
cv2.imshow('HDR Image', hdr_image)
cv2.imshow('Tonemapped Image', tonemapped_image_uint8)

cv2.waitKey(0)
cv2.destroyAllWindows()
