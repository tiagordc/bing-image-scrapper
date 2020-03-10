import argparse, os, random, string, shutil
from imageai.Detection import ObjectDetection

# Remove images with certain objects detected

PREDICTION = []
DETECTION_EXCLUDE = ["person", "tv", "laptop", "cell phone"]
DETECTION_INCLUDE = []

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True, help="path to output directory of images")
    # TODO: list files or delete
    args, unknown = ap.parse_known_args()

    directory = os.path.sep.join(["data", args.folder])

    negative = directory + "_Negative"
    if not os.path.exists(negative): os.makedirs(negative)

    positive = directory + "_Positive"
    if not os.path.exists(positive): os.makedirs(positive)

    # https://github.com/OlafenwaMoses/ImageAI/releases/download/1.0/yolo-tiny.h5
    model_path = "./models/yolo-tiny.h5"

    detector = ObjectDetection()
    detector.setModelTypeAsTinyYOLOv3()
    detector.setModelPath(model_path)
    detector.loadModel()

    for this in os.listdir(directory):
        
        filePath = os.path.join(directory, this)
        negativePath = os.path.join(negative, this)
        positivePath = os.path.join(positive, this)
        detection = detector.detectObjectsFromImage(input_image=filePath, output_image_path=negativePath)

        if len(detection) > 0:

            features = [ x["name"] for x in detection ]
            shouldExclude = any(elem in features for elem in DETECTION_EXCLUDE)
            os.remove(negativePath) # keep the original file

            if shouldExclude:
                shutil.copyfile(filePath, positivePath) 
            else:
                shutil.copyfile(filePath, negativePath)

            for eachItem in detection:
                print(this, " - ", eachItem["name"] , " - ", eachItem["percentage_probability"])
