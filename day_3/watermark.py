import cv2
import numpy as np

image_path = r"Path of the image whose watermark needs to be removed"
image = cv2.imread(image_path)

# Converting the image to HSV
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Masking the blue colours of the image
lower_blue = np.array([85, 20, 155])
upper_blue = np.array([105, 205, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
kernel = np.ones((3, 3), np.uint8)
mask = cv2.dilate(mask, kernel, iterations=3)

inpainted = cv2.inpaint(image, mask, inpaintRadius=3, flags=cv2.INPAINT_TELEA)
resize_factor = 0.2
resize = cv2.resize(inpainted, (0, 0), fx=resize_factor, fy=resize_factor)
# cv2.imwrite("output.jpg", inpainted)
cv2.imshow("Watermark Removed", resize)
cv2.waitKey(0)
