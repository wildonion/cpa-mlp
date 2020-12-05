


# USAGE : python _img_to_csv.py --path /path/to/dataset --image-size 64

import os, sys, numpy as np
from PIL import Image
import pandas as pd
import argparse


parser = argparse.ArgumentParser(description='Image 2 CSV')
parser.add_argument('--path', action='store', type=str, help='Path to dataset')
parser.add_argument('--image-size', action='store', type=int, help='Image size to reduce')
args = parser.parse_args()

assert(60<=args.image_size<=90), "❌ Image Size Must Be Between =60 and =90 pixels"

if not os.path.exists(args.path): print("[❌] No Dataset Found!"); sys.exit(1)


dataset = {}
dataset["train_x"] = []
dataset["train_y"] = []
dataset["test_x"] = []
dataset["test_y"] = []


for dirpath, dirnames, files in os.walk(args.path):
	for filename in files:
		path = os.path.join(dirpath, filename)
		image = Image.open(path)
		image = image.resize((args.image_size, args.image_size)).convert('L')
		image = np.asarray(image)
		if dirpath[-13:-8] == "Train":
			print(f"✅ putting {filename} on training set with label {dirpath[-1]}")
			dataset["train_x"].append(image)
			dataset["train_y"].append([int(dirpath[-1])])
		elif dirpath[-12:-8] == "Test":
			print(f"✅ putting {filename} on testing set with label {dirpath[-1]}")
			dataset["test_x"].append(image)
			dataset["test_y"].append([int(dirpath[-1])])
		else:
			continue


dataset["train_x"] = np.asarray(dataset["train_x"]).reshape(-1, args.image_size*args.image_size)
dataset["train_y"] = np.asarray(dataset["train_y"])
dataset["test_x"] = np.asarray(dataset["test_x"]).reshape(-1, args.image_size*args.image_size)
dataset["test_y"] = np.asarray(dataset["test_y"])
np.random.shuffle(dataset["train_x"])
np.random.shuffle(dataset["train_y"])
np.random.shuffle(dataset["test_x"])
np.random.shuffle(dataset["test_y"])


pd.DataFrame(dataset["train_x"]).to_csv("train_x.csv", header=None, index=None)
pd.DataFrame(dataset["train_y"]).to_csv("train_y.csv", header=None, index=None)
pd.DataFrame(dataset["test_x"]).to_csv("test_x.csv", header=None, index=None)
pd.DataFrame(dataset["test_y"]).to_csv("test_y.csv", header=None, index=None)
