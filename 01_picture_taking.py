import cv2
import time
import os
import pathlib

if __name__ == '__main__':
    #####################
    # 1. Setup the camera
    #####################
    camera_channel = 1
    cap = cv2.VideoCapture(camera_channel)

    
    current_dir = pathlib.Path(__file__).parent.resolve()
    image_dir = os.path.join(current_dir, "captured_images")

    k = 0
    while True:
        ##########################################
        # 2. Show captured images
        ##########################################
        _, image = cap.read()

        cv2.imshow('captured image', image)
        time.sleep(3)

        ##########################################
        # 3. Save images once every three seconds
        ##########################################
        image_name = "test_" + str(k) + ".png"
        image_path = os.path.join(image_dir, image_name)
        cv2.imwrite(image_path, image)
        print(f'{image_name} is saved ... ')

        k += 1
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()