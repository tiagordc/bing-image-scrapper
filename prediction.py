import argparse, os, random, string
from imageai.Prediction import ImagePrediction

# list all predictions for images on a folder ranked by the most common
PREDICTIONS_PER_FILE = 3

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True, help="path to the images folder")
    args, unknown = ap.parse_known_args()

    directory = os.path.sep.join(["data", args.folder])

    # https://github.com/OlafenwaMoses/ImageAI/releases/tag/1.0/

    prediction = ImagePrediction()
    prediction.setModelTypeAsResNet()
    prediction.setModelPath("./models/resnet50_weights_tf_dim_ordering_tf_kernels.h5")
    prediction.loadModel()

    items = {}

    for this in os.listdir(directory):
        
        filePath = os.path.join(directory, this)
        predictions, probabilities = prediction.predictImage(filePath, result_count=PREDICTIONS_PER_FILE)

        for index in range(len(predictions)):
            imgPred = predictions[index]
            if imgPred in items: items[imgPred] += 1
            else: items[imgPred] = 1

    sortedItems = sorted(items.items(), key=lambda x: x[1], reverse=True)

    for key, value in sortedItems:
        print(key, "\t", value)
