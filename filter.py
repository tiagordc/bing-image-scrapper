import argparse, os, random, string, shutil
from imageai.Detection import ObjectDetection
from imageai.Prediction import ImagePrediction

# move images to A and B folders based on prediction and detection rules

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True, help="path to output directory of images")
    ap.add_argument("-s", "--strategy", required=True, help="strategy of AB test: Prediction, Detection", default="Detection")
    ap.add_argument("-o", "--objects", required=True, help="list of objects to identify to folder A")
    ap.add_argument("-p", "--probability", required=True, help="minimum probability", default="90")
    args, unknown = ap.parse_known_args()

    threshold = int(args.probability)
    objectsToDetect = args.objects.split(',')
    directory = os.path.sep.join(["data", args.folder])

    folderA = directory + "_A"
    if not os.path.exists(folderA): os.makedirs(folderA)
    else: raise Exception("Folder A already exists")
    folderB = directory + "_B"
    if not os.path.exists(folderB): os.makedirs(folderB)
    else: raise Exception("Folder B already exists")

    # https://github.com/OlafenwaMoses/ImageAI/releases/tag/1.0/

    if args.strategy == "Detection":
        detector = ObjectDetection()
        detector.setModelTypeAsYOLOv3()
        detector.setModelPath("./models/yolo.h5")
        detector.loadModel()
    else:
        prediction = ImagePrediction()
        prediction.setModelTypeAsResNet()
        prediction.setModelPath("./models/resnet50_weights_tf_dim_ordering_tf_kernels.h5")
        prediction.loadModel()

    for this in os.listdir(directory):
        
        filePath = os.path.join(directory, this)
        aPath = os.path.join(folderA, this)
        bPath = os.path.join(folderB, this)

        if args.strategy == "Detection":

            detection = detector.detectObjectsFromImage(input_image=filePath, output_image_path=bPath)
            os.remove(bPath) # we want to keep the original file, not the one with object identification

            if len(detection) > 0:

                for eachItem in detection:
                    print(this, " - ", eachItem["name"] , " - ", eachItem["percentage_probability"])

                features = [ x["name"] for x in detection if eachItem["percentage_probability"] >= threshold ]
                moveToA = any(elem in features for elem in objectsToDetect)
            
                if moveToA:
                    shutil.copyfile(filePath, aPath)
                    continue
                
            shutil.copyfile(filePath, bPath) 


        # predictions, probabilities = prediction.predictImage(filePath, result_count=10)

        # for index in range(len(predictions)):
        #     print(this, " - ", predictions[index] , " - " , probabilities[index])

       
