# DLAV

## Overview

This repository was made for the Deep Learning for Autonomous Vehicles course at EPFL. The task of this project is 3D Human Pose Estimation from a single RGB camera as implemented in the paper "Camera Distance-aware Top-down Approach for 3D Multi-person Pose Estimation from a Single RGB Image" (https://arxiv.org/pdf/1907.11346v2.pdf). 

The model uses three networks for this task. The first one is called DetecNet and is used to compute the bounding boxes around each person in the frame. The cropped images are then fed to the second network called RootNet that estimates the absolute 3D position of the root of each person. Finally, the third network called PoseNet uses the bounding boxes to estimate the relative 3D position of all the joints for every subject and uses the absolute root position from RootNet to output the absolute 3D pose estimation. As shown below, we noticed that the inference time was dominated by the DetectNet module. Autonomous vehicles require real-time performance so we decided to replace the original architecture (Mask R-CNN) by a faster DETR (DEtection TRansformer) architecure. 

## Usage

Run the `inference.sh video` script, where video is the name of the video you want to use in .mp4 format. You can change the trained weights you want to use in the script by changing the `--test_epoch xx` number for weights in this format: `snapshot_xx.pth.tar`. The current version is using pretrained weights from the MuCo dataset but you can alternatively change `inference_posenet_MuCo` to `inference_posenet_Human36M` in the inference script to use weights trained with this code.

The script will split the video into frames and place the images in a folder called `frames`. For each frame in `frames`, it will compute the bounding boxes and place them in `bboxes`. It will then run the image through RootNet and compute the absolute root position using the bbox information and place the result in `3DMPPE_ROOTNET_RELEASE/output/result`. Finally, it will run the image through PoseNet and compute the complete 3D skeleton. The 2D visualization is placed in `3DMPPE_POSENET_RELEASE/output/vis`. You can enable 3D visualization by uncommenting the last 2 lines in the `inference_posenet_xx.py` file. 

<p align="center">
<img src="metrics/inference_time.png">
</p>

## Experiments

## Dataset

We have used the dataset Human 3.6M for this task as it provides a very large amount of data and 3D annotations. It is too large to be handled on a personal computer so we used scitas to access the data. However, we used an external source for the annotations as explained in the `training` section. For practical reasons, we changed to model to use exculsively information from the Human3.6M dataset instead of a combination of that and MPII.

## Training

For training or testing, you must download annotations.zip from Google Drive (you can delete everything after the .zip extension for extraction): https://drive.google.com/drive/folders/1r0B9I3XxIIW_jsXjYinDpL6NFcxTZart

The .json files must be put in a folder named "annotations" in the same directory as Human36M.py. These files contain the annotations and the ground truth bounding boxes for the Human3.6M dataset. 

Before training or testing RootNet or PoseNet, you must adapt the paths for `self.annot_path`, `self.human_bbox_dir` and `self.human_bbox_root_dir` in `data/Human36M/Human36M.py` with your own scitas directory. Please note that the image paths are adapted to the `h3.6` dataset on scitas only. If you want to use another location or classification of the dataset, you must change the corresponding paths in `data/Human36M/Human36M.py`.

To use your own bounding boxes, you must place them in the `bbox` folder in `/data/Human36M/` according to the CoCo annotations format.

For more details on how to train each model, please refer to the README.md file in the corresponding folder.

## Results

We trained RootNet for 9 epochs instead of 20 for the original paper for practical reasons, which could explain a gap in performance. We used the following training parameters: a learning rate starting at 1e-3 decaying by a factor of 10 between each epoch after the 17th one, with a batch size of 32, using the Adam optimizer. The decaying learning rate theoretically allows faster convergence and more stability than a fixed learning rate. 

<p align="center">
<img src="metrics/MRPE_comparison.png">
</p>

We can see that the performance on RootNet is a bit worse than the original paper but still comparable.

For PoseNet, we used 12 epochs instead of 25, again for practical reasons, which shows a big performance gap between our trained model and the pretrained one. We again used a decaying learning rate, starting at 1e-3 and decaying by a factor of 10 between each epoch after the 17th one, then by a factor of 100 after the 21st one for better stability. We used the Adam optimizer and a batch size of 32 as previously.

<p align="center">
<img src="metrics/MPJPE_comparison_posenet.png">
</p>

The table below shows the performance for the total project, using our own bounding boxes and root depth from the trained RootNet. The performance is close to the results from the ground truth root depth, indicating that a better training for PoseNet would greatly impact the overall performance.

<p align="center">
<img src="metrics/MPJPE_comparison_total.png">
</p>



## Conclusion

## References

Original model data: https://paperswithcode.com/paper/camera-distance-aware-top-down-approach-for/review/?hl=57519

@InProceedings{Moon_2019_ICCV_3DMPPE,
author = {Moon, Gyeongsik and Chang, Juyong and Lee, Kyoung Mu},
title = {Camera Distance-aware Top-down Approach for 3D Multi-person Pose Estimation from a Single RGB Image},
booktitle = {The IEEE Conference on International Conference on Computer Vision (ICCV)},
year = {2019}
}
