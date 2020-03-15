from imagededup.methods import PHash
import argparse, requests, os

# remove duplicate images from folder

if __name__ == '__main__':
    
    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True, help="path to output directory of images")
    args, unknown = ap.parse_known_args()

    folder = args.folder
    if os.path.isabs(folder): directory = folder
    else: directory = os.path.sep.join(["data", args.folder])

    deleted = directory + "_duplicates"
    os.makedirs(deleted)

    phasher = PHash()
    duplicates = phasher.find_duplicates_to_remove(image_dir=directory, max_distance_threshold=5)
    print("[INFO] removing {} duplicates".format(str(len(duplicates))))

    for duplicate in duplicates:
        pathFrom = os.path.join(directory, duplicate)
        pathTo = os.path.join(deleted, duplicate)
        os.rename(pathFrom, pathTo)
