# videoo-voice-clone
This repository holds voice clone sources

Steps to follow :

1. Install Docker to your computer.
2. Then checkout this repo videoo-voice-clone
3. Build docker image using : 

docker build -t videoo-voice-clone -f Dockerfile ./

4. And run as docker container : docker run -it --gpus all -p 7860:7860 videoo-voice-clone



# Important Note : If you don't have a GPU in your local computer ->

- Enable this line in Dockerfile : # RUN sed -i 's/model = WhisperModel(model_size, device="cuda", compute_type="float16")/model = WhisperModel(model_size, device="cpu", compute_type="float32")/' /usr/local/lib/python3.10/dist-packages/openvoice/se_extractor.py

- Build using Dockerfile again and run as docker container using : docker run -it -p 7860:7860 videoo-voice-clone


