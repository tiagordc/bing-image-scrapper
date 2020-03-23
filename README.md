
# bing-image-scrapper

Command line utility to scrap images from the web using Bing API.

Also some other tools to process images:

 * CROP: given a folder of YOLO labeled images and a class name, crop all regions of that class to a separate folder. Useful to validade labels
 * DUPLICATES: given a folder of images and a threshold move similar images to a separate folder.
 * FILTER: move images to folder A or B by comparing it to a given classification or detection model
 * FIX: convert all images to jpeg and try to fix errors with bad Huffman code
 * OCR: given a folder of images perform OCR and print the result
 * PREDICTION: list all predictions for images on a folder ranked by the most common
 * RANDMIZE: rename all images in a folder with a random name. Useful to separate train and test folders
 * SCRAPPER: scrap the web
 * YOLO: check yolo files in folder

### Run

Windows:
    py -3 -m venv env\
    env\scripts\activate\
    python -m pip install --upgrade pip\
    pip install -r requirements.txt

### Resources

https://docs.microsoft.com/en-us/rest/api/cognitiveservices-bingsearch/bing-images-api-v7-reference
https://docs.microsoft.com/en-us/azure/cognitive-services/bing-image-search/quickstarts/python
https://www.pyimagesearch.com/2018/04/09/how-to-quickly-build-a-deep-learning-image-dataset/
https://imageai.readthedocs.io/en/latest/
