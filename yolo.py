import argparse, os, imghdr
from PIL import Image

# check yolo 

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True, help="path to directory of images")
    ap.add_argument("-c", "--crop", required=True, help="YOLO class to crop")
    args, unknown = ap.parse_known_args()

    folder = args.folder
    if os.path.isabs(folder): directory = folder
    else: directory = os.path.sep.join(["data", args.folder])

    classesFile = os.path.join(directory, "classes.txt")
    classes = {}

    with open(classesFile) as f:
        index = 0
        for line in f:
            classes[index] = { "name": line.rstrip(), "count": 0 }
            index += 1
    
    missing = []

    for this in os.listdir(directory):

        fileName = os.path.splitext(this)[0].lower()
        extension = os.path.splitext(this)[1].lower()
        filePath = os.path.join(directory, this)
        noExtension = os.path.splitext(filePath)[0]

        if extension == ".txt" and this != "classes.txt":
            if os.path.exists(noExtension + ".jpg"):
                with open(filePath) as f:
                    for line in f:
                        curr = classes.get(int(line.rstrip().split(' ')[0]))
                        curr["count"] += 1
            else:
                missing.append(this)
        
        if extension == ".jpg":
            if not os.path.exists(noExtension + ".txt"):
                missing.append(this)

    if len(missing) > 0:
        print("missing: " + ', '.join(missing))

    for index in classes:
        item = classes.get(index)
        print(f'{item["name"]}: {item["count"]}')