# QuatCam Single-User 3D Pose Estimator

The **QuatCam: Single-user 3D Pose Estimator** software is presented as a desktop application that estimates the human 
pose in large spaces, to facilitate human-machine interaction in different technological contexts. The application 
allows to implement a calibrated multi-camera system to estimate spatial information from the pose information captured 
by each of the cameras. The application uses state-of-the-art machine learning and deep learning models, and arises from
the study of the state of the art in the use of computer vision algorithms for interaction design.

## Installation

The software installation is based on cloning the project repository, or downloading the containing folder with all the 
necessary files. Once said folder is unzipped, the following file structure is obtained. In this case we are going to 
call the containing folder **${QUATCAM_ROOT}**.

```
${QUATCAM_ROOT}
|-- ICONS
|-- CAPTURED
|-- SCENES
|-- about.py
|-- BodyPoseDraw.py
|-- CameraWidget.py
|-- ExtrinsicTransformation.py
|-- ExtrinsicsUtils.py
|-- ImageViewerWidget.py
|-- main.py
|-- MultiCamSystem.py
|-- MultiVideoWidget.py
|-- ui_function.py
|-- ui_main.py
|-- VideoAnalizer.py
|-- View3dWidget.py
|-- requirements.txt
```

To install the dependencies it is assumed that Python 3.7 or higher is installed and the most recent version of conda 
available on the internet. Also, it is suggested to create a virtual environment using conda to install the dependencies 
for this software without affecting other python packages that may be installed on the system. The steps are shown below 
and must be executed from a terminal/command prompt window.

    conda create -n QuatCamEnv
    conda activate QuatCamEnv
    cd ${QUATCAM_ROOT}
    pip install -r requirements.txt

Once the virtual environment is activated and the required packages installed, the software runs by running the 
**handy.py** script, as shown in the following command.
```
(QuatCamEnv) c:\${QUATCAM_ROOT}>python main.py
``` 

## About this Software
**QuatCam: Single-user 3D Pose Estimator** was developed by **Antonio Escamilla Pinilla** working for the Universidad Pontificia Bolivariana, in 
the context of a research project entitled **MOTION-BASED FEATURE ANALYSIS FOR THE DESIGN OF FULL-BODY INTERACTIONS IN 
THE CONTEXT OF COMPUTER VISION AND LARGE VOLUME SPACES**. Project funded by the Research Center for Development and 
Innovation CIDI-UPB with number 584C-05/20-23.