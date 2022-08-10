# Note: numpy uses (y,x) convention but most OpenCV functions use (x,y)

import cv2
import numpy as np
import math
import statistics as stat
from matplotlib import pyplot as plt
import glob
import os
import pathlib


# From imutils, added a parameter for specifying the interpolation method
def rotate_bound(image, angle, inter):
    # grab the dimensions of the image and then determine the
    # center
    (h, w) = image.shape[:2]
    (cX, cY) = (w / 2, h / 2)

    # grab the rotation matrix (applying the negative of the
    # angle to rotate clockwise), then grab the sine and cosine
    # (i.e., the rotation components of the matrix)
    M = cv2.getRotationMatrix2D((cX, cY), -angle, 1.0)
    cos = np.abs(M[0, 0])
    sin = np.abs(M[0, 1])

    # compute the new bounding dimensions of the image
    nW = int((h * sin) + (w * cos))
    nH = int((h * cos) + (w * sin))

    # adjust the rotation matrix to take into account translation
    M[0, 2] += (nW / 2) - cX
    M[1, 2] += (nH / 2) - cY

    # perform the actual rotation and return the image
    return cv2.warpAffine(image, M, (nW, nH), flags=inter)

# detects ~30deg offset 1, 2.2
def detect_strong_hlines(image):
    lines = cv2.HoughLines(image, rho=1, theta=np.pi / 180, threshold=200, min_theta=1, max_theta=2.2)

    # Convert to 2d array
    if lines is None:
        return None
    lines = lines[:, 0, :]

    # Filter out lines_detected that are too similar - i.e. close by pixels with similar angle
    strong_lines = [lines[0]]
    for line in lines[1:]:
        count = 0
        for strong_line in strong_lines:
            if abs(line[0] - strong_line[0]) <= 10 and abs(line[1] - strong_line[1] <= math.degrees(5)):
                count += 1
        if count != 0:
            continue
        strong_lines.append(line)

    # Convert the filtered lines_detected to np array for convenience
    strong_lines = np.array(strong_lines)
    return strong_lines


def plot_images(images: list, figure_name: str = 'fig'):
    img1, img2 = images
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.canvas.manager.set_window_title(figure_name)
    fig.set_figheight(6)
    fig.set_figwidth(12)
    ax1.imshow(img1)
    ax2.imshow(img2)
    plt.tight_layout()
    plt.show()


def display_lines(image, lines, color=(255, 0, 0)):
    for line in lines:
        rho = line[0]
        theta = line[1]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * a)
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * a)
        cv2.line(image, (x1, y1), (x2, y2), color, 2)
    return image


# Import image_array
pattern = 'images/*.png'
paths = glob.glob(pattern)
image_array = [cv2.imread(path) for path in paths]
filenames = [os.path.basename(path) for path in paths]

for img, filename in zip(image_array, filenames):
    print(f'File: {filename}')
    # Create copy of img for the output
    img_rotated = img.copy()

    # Convert to greyscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Canny edge detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Detect strong lines
    lines_detected = detect_strong_hlines(edges)
    if lines_detected is None:
        print('No lines detected, no rotation.')
        continue
    print(f'Detected {lines_detected.shape[0]} strong lines =\n{lines_detected}')

    # Add lines_detected to the original img
    img = display_lines(img, lines_detected, color=(0, 255, 0))

    # Calculate the rotation degree
    theta_values = lines_detected[:, 1]
    rad_mode = stat.mode(theta_values)
    deg_mode = math.degrees(rad_mode)
    rotate_deg = 90 - deg_mode

    print(f'Deg_mode = {deg_mode}')
    if abs(rotate_deg) <= 0.5:
        print(f'Document is off by {rotate_deg} degrees - too low, not rotating.\n')
        continue
    print(f'Rotation by: {rotate_deg} degrees\n')

    # Rotate
    img_rotated = rotate_bound(img_rotated, rotate_deg, inter=cv2.INTER_LANCZOS4)

    plot_images([img, img_rotated], filename)

    # Save the rotated image
    output_filename = os.path.splitext(filename)[0] + '-rotated.png'
    output_path = pathlib.Path('output') / output_filename
    cv2.imwrite(str(output_path), img_rotated)
