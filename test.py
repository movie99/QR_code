import cv2
import numpy as np

def wait_until_closed(window_name):
    while cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE) >= 1.0:
        print(cv2.getWindowProperty(window_name, cv2.WND_PROP_VISIBLE))
        k = cv2.waitKey(50)
        if k == 27 :  # Break the loop if the user presses the 'ESC' key
            break

# OpenCV window setup
window_name = "MyWindow"
cv2.namedWindow(window_name)

# Show random images until the user closes the window

img = np.random.randint(0, 255, (300, 400, 3), dtype=np.uint8)
cv2.imshow(window_name, img)
wait_until_closed(window_name)

# Print a message when the window is closed
print("Window closed by user")

# Continue with the rest of your code
cv2.destroyAllWindows()
