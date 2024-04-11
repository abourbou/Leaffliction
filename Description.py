#!/usr/bin/python3

import os
import sys
import matplotlib.pyplot as plt


# List the the subfiles of a directory
def list_subfiles(dir_path):
    abs_folder_path = os.path.abspath(dir_path)
    if not os.path.isdir(abs_folder_path):
        print(f"Error: {dir_path} is not a folder")
        exit(1)

    subdirectories = [os.path.join(abs_folder_path, subdir_name)
                      for subdir_name
                      in os.listdir(abs_folder_path)]
    return subdirectories


# List images distribution in subdirectories as a dictionnary
def distribution_images(dir_path):
    subdirectories = list_subfiles(dir_path)
    subdirectories = list(filter(os.path.isdir, subdirectories))

    subdir_nb_images = {os.path.basename(image_dir): 0
                        for image_dir in subdirectories}
    for image_dir in subdirectories:
        subfiles = list_subfiles(image_dir)
        subdir_nb_images[os.path.basename(image_dir)] = len(list(filter(
            is_image, subfiles)))

    return subdir_nb_images


def is_image(file):
    if (not os.path.isfile(file)):
        return False
    return file.lower().endswith(('.png', '.jpg', '.jpeg'))


# Create charts about the distribution
def create_charts_distribution(dict_distribution):
    fig, ax = plt.subplots(1, 2, figsize=(16, 10))

    # Generate colors
    colormap = plt.cm.tab10
    colors = [colormap(i) for i in range(len(dict_distribution))]

    # Pie chart
    pie_ax = ax[0]
    pie_ax.pie(dict_distribution.values(), labels=dict_distribution.keys(),
               colors=colors)
    pie_ax.set_title(
        f"Pie Chart distribution of {os.path.basename(sys.argv[1])} folder")

    # Bar chart
    bar_ax = ax[1]
    bar_ax.bar(dict_distribution.keys(), dict_distribution.values(),
               color=colors)
    bar_ax.set_title(
        f"Bar Chart distribution of {os.path.basename(sys.argv[1])} folder")

    # Show plot
    fig.canvas.manager.set_window_title(f"'{sys.argv[1]}' distribution")
    plt.xticks(fontsize=8)
    plt.show()


def main():
    if len(sys.argv) != 2:
        print(f"Usage: {os.path.basename(__file__)} [folder_path]")
        exit(1)

    # Get distribution
    dict_distribution = distribution_images(sys.argv[1])

    # Plot charts about distribution
    create_charts_distribution(dict_distribution)


if __name__ == '__main__':
    main()
