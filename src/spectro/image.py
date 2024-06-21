import numpy as np
from pathlib import Path
from typing import Tuple
import cv2


def load_image_from_path(path: str | Path) -> cv2.Mat:
    # Make sure image is in BGR format
    return cv2.imread(path)


def load_image_from_bytes(bytes: bytes) -> cv2.Mat:
    nparr = np.frombuffer(bytes, np.uint8)
    return cv2.imdecode(nparr, cv2.IMREAD_COLOR)


def find_patch_position(image: cv2.Mat) -> Tuple[int, int, int, int, float]:
    grey = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    blurred = cv2.GaussianBlur(grey, (5, 5), 0)

    # Thresholding
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the contour with the largest area
    largest_contour = max(contours, key=cv2.contourArea)

    # Get the bounding rectangle of the largest contour
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Find the rotation of the rectangle
    rect = cv2.minAreaRect(largest_contour)
    rotation_angle = rect[2]

    # Rotate the image

    return (x, y, w, h, rotation_angle)


def extract_patch(
    image: cv2.Mat, position: Tuple[int, int, int, int, float]
) -> cv2.Mat:
    x, y, w, h, rotation_angle = position

    # Rotate the image
    rotated = cv2.warpAffine(
        image,
        cv2.getRotationMatrix2D((x + w / 2, y + h / 2), rotation_angle, 1.0),
        (image.shape[1], image.shape[0]),
    )

    # Extract the patch
    patch = rotated[y : y + h, :]

    # Rotate the patch to make its longer side horizontal
    if h > w:
        patch = cv2.rotate(patch, cv2.ROTATE_90_CLOCKWISE)

    return patch
