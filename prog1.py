import cv2
import numpy as np

# Global variables
drawing = False
last_x, last_y = -1, -1
brush_radius = 5
color = (0, 0, 0)

def draw_circle(event, x, y, flags, param):
    global drawing, last_x, last_y, color, brush_radius
    
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        last_x, last_y = x, y
        
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
    
    if drawing and event == cv2.EVENT_MOUSEMOVE:
        cv2.circle(canvas, (x, y), brush_radius, color, -1)
        
        # Update the last_x and last_y to the current position
        last_x, last_y = x, y

def nothing(x):
    pass

# Create a blank canvas
canvas = np.ones((600, 800, 3), np.uint8) * 255

# Create a named window
cv2.namedWindow('Paint Application')

# Create trackbars for color selection
cv2.createTrackbar('Blue', 'Paint Application', 0, 255, nothing)
cv2.createTrackbar('Green', 'Paint Application', 0, 255, nothing)
cv2.createTrackbar('Red', 'Paint Application', 0, 255, nothing)

# Create a trackbar for brush radius
cv2.createTrackbar('Brush Radius', 'Paint Application', 1, 20, nothing)

# Set up the mouse callback
cv2.setMouseCallback('Paint Application', draw_circle)

while True:
    # Get the current trackbar positions
    blue = cv2.getTrackbarPos('Blue', 'Paint Application')
    green = cv2.getTrackbarPos('Green', 'Paint Application')
    red = cv2.getTrackbarPos('Red', 'Paint Application')
    brush_radius = cv2.getTrackbarPos('Brush Radius', 'Paint Application')
    
    # Update the color
    color = (blue, green, red)
    
    cv2.imshow('Paint Application', canvas)
    
    # Press 'Esc' to exit the application
    if cv2.waitKey(1) == 27:
        break

cv2.destroyAllWindows()
