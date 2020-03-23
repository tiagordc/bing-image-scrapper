import argparse, os, imghdr
from PIL import Image

# Convert all images to jpeg and try to fix error: Corrupt JPEG data bad Huffman code

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True, help="path to directory of images")
    args, unknown = ap.parse_known_args()

    folder = args.folder
    if os.path.isabs(folder): directory = folder
    else: directory = os.path.sep.join(["data", args.folder])

    images = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff", ".jfif"]

    converted = 0
    rewrite = 0

    for this in os.listdir(directory):

        extension = os.path.splitext(this)[1].lower()
        filePath = os.path.join(directory, this)
        noExtension = os.path.splitext(filePath)[0]

        if os.path.isfile(filePath) and extension in images:

            jpegPath = noExtension + ".jpg"

            with Image.open(filePath) as im:
                im.convert('RGB').save(jpegPath)

            if extension == ".jpg":
                rewrite += 1
            else:
                os.remove(filePath)
                converted += 1

    print(f"Converted {converted} | Rewrite {rewrite}")
