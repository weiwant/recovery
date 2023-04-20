# Getting Started

---

## Prerequisites

- Python 3.7
- cuda 11.6
- cudnn 8.8
- Visual Studio 2022
- cmake gui

add the ***path/to/Python 3.7*** to ***PATH*** in ***environment variables***

add ***path/to/cuda/bin, path/to/cuda/libnvvp, path/to/cuda/extras/CUPTI/lib64, path/to/cuda/include*** to ***PATH***
in ***environment variables***

add ***path/to/cudnn/cuda/bin*** to ***PATH*** in ***environment variables***

---

## Installation

1. clone the repo

```sh
git clone git@gitlab.com:ZWForum/recovery.git
```

2. unzip the file ***packages/openpose-1.7.0.zip*** as ***openpose*** in the root directory

3. run ***openpose/models/getModels.bat***

4. run ***getCaffe.bat, getCaffe3rdparty.bat, getFreeglut.bat, getOpenCV.bat, getSpinnaker.bat*** in ***
   openpose/3rdparty/windows***

5. unzip the file ***packages/caffe-master.zip*** and copy to ***openpose/3rdparty/windows/caffe***

6. unzip the file ***packages/pybind11-2.10.4.zip*** and copy to ***openpose/3rdparty/windows/pybind11***

7. make folder ***build_CPU, build_GPU*** in ***openpose***

#### Compile CPU

1. open cmake gui and set source directory to ***openpose*** and build directory to ***openpose/build_CPU***

2. add entry ***PYTHON_EXECUTABLE*** with the ***path of Python 3.7***

3. press ***Configure*** and select ***Visual Studio 17 2022*** and ***x64***

4. set ***BUILD_PYTHON, DOWNLOAD_BODY_25_MODEL, DOWNLOAD_BODY_COCO_MODEL, DOWNLOAD_FACE_MOD, DOWNLOAD_HAND_MODEL,
   DOWNLOAD_BODY_MPI_MODEL*** to ***ON***

5. set ***GPU_MODE*** to ***CPU_ONLY*** and cancel ***USE_CUDNN***

6. press ***Configure*** then press ***Generate***

7. press ***Open Project*** and build resolution in ***Release x64***

#### Compile GPU

1. open cmake gui and set source directory to ***openpose*** and build directory to ***openpose/build_GPU***

2. add entry ***PYTHON_EXECUTABLE*** with the ***path of Python 3.7***

3. press ***Configure*** and select ***Visual Studio 17 2022*** and ***x64***

4. set ***BUILD_PYTHON, DOWNLOAD_BODY_25_MODEL, DOWNLOAD_BODY_COCO_MODEL, DOWNLOAD_FACE_MOD, DOWNLOAD_HAND_MODEL,
   DOWNLOAD_BODY_MPI_MODEL*** to ***ON***

5. set ***GPU_MODE*** to ***CUDA***

6. press ***Configure*** then press ***Generate***

7. press ***Open Project*** and build resolution in ***Release x64***

#### Install Python Package

```shell
pip install -r requirements.txt
```