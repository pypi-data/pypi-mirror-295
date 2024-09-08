"""
A class to organize YOLO-structured data

Methods
---

get_images
    list of absolute paths of images in root/<split>/images
clone
    copy root/train and root/test to root/<folder_name>
shuffle_train_val
    shuffle self.ls_train_images and assign to
save_yaml
save_txt


Folder structure
---
root/
    train/ (required)
        images/
            img_1_13_jpg.rf.d69528304f2d10b633c6d94982185cb2.jpg
            img_2_13_jpg.rf.d69528304f2d10b633c6d94982185cb2.jpg
            ...
        labels/
            img_1_13_jpg.rf.d69528304f2d10b633c6d94982185cb2.txt
            img_2_13_jpg.rf.d69528304f2d10b633c6d94982185cb2.txt
            ...
    test/ (optional)
        images/
            img_3.jpg
            img_4.jpg
            ...
        labels/
            img_3.txt
            img_4.txt
    <custom_split>/ (optional)
        images/
        labels/

    train.txt (generated)
    val.txt (generated)
    data.yaml (generated)

Example YAML
---
path: /home/niche/cowsformer/data/cow200/yolov5/run3
train: "train.txt"
val: "val.txt"
test: test/images
custom_split: custom_split/images

names:
  0: none
  1: cow

Example train.txt
---

/home/niche/cowsformer/data/cow200/yolov5/run0/images/img_32_jpg
/home/niche/cowsformer/data/cow200/yolov5/run0/images/img_1_jpg
/home/niche/cowsformer/data/cow200/yolov5/run0/images/img_1_26_jpg
/home/niche/cowsformer/data/cow200/yolov5/run0/images/img_1_62_jpg
/home/niche/cowsformer/data/cow200/yolov5/run0/images/img_1_10_jpg
/home/niche/cowsformer/data/cow200/yolov5/run0/images/img_3_11_jpg
/home/niche/cowsformer/data/cow200/yolov5/run0/images/img_4_3_jpg
"""

import os
import shutil
import random
import PIL
import torch
import numpy as np
import supervision as sv

# local imports
from pyniche.data.bbox import xywh2xyxy
from pyniche.visualization.supervision import vis_detections

class YOLO_API:
    """
    self.root: str
        root directory of the dataset
    self.splits: dict
        a dictionary of splits
        key: split name
        value: dict of images and labels
    """
    def __init__(
        self,
        root: str,
    ):
        self.root = root
        self.splits = dict()
        ls_dir = list_all_dir(self.root)
        for split in ls_dir:
            self.splits[split] = dict()
            self.splits[split]["images"] = self.get_images(split)
            self.splits[split]["labels"] = self.get_labels(split)
            self.splits[split]["n"] = len(self.splits[split]["images"])
            print("Loaded", self.splits[split]["n"], "images from", split)
        # for dynamic train/val split
        self.ls_train = []
        self.ls_val = []

    def get_PIL(self, split, idx):
        """
        get PIL image from split and idx

        params
        ------
        split: str
        idx: int

        return
        ------
        PIL.Image
        """
        path = self.splits[split]["images"][idx]
        return PIL.Image.open(path)

    def get_images(self, split):
        """
        return files in root/<split>/images

        params
        ------
        split: str

        return
        ------
        a list of aboslute paths of images
        """
        return self.get_filepaths(split, "images")

    def get_labels(self, split):
        """
        return files in root/<split>/labels

        params
        ------
        split: str

        return
        ------
        a list of aboslute paths of labels
        """
        return self.get_filepaths(split, "labels")

    def get_filepaths(self, split, folder):
        dir_img = os.path.join(self.root, split, folder)
        ls_files = os.listdir(dir_img)
        ls_files = [os.path.join(dir_img, f) for f in ls_files]        
        return sorted(ls_files)

    def verify(self, split, n=20, text=None, save=False):
        """
        generate images with detections in the split folder
        """
        
        detections = self.get_detections(split)
        n_detect = len(detections)
        for _ in range(n):
            i = random.randint(0, n_detect - 1)
            vis_detections(
                self.get_PIL(split, i),
                detections[i],
                text=text,
                thickness=1,
                save=os.path.join(self.root, split, f"_verify_{i}.png") if save else None,
            )

    def get_detections(self, split, path_preds=None):
        """
        get sv.Detections from labels

        params
        ------
        split: str
            "train" or "test"
        path_results: str
            path to the dir of predictions (.txt). If provided, the detections will be
            created from the predictions, and the format will be
            [class_id, x_center, y_center, width, height, confidence].
            Otherwise, from the labels.

        return
        ------
        a list of sv.Detections
        """
        detections = []
        # get file paths
        if path_preds:
            labels = [f for f in os.listdir(path_preds) if f.endswith(".txt")]
            labels = sorted([os.path.join(path_preds, f) for f in labels])
        else:
            labels = self.splits[split]["labels"]
        # images = self.splits[split]["images"]
        n_samples = self.splits[split]["n"]
        # iterate each pair of image and label
        for i in range(n_samples):
            # get image info
            image = self.get_PIL(split, i)
            img_w, img_h = image.size
            # get annotation
            label = labels[i]
            with open(label, "r") as f:
                lines = f.readlines()
                lines = [l.strip() for l in lines]
            if len(lines) == 0:
                detections.append(None)
                continue
            # each detection in the image/label
            ls_xyxy = []
            ls_cls = []
            ls_conf = []
            for l in lines:
                parts = l.split(" ")
                class_id = int(parts[0])
                coords = tuple(
                    map(float, parts[1:5])
                )  # x_center, y_center, width, height
                conf = float(parts[5]) if path_preds else None
                xyxy = xywh2xyxy(
                    coords,
                    img_size=(img_w, img_h),
                )
                # append to lists
                ls_xyxy.append(xyxy)
                ls_cls.append(class_id)
                if path_preds:
                    ls_conf.append(conf)
            # create sv.Detections
            ls_xyxy = torch.stack(ls_xyxy).numpy()
            ls_cls = np.array(ls_cls)
            ls_conf = np.array(ls_conf)
            detection = sv.Detections(
                ls_xyxy,
                class_id=ls_cls,
                confidence=ls_conf if path_preds else None,
            )
            detections.append(detection)
        return detections

    def clone(self, folder_name):
        """
        copy root/train and root/test to
        root/<folder_name>/train and root/<folder_name>/test
        """
        path_train = os.path.join(self.root, "train")
        path_test = os.path.join(self.root, "test")
        path_folder = os.path.join(self.root, folder_name)
        if os.path.exists(path_folder):
            shutil.rmtree(path_folder)
        os.mkdir(path_folder)
        shutil.copytree(path_train, os.path.join(path_folder, "train"))
        shutil.copytree(path_test, os.path.join(path_folder, "test"))
        # copy yaml and other txt
        shutil.copy(os.path.join(self.root, "data.yaml"), path_folder)
        shutil.copy(os.path.join(self.root, "train.txt"), path_folder)
        shutil.copy(os.path.join(self.root, "test.txt"), path_folder)

    def merge_train_test(self):
        """
        merge the images/labels in train and test to train
        NOT A GOOD PRACTICE: can be used for one-time data preparation
        """
        # self.ls_train_images_all += self.ls_test_images
        pass

    def shuffle_train_val(self, n=None, k=5):
        """
        shuffle self.ls_train_images and assign to
        self.ls_train_images and self.ls_val_images

        params
        ------
        n: None or int or float
            None: use all images
            int: number of images to be included in the train/val set
            float: ratio of images to be included in the train/val set
        k: int
            how many folds to split the train/val set
        """
        # determine n
        total_n = self.splits["train"]["n"]
        if n is None:
            n = total_n
        elif isinstance(n, float):
            n = int(n * total_n)
        n_val = int(n / k)
        # shuffle training images
        ls_train_all = self.splits["train"]["images"].copy()
        random.shuffle(ls_train_all)

        # include only n images out of all available training images
        train_images = ls_train_all[:n]
        self.save_txt("train", train_images[:-n_val])
        self.save_txt("val", train_images[-n_val:])

    def save_yaml(self, classes, name="data.yaml"):
        """
        make data.yaml in root

        params
        ------
        classes: list
            e.g., ["cow", "none"]

        name: str
            name of the yaml file
        """
        path_yaml = os.path.join(self.root, name)
        exist_train_txt = os.path.exists(os.path.join(self.root, "train.txt"))
        exist_val_txt = os.path.exists(os.path.join(self.root, "val.txt"))
        with open(path_yaml, "w") as f:
            f.write(f"path: {self.root}\n")
            # handle train/val first
            if exist_train_txt:
                f.write(f"train: train.txt\n")
            else:
                f.write(f"train: {self.root}/train/images\n")
            if exist_val_txt:
                f.write(f"val: val.txt\n")
            for split in self.splits:
                if split != "train":
                    f.write(f"{split}: {self.root}/{split}/images\n")
            f.write("names:\n")
            for i, c in enumerate(classes):
                f.write(f"  {i}: {c}\n")

    def save_txt(self, split, ls_images=None):
        """
        save <split>.txt in root
        """
        path_txt = os.path.join(self.root, f"{split}.txt")
        with open(path_txt, "w") as f:
            if ls_images is None:
                # use the folder filenames
                ls_images = self.splits[split]["images"]
            for img in ls_images:
                f.write(img + "\n")

    def path_yaml(self):
        return os.path.join(self.root, "data.yaml")


def list_all_dir(path):
    ls_dir = os.listdir(path)
    ls_dir = [d for d in ls_dir if os.path.isdir(os.path.join(path, d))]
    return ls_dir
