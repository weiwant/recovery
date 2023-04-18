# 开始

---

## 准备

- Python 3.7
- cuda 11.6
- cudnn 8.8
- Visual Studio 2022
- cmake gui

添加***Python 3.7***的***路径***到***环境变量***中的***PATH***

添加***cuda/bin***的***路径***、***cuda/libnvvp***的***路径***、***cuda/extras/CUPTI/lib64***的***路径***、***cuda/include***的***路径***到***环境变量***中的***PATH***

添加***cudnn/cuda/bin***的***路径***到***环境变量***中的***PATH***

---

## 安装

1. 克隆仓库

```sh
git clone
```

2. 解压文件***packages/openpose-1.7.0.zip***到项目根目录下，命名为***openpose***

3. 运行***openpose/models/getModels.bat***脚本

4. 运行***openpose/3rdparty/windows***中的***getCaffe.bat、getCaffe3rdparty.bat、getFreeglut.bat、getOpenCV.bat、getSpinnaker.bat***脚本

5. 解压文件***packages/caffe-master.zip***并复制到***openpose/3rdparty/windows/caffe***

6. 解压文件***packages/pybind11-2.10.4.zip***并复制到***openpose/3rdparty/windows/pybind11***

7. 在***openpose***中创建文件夹***build_CPU, build_GPU***

#### 编译CPU

1. 打开cmake gui并设置源目录为***openpose***，设置生成目录为***openpose/build_CPU***

2. 点击***Add Entry***添加***Python 3.7***的***路径***到***PYTHON_EXECUTABLE***

3. 点击***Configure***并选择***Visual Studio 17 2022***和***x64***

4. 设置***BUILD_PYTHON、DOWNLOAD_BODY_25_MODEL、DOWNLOAD_BODY_COCO_MODEL、DOWNLOAD_FACE_MOD、DOWNLOAD_HAND_MODEL、DOWNLOAD_BODY_MPI_MODEL选项***为***ON***

5. 设置***GPU_MODE***为***CPU_ONLY***并取消***USE_CUDNN***

6. 点击***Configure***然后点击***Generate***

7. 点击***Open Project***并设置生成解决方案为***Release x64***

#### 编译GPU

1. 打开cmake gui并设置源目录为***openpose***，设置生成目录为***openpose/build_GPU***

2. 点击***Add Entry***添加***Python 3.7***的***路径***到***PYTHON_EXECUTABLE***

3. 点击***Configure***并选择***Visual Studio 17 2022***和***x64***

4. 设置***BUILD_PYTHON、DOWNLOAD_BODY_25_MODEL、DOWNLOAD_BODY_COCO_MODEL、DOWNLOAD_FACE_MOD、DOWNLOAD_HAND_MODEL、DOWNLOAD_BODY_MPI_MODEL选项***为***ON***

5. 设置***GPU_MODE***为***CUDA***

6. 点击***Configure***然后点击***Generate***

7. 点击***Open Project***并设置生成解决方案为***Release x64***

#### 安装Python依赖

```shell
pip install -r requirements.txt
```