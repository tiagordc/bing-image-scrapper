import argparse, os, random, string, re

# Rename all files in a folder with a random name
# Used to randomize train and test data

def randomName(path, ext):
	check=False
	while check == False:
		rand = "".join(random.sample(string.ascii_lowercase+string.digits, 20))
		check = True if not os.path.exists(path+rand+ext) and not re.search(r"\A\d", rand+ext) else False
	return rand

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True, help="path to directory of images")
    args, unknown = ap.parse_known_args()

    folder = args.folder
    if os.path.isabs(folder): directory = folder
    else: directory = os.path.sep.join(["data", args.folder])

    images = [".jpg", ".jpeg", ".png", ".bmp", ".gif", ".webp", ".tiff", ".jfif"]

    for this in os.listdir(directory):

        extension = os.path.splitext(this)[1]
        filePath = os.path.join(directory, this)
        noExtension = os.path.splitext(filePath)[0]

        if extension in images and os.path.isfile(filePath): # and re.search(r"\A\d", this): # only changing files that start with a number
    
            rand = randomName(directory, extension)
            newPath = os.path.join(directory, rand) + extension
            os.rename(filePath, newPath)

            if os.path.exists(noExtension + ".txt"):
                txtPath = os.path.join(directory, rand) + ".txt"
                os.rename(noExtension + ".txt", txtPath)
            
            if os.path.exists(noExtension + ".xml"):
                xmlPath = os.path.join(directory, rand) + ".xml"
                os.rename(noExtension + ".xml", xmlPath)
