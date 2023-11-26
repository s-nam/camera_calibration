import cv2
import pathlib
import os

def load_coefficients(path):
    """ Loads camera matrix and distortion coefficients. """
    # FILE_STORAGE_READ
    cv_file = cv2.FileStorage(path, cv2.FILE_STORAGE_READ)

    # note we also have to specify the type to retrieve other wise we only get a
    # FileNode object back instead of a matrix
    camera_matrix = cv_file.getNode("K").mat()
    dist_matrix = cv_file.getNode("D").mat()

    cv_file.release()
    return [camera_matrix, dist_matrix]

def undistort_image(image, K, D):
    h, w = image.shape[:2]
    new_camera_matrix, roi = cv2.getOptimalNewCameraMatrix(K, D, (w,h), 1, (w,h))
    
    # Undistort the image
    dst = cv2.undistort(image, K, D, None, new_camera_matrix)

    # Crop the image (optional)
    x, y, w, h = roi
    dst = dst[y:y+h, x:x+w]
    
    return dst

def resize_image(image, scale_percent):
    width = int(image.shape[1] * scale_percent / 100)
    height = int(image.shape[0] * scale_percent / 100)
    dim = (width, height)
    resized = cv2.resize(image, dim, interpolation=cv2.INTER_AREA)
    return resized

if __name__ == '__main__':
    current_dir = pathlib.Path(__file__).parent.resolve()
    calib_file_path = os.path.join(current_dir, "intrinsic_params.yaml")
    img_file_path = os.path.join(current_dir, "captured_images", "test_31.png")

    [K, D] = load_coefficients(calib_file_path)
    
    img = cv2.imread(img_file_path)
    print(f'size of the original image = {img.shape}')
    
    calibrated_img = undistort_image(img, K, D)
    print(f'size of the undistored image = {calibrated_img.shape}')

    # Resize the images by 50%
    img_resized = resize_image(img, 50)
    calibrated_img_resized = resize_image(calibrated_img, 50)
    
    cv2.imshow('Original Image', img_resized)
    cv2.imshow('Calibrated Image', calibrated_img_resized)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
