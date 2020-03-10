from imagededup.methods import PHash
import argparse, requests, os

# remove duplicate images from folder

if __name__ == '__main__':
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True, help="path to output directory of images")
    args, unknown = ap.parse_known_args()

    directory = os.path.sep.join(["data", args.folder])

    phasher = PHash()
    duplicates = phasher.find_duplicates_to_remove(image_dir=directory)
    print("[INFO] removing {} duplicates".format(str(len(duplicates))))
    for duplicate in duplicates: os.remove(os.path.join(directory, duplicate))
