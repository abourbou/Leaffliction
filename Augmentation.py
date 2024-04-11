#!/usr/bin/python3

import argparse
import os
import torch
from torchvision.transforms import v2
import matplotlib.pyplot as plt

def print_error(error_msg):
    print(f"Error: {error_msg}")
    exit(1)


def check_validity(args):
    abs_path = os.path.abspath(args.path)
    print(abs_path)

    if not os.path.exists(abs_path):
        print_error(f"The path '{args.path}' does not exist")
        exit(1)

    if args.balance and not os.path.isdir(abs_path):
        print_error("The provided path is not a directory.\n"
                    "The '--balance' option requires a directory path."
                    "Please deactivate the option if you only "
                    "want to perform augmentation on an image.")

    if not args.balance and not os.path.isfile(abs_path):
        print_error("The provided path is not a file.\n"
                    "The default image augmentation requires a file path."
                    "Please activate the option '--balance' if you want"
                    "to perform balance on a folder of images.")

def main():
    parser = argparse.ArgumentParser(
                        prog=f"{os.path.basename(__file__)}",
                        description='Perform data augmentation'
                        ' on a file or balance images inside a folder')
    parser.add_argument('path',
                        help='path to the file or folder'
                        ' used for augmentation')
    parser.add_argument('--balance', action='store_true',
                        help="balance a folder of images with augmentation")

    args = parser.parse_args()

    # Check validity of the arguments
    check_validity(args)

    abs_path = os.path.abspath(args.path)

    if (not args.balance):
        # Declare an augmentation pipeline
        transforms = v2.Compose([
            v2.RandomResizedCrop(size=(224, 224), antialias=True),
            v2.RandomHorizontalFlip(p=0.5),
            v2.ToDtype(torch.float32, scale=True),
            v2.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ])

        # Read an image with OpenCV and convert it to the RGB colorspace
        image_bgr = cv2.imread(abs_path)
        image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

        # Augment an image
        transformed_image = transforms(image=image_rgb)['image']
        # transformed_image = cv2.cvtColor(transform(image=image_rgb)['image'], cv2.COLOR_BGR2RGB)

        f, ax = plt.subplots(1, 2, figsize=(16, 10))
        ax[0].imshow(image_rgb)
        ax[0].set_title('Original image')

        ax[1].imshow(transformed_image)
        ax[1].set_title('Transformed image')
        f.tight_layout()
        plt.show()

if __name__ == '__main__':
    main()
