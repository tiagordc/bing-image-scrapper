import argparse, os, imghdr
from PIL import Image

# Crop images by YOLO class

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True, help="path to directory of images")
    ap.add_argument("-c", "--crop", required=True, help="YOLO class to crop")
    args, unknown = ap.parse_known_args()

    folder = args.folder
    if os.path.isabs(folder): directory = folder
    else: directory = os.path.sep.join(["data", args.folder])

    classesFile = os.path.join(directory, "classes.txt")
    with open(classesFile) as f:
        index = [line.rstrip() for line in f].index(args.crop)

    cropDir = directory + "_" + args.crop
    if (os.path.exists(cropDir) == False): 
        os.makedirs(cropDir)

    for this in os.listdir(directory):

        fileName = os.path.splitext(this)[0].lower()
        extension = os.path.splitext(this)[1].lower()
        filePath = os.path.join(directory, this)
        noExtension = os.path.splitext(filePath)[0]

        if extension == ".txt" and this != "classes.txt" and os.path.exists(noExtension + ".jpg"):

            with open(filePath) as f:
                labels = [line.rstrip().split(' ') for line in f]

            cropLabels = [x for x in labels if int(x[0]) == index]

            with Image.open(noExtension + ".jpg") as img:
                
                labelIndex = 0

                for label in cropLabels:

                    # yolo : (idx center_x_ratio, center_y_ratio, width_ratio, height_ratio)
                    x = float(label[1]) * img.width
                    y = float(label[2]) * img.height
                    w = float(label[3]) * img.width
                    h = float(label[4]) * img.height
                    x = x - w/2
                    y = y - h/2
                    r = x + w
                    l = y + h

                    labelName = f'{fileName}_{labelIndex}.jpg'
                    labelIndex += 1

                    with img.crop((int(x), int(y), int(r), int(l))) as crop:
                        crop.save(os.path.join(cropDir, labelName))

            print(fileName)