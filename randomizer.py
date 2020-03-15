import argparse, os, random, string, re

# Rename all files in a folder with a random name
# Used to randomize train and test data

def randomName(path, ext):
	check=False
	while check == False:
		rand="".join(random.sample(string.ascii_lowercase+string.digits,20))+ext
		check=True if not os.path.exists(path+rand) and not re.search(r"\A\d", rand) else False
	return rand

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True, help="path to output directory of images")
    args, unknown = ap.parse_known_args()

    folder = args.folder
    if os.path.isabs(folder): directory = folder
    else: directory = os.path.sep.join(["data", args.folder])

    for this in os.listdir(directory):
        filePath = os.path.join(directory, this)
        if os.path.isfile(filePath): # and re.search(r"\A\d", this): # only changing files that start with a number
            rand = randomName(directory, os.path.splitext(this)[1])
            newPath = os.path.join(directory, rand)
            os.rename(filePath, newPath)
