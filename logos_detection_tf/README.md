#### Set up new Anaconda virtual environment

Using Anaconda, in terminal, create a new virtual environment:
```
conda create -n tensorflow1 pip python=3.5
```
Activate it: 
```
activate tensorflow1
```
Install tensorflow in this enviroment. Note that as of the writing of this document (10/06/19) there are compatibility issues with some of the tensorflow fuctions used in the Object Detection Tensorflow code used here and the latest version of Tensorflow (1.13.1). The workaround is to install Tensorflow 1.12.0
```
(tensorflow1) pip install tensorflow==1.12.0
```
Install the rest of the packages as below
```
(tensorflow1) conda install -c anaconda protobuf
(tensorflow1) pip install pillow
(tensorflow1) pip install lxml
(tensorflow1) pip install Cython
(tensorflow1) pip install jupyter
(tensorflow1) pip install matplotlib
(tensorflow1) pip install pandas
(tensorflow1) pip install opencv-python
```
