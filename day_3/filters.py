import cv2

# Load the image
image = cv2.imread(r"Path of the image to be blurred")

resize_factor = 0.2
resized_image = cv2.resize(image, (0, 0), fx=resize_factor, fy=resize_factor)

blurred_image = cv2.GaussianBlur(resized_image, (15, 15), 0)

cv2.imshow('Original Image', resized_image)
cv2.imshow('Blurred Image', blurred_image)

cv2.waitKey(0)
