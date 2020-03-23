import argparse, os, imghdr, cv2, pytesseract, numpy as np, imutils
from PIL import Image

# Run OCR on a specific folder

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True, help="path to directory of images")
    ap.add_argument("-o", "--ocr", required=True, help="class to crop")
    args, unknown = ap.parse_known_args()

    folder = args.folder
    if os.path.isabs(folder): directory = folder
    else: directory = os.path.sep.join(["data", args.folder])

    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    for this in os.listdir(directory):

        fileName = os.path.splitext(this)[0].lower()
        extension = os.path.splitext(this)[1].lower()
        filePath = os.path.join(directory, this)
        noExtension = os.path.splitext(filePath)[0]

        if extension == ".jpg":
            
            img = cv2.imread(filePath)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            text = pytesseract.image_to_string(img, config=args.ocr) # "-c tessedit_char_whitelist=0123456789.,"
            print(f'{this}: {text}')
