from imutils import paths
import numpy as np
import argparse
import cv2
import os

ap = argparse.ArgumentParser()
ap.add_argument("-w", "--watermark", default = r"C:\Users\suyas\Desktop\DigitalWartermarking\Images\Watermark\enter.png", help="path to watermark image (assumed to be transparent PNG)")

ap.add_argument("-i", "--input", default = r"C:\Users\suyas\Desktop\DigitalWartermarking\Images\Input", help="path to the input directory of images")

ap.add_argument("-o", "--output", default = r"C:\Users\suyas\Desktop\DigitalWartermarking\Images\Output", help="path to the output directory")

ap.add_argument("-a", "--alpha", type=float, default=0.000, help="alpha transparency of the overlay (smaller is more transparent)")

ap.add_argument("-c", "--correct", type=int, default=1, help="flag used to handle if bug is displayed or not")

args = vars(ap.parse_args())
alpha= 1/(1-args["alpha"])
beta = (1 -1/(1- args["alpha"]))
print("alpha" + str(alpha))
print("beta" + str(beta))
# load the watermark image, making sure we retain the 4th channel
# which contains the alpha transparency
watermark = cv2.imread(args["watermark"], cv2.IMREAD_UNCHANGED)
(wH, wW) = watermark.shape[:2]
# split the watermark into its respective Blue, Green, Red, and
# Alpha channels; then take the bitwise AND between all channels
# and the Alpha channels to construct the actual watermark
# NOTE: I'm not sure why we have to do this, but if we don't,
# pixels are marked as opaque when they shouldn't be
if args["correct"] > 0:
    (B, G, R, A) = cv2.split(watermark)
    B = cv2.bitwise_and(B, B, mask=A)
    G = cv2.bitwise_and(G, G, mask=A)
    R = cv2.bitwise_and(R, R, mask=A)
    watermark = cv2.merge([B, G, R, A])
# loop over the input images
for imagePath in paths.list_images(args["input"]):
# load the input image, then add an extra dimension to the
# image (i.e., the alpha transparency)
    image = cv2.imread(imagePath)
    (h, w) = image.shape[:2]
    image = np.dstack([image, np.ones((h, w), dtype="uint8") *255])
# construct an overlay that is the same size as the input image, (using an extra dimension for the alpha transparency),then add the watermark to the overlay in the bottom-right corner
    overlay = np.zeros((h, w, 4), dtype="uint8")
    overlay[h - wH - 10:h - 10, w - wW - 10:w - 10] = watermark
# blend the two images together using transparent overlays
    output = image.copy()
    cv2.addWeighted(output, alpha, overlay, beta, 0, output)
# write the output image to disk
    filename = imagePath[imagePath.rfind(os.path.sep) + 1:]
    p = os.path.sep.join((args["output"], filename))
    cv2.imwrite(p, output)