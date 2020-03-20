import argparse, os, imghdr
from PIL import Image

# Convert all images to jpeg

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True, help="path to directory of images")
    args, unknown = ap.parse_known_args()

    folder = args.folder
    if os.path.isabs(folder): directory = folder
    else: directory = os.path.sep.join(["data", args.folder])

    for this in os.listdir(directory):

        filePath = os.path.join(directory, this)
        if os.path.isfile(filePath):

            what = imghdr.what(filePath)

            if what is None: continue

            if what is "jpeg":
                try:
                    im = Image.open(filePath)
                    im.verify() #I perform also verify, don't know if he sees other types o defects
                    im.close() #reload is necessary in my case
                    im = Image.open(filePath) 
                    im.transpose(Image.FLIP_LEFT_RIGHT)
                    im.close()
                except Exception as xpto: 
                    pass
            else:
                jpegPath = os.path.splitext(filePath)[0] + ".jpg"
                with Image.open(filePath) as im:
                    rgb_im = im.convert('RGB')
                    rgb_im.save(jpegPath)
                os.remove(filePath)


    # im = Image.open("Ba_b_do8mag_c6_big.png")
    # rgb_im = im.convert('RGB')
    # rgb_im.save('colors.jpg')