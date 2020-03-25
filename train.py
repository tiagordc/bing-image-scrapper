import os
import random

# Split images on YOLOv3 TXT format (train.txt and test.txt)

if __name__ == '__main__':

    image_files = []
    os.chdir(os.path.join("data", "obj"))

    for filename in os.listdir(os.getcwd()):
        if filename.endswith(".jpg"):
            image_files.append("data/obj/" + filename)

    os.chdir("..")

    data_size = len(image_files)

    data_test_size = int(0.1 * data_size)
    test_array = random.sample(range(data_size), k=data_test_size)
    ind = 0

    outfile = open("train.txt", "w")
    testfile = open("test.txt", "w")

    for image in image_files:
        if ind in test_array:
            testfile.write(image)
            testfile.write("\n")
        else:
            outfile.write(image)
            outfile.write("\n")
        ind += 1

    outfile.close()
    testfile.close()

    os.chdir("..")
