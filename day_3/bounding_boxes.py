import cv2

image = cv2.imread(r"Path of the image")

# Converting to gray scaled image
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

edges = cv2.Canny(gray_image, 100, 200)

contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2) 

cv2.imshow('Detected Objects', image)

cv2.waitKey(0)
cv2.destroyAllWindows()
