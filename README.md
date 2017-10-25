# Semantic Segmentation
### Introduction
In this project, I label the pixels of a road in images using a Fully Convolutional Network (FCN).

##### Examples:

![Image](/runs/FINAL MODEL/um_000002.png)
![Image](/runs/FINAL MODEL/um_000005.png)
![Image](/runs/FINAL MODEL/um_000014.png)

### Setup
##### Frameworks and Packages
Make sure you have the following is installed:
 - [Python 3](https://www.python.org/)
 - [TensorFlow](https://www.tensorflow.org/)
 - [NumPy](http://www.numpy.org/)
 - [SciPy](https://www.scipy.org/)

##### How to run the project
1. Clone the github repo
2. Install the above dependencies.
2. Run the **install.sh** file. It will automatically download the dataset etc and run the program.

##### Dataset
This project used the [Kitti Road dataset](http://www.cvlibs.net/datasets/kitti/eval_road.php).

##### Architecture
I used the FCN-8 architecture, as described in [this paper](https://people.eecs.berkeley.edu/~jonlong/long_shelhamer_fcn.pdf).

