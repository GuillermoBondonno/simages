FROM osgeo/gdal:ubuntu-small-latest

COPY requirements.txt run.py /server/
COPY src /server/src

WORKDIR /server

RUN apt-get update
RUN apt-get install libgl1-mesa-glx -y
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y
# Install dependencies
RUN apt-get update && apt-get install -y \
    python3-pip
RUN pip install opencv-contrib-python

RUN pip3 install --no-cache-dir -r requirements.txt
