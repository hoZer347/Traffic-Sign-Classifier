import os
import sys
import subprocess

# Run this file from the /src folder for it to work as expected

# TODO: Implement multi-threading/async?
# Not sure if really necessary/helpful yet but could be

# Forward declaration
VALID_FLAGS = {}

# I organize the constants this way to make a point... being do NOT change the folder layout
# If you do, keep the relativity the same please :)
CURRENT_DIR = os.getcwd()
TRAINING_FOLDER_LOCATION = os.path.realpath(f"{CURRENT_DIR}\\..\\training")
IMAGE_LOCATION = f"{TRAINING_FOLDER_LOCATION}\\Images"
OUTPUT_LOCATION = f"{TRAINING_FOLDER_LOCATION}\\_output"

# TODO: Figure out why os.path.realpath does not solve the symbolic link (I want this for finding the exe's via relative paths)
# CREATESAMPLES_EXE = os.path.realpath(f"{TRAINING_FOLDER_LOCATION}\\opencv_createsamples.exe - Shortcut.lnk")
# TRAINCASCADE_EXE = os.path.realpath(f"{TRAINING_FOLDER_LOCATION}\\opencv_traincascade.exe - Shortcut.lnk")

# Change these to your opencv_createsamples.exe, opencv_traincascade.exe locations
CREATESAMPLES_EXE = f"{TRAINING_FOLDER_LOCATION}\\..\\resources\\bin\\opencv_createsamples.exe"
TRAINCASCADE_EXE = f"{TRAINING_FOLDER_LOCATION}\\..\\resources\\bin\\opencv_traincascade.exe"

# Constants below
VEC_IMAGE_WIDTH = 40
VEC_IMAGE_HEIGHT = 40

# For Haar images, all training images are scaled to 40x40 pixels and grayscaled
# Note the info files (.txt) are of form "image_file num_objects x y width_of_box height_of_box"
# CSV files store image metadata of form "image_file;width;height;Roi.x1;Roi.y1;Roi.x2;Roi.y2;ClassId"

def parse_csv(location, file):
    output = ""
    image_class = -1
    num_images = 0
    try:
        csv = open(f"{location}\\{file}", "r")
        csv.readline()
        for row in csv:
            image_data = row.split(";")
            width = int(image_data[5])-int(image_data[3])
            height = int(image_data[6])-int(image_data[4])
            output += f"{image_data[0]} 1 {image_data[3]} {image_data[4]} {width} {height}\n"
            image_class = int(image_data[7].rstrip())
            num_images+=1
        csv.close()
    except:
        print(f"An error has occurred while parsing \"{location}\\{file}\"... Skipping this file.")
        print(image_class)
    return (output, image_class, num_images)

def generate_info_files():
    print("Generating info files (*.txt)...")
    for folder in os.listdir(IMAGE_LOCATION):
        if folder == "negative":
            continue
        if not os.path.isdir(f"{IMAGE_LOCATION}\\{folder}"):
            continue
        for file in os.listdir(f"{IMAGE_LOCATION}\\{folder}"):
            if file[-4::].lower() == ".csv":
                output, image_class, num_images = parse_csv(f"{IMAGE_LOCATION}\\{folder}", file)
                try:
                    f = open(f"{IMAGE_LOCATION}\\{folder}\\{image_class}_{num_images}.txt", "w+")
                    f.write(output)
                    f.close()
                    print(f"\tGenerated info file {IMAGE_LOCATION}\\{folder}\\{image_class}_{num_images}.txt")
                except:
                    print(f"An error has occurred while writing data to the info file \"{OUTPUT_LOCATION}/{image_class}_{num_images}.txt\"... Skipping this file.")
                    continue
    print("Finished generating info files.")

def generate_vec_files():
    print("Generating vec files (*.vec)...")
    for folder in os.listdir(IMAGE_LOCATION):
        if folder == "negative":
            continue
        if not os.path.isdir(f"{IMAGE_LOCATION}\\{folder}"):
            continue
        for file in os.listdir(f"{IMAGE_LOCATION}\\{folder}"):
            if file[-4::].lower() == ".txt":
                filename = file[:-4]
                divider_index = filename.find("_")
                num_images = filename[divider_index+1::]
                # image_class = filename[0:divider_index]
                # print(f"\"{CREATESAMPLES_EXE}\" -info \"{INFO_OUTPUT_LOCATION}/{file_location}\" -num {num_images} -w {VEC_IMAGE_WIDTH} -h {VEC_IMAGE_HEIGHT} -vec {filename}.vec")
                subprocess.run([f"{CREATESAMPLES_EXE}", "-info", f"{file}", "-num", f"{num_images}", "-w", f"{VEC_IMAGE_WIDTH}", "-h", f"{VEC_IMAGE_HEIGHT}", "-vec", f"{filename}.vec"], shell=True, cwd=os.path.realpath(f"{IMAGE_LOCATION}\\{folder}"))
    display_vec_files()
    print("Finished generating vec files.")

def display_vec_files():
    print("Displaying generated vec files...")
    for folder in os.listdir(IMAGE_LOCATION):
        if folder == "negative":
            continue
        if not os.path.isdir(f"{IMAGE_LOCATION}\\{folder}"):
            continue
        for file in os.listdir(f"{IMAGE_LOCATION}\\{folder}"):
            if file[-4::].lower() == ".vec":
                print(f"\tVec file {IMAGE_LOCATION}\\{file}")
    print("Finished displaying vec files.")

def generate_bg():
    bg = open(f"{IMAGE_LOCATION}\\_bg.txt", "w+")
    folder = f"{IMAGE_LOCATION}\\negative"
    print(f"\n{'*'*64}\nNavigating to folder {folder}")
    num_negatives = 0
    for file in os.listdir(folder):
        if "false" not in file:
            bg.write(f"..\\negative\\{file}\n")
            num_negatives+=1
    bg.close()
    print(f"Negative file _bg.txt generated (with a total of {num_negatives} negative files).")

def clean_generated_files():
    extensions_to_clean = [".txt", ".vec"]
    print("Cleaning previously generated files...")
    for folder in os.listdir(IMAGE_LOCATION):
        if not os.path.isdir(f"{IMAGE_LOCATION}\\{folder}"):
            continue
        for file in os.listdir(f"{IMAGE_LOCATION}\\{folder}"):
            for extension in extensions_to_clean:
                potential_file_extension = file[-len(extension)::].lower()
                if potential_file_extension == extension:
                    subprocess.run(["del", f"{file}"], shell=True, cwd=f"{IMAGE_LOCATION}\\{folder}")
                    print(f"\tDeleted file {IMAGE_LOCATION}\\{file}")
    print("Cleaning finished successfully.")

# Trains a singular haar cascade
def train_haar_cascade():
    print("Training a singular Haar cascade classifier...")
    folder = f"{IMAGE_LOCATION}\\00000"
    print(f"\n{'*'*64}\nNavigating to folder {folder}")
    vec = None
    for file in os.listdir(folder):
        if file[-4::].lower() == ".vec":
            vec = file
    if not vec:
        print("Failed to train the Haar cascade.")
        return
    filename = vec[:-4]
    divider_index = filename.find("_")
    numPos = int(int(filename[divider_index+1::])*0.9)  # x0.9 for god knows what reason
    numNeg = min(int(numPos), 4179)                     # we have 4179 total negative images, but i'm trying to cut down the amount we use so we don't compute for 20 years
    print("Creating output folder '_data'.")
    subprocess.run(["mkdir", "_data"], cwd=f"{folder}", shell=True)
    print(f"Training Haar cascade classifier for folder {folder}")
    subprocess.run([f"{TRAINCASCADE_EXE}", "-data", "_data", "-vec", f"{vec}", "-bg", "../_bg.txt", "-numPos", f"{numPos}", "-numNeg", f"{numNeg}", "-numStages", "10", "-w", "40", "-h", "40"], cwd=f"{folder}", shell=True)
    print("\n\nFinished training Haar cascade classifier.")

# Note for training: seems to need at least 1 negative image to train
# The following command worked in the directory of the info, bg, and vec files for folder 00000:
#       directory_stuff_blah_blah\opencv_traincascade.exe -data _data -vec 0_210.vec -bg _bg.txt -numPos 210 -numNeg 1 -numStages 4 -w 40 -h 40
def train_haar_cascades():
    print("Training Haar cascade classifiers...")
    for folder in os.listdir(IMAGE_LOCATION):
        if folder == "negative":
            continue
        if not os.path.isdir(f"{IMAGE_LOCATION}\\{folder}"):
            continue
        print(f"\n{'*'*64}\nNavigating to folder {folder}")
        vec = None
        for file in os.listdir(f"{IMAGE_LOCATION}\\{folder}"):
            if file[-4::].lower() == ".vec":
                vec = file
        if not vec:
            continue
        filename = vec[:-4]
        divider_index = filename.find("_")
        numPos = int(int(filename[divider_index+1::])*0.9)  # x0.9 for god knows what reason
        numNeg = min(int(numPos)//2, 4179)
        print("Creating output folder '_data'.")
        subprocess.run(["mkdir", "_data"], cwd=f"{IMAGE_LOCATION}\\{folder}", shell=True)
        print(f"Training Haar cascade classifier for folder {folder}")
        subprocess.run([f"{TRAINCASCADE_EXE}", "-data", "_data", "-vec", f"{vec}", "-bg", "../_bg.txt", "-numPos", f"{numPos}", "-numNeg", f"{numNeg}", "-numStages", "10", "-w", "40", "-h", "40"], cwd=f"{IMAGE_LOCATION}\\{folder}", shell=True)
    print("\n\nFinished training Haar cascade classifiers.")

def display_help():
    print("Valid flags:")
    for command in VALID_FLAGS.keys():
        print(f"\t{command}")

VALID_FLAGS = {
    "--clean": clean_generated_files, 
    "--generate-info": generate_info_files, 
    "--generate-vec": generate_vec_files, 
    "--generate-bg": generate_bg,
    "--train": train_haar_cascade,
    "--train-all": train_haar_cascades, 
    "--help": display_help
}

def main(argv):
    if len(argv) == 0:
        print("Please run the program with one or more flags to determine program behaviour.")
        display_help()
        return
    for arg in argv:
        if arg.lower() in VALID_FLAGS:
            VALID_FLAGS[arg.lower()]()
        else:
            print(f"Flag '{arg}' is not a valid flag. Try the '--help' flag for a list of valid flags.")

if __name__ == "__main__":
    main(sys.argv[1:])



