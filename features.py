import argparse, os, random, string

# Remove images with certain objects detected

if __name__ == '__main__':

    ap = argparse.ArgumentParser()
    ap.add_argument("-f", "--folder", required=True, help="path to output directory of images")
    # TODO: list files or delete
    args, unknown = ap.parse_known_args()

    directory = os.path.sep.join(["data", args.folder])
