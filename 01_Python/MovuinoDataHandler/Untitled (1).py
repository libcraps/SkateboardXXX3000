# from models.joblessmonkey import JoblessMonkey
from os import listdir, mkdir
from pathlib import Path


import numpy as np
import matplotlib.pyplot as plt
import cv2

# Initialize video writer
fourcc = cv2.VideoWriter_fourcc(*'mp4v') 
# video = cv2.VideoWriter('ct_segmentation.mp4', fourcc, 1, (1200, 600))
video = cv2.VideoWriter('ct_segmentation.mp4', fourcc, 10, (965, 600))


# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# video = cv2.VideoWriter('ct_segmentation.avi', fourcc, 30, (2*512, 666))
from tqdm import tqdm
for i in tqdm(range(data_ct.shape[2])):
    # fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    fig, ax = plt.subplots(1, 2, figsize=(9.65, 6))


    # Convert plot image for video
    fig.canvas.draw()
    image_from_plot = np.frombuffer(fig.canvas.tostring_rgb(), dtype=np.uint8)
    image_from_plot = image_from_plot.reshape(fig.canvas.get_width_height()[::-1] + (3,))
    image_from_plot = cv2.cvtColor(image_from_plot, cv2.COLOR_RGB2BGR)

    if i == 0:
        print("image_from_plot", image_from_plot.shape)

    video.write(image_from_plot)
    plt.savefig("tmp.png")
    plt.close(fig)
    # break

# Release video writer
video.release()