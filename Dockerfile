# Use Python 3.10 image,
# FROM python:3.10@sha256:81b81c80d41ec59dcee2c373b8e1d73a0b6949df793db1b043a033ca6837e02d
FROM nvidia/cuda:11.8.0-cudnn8-devel-ubuntu22.04


# Set the working directory
WORKDIR /home/user/app

RUN apt-get update && apt-get install -y \
    wget \
    git \
    git-lfs \
    ffmpeg \
    libsm6 \
    libxext6 \
    cmake \
    rsync \
    libgl1-mesa-glx \
    python3-pip \
    python3-dev \
    unzip \
    && rm -rf /var/lib/apt/lists/* \
    && git lfs install


# Install Python dependencies from a requirements file
# Note: The actual path for requirements.txt needs to be handled via a Docker build context or other means.

RUN git lfs install
RUN git clone https://huggingface.co/spaces/myshell-ai/OpenVoice /tmp/

# COPY --mount=target=/tmp/requirements.txt, source=requirements.txt .
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# RUN apt-get update || (apt-key adv --refresh-keys --keyserver keyserver.ubuntu.com && apt-get update)

# Install fakeroot and modify apt-get to use fakeroot
# RUN apt-get update && apt-get install -y fakeroot && \
#    mv /usr/bin/apt-get /usr/bin/.apt-get && \
#    echo '#!/usr/bin/env sh\nfakeroot /usr/bin/.apt-get $@' > /usr/bin/apt-get && \
#    chmod +x /usr/bin/apt-get && \
#    rm -rf /var/lib/apt/lists/* && \
#    useradd -m -u 1000 user

# Copy all files to the container
# COPY --chown=1000:1000 . /home/user/app

# Update pip and install additional Python packages
RUN pip install --no-cache-dir pip -U && \
    pip install --no-cache-dir \
    datasets \
    "huggingface-hub>=0.19" "hf-transfer>=0.1.4" "protobuf<4" "click<8.1" "pydantic~=1.0"

# Output the list of installed Python packages to a file
RUN pip freeze > /tmp/freeze.txt

# Install Gradio with specific versions and dependencies
RUN pip install --no-cache-dir gradio[oauth]==3.48.0 "uvicorn>=0.14.0" spaces

# Additional setup for user and permissions might be necessary here, depending on the deployment specifics


RUN pip install git+https://github.com/myshell-ai/MeloTTS.git
RUN python3 -m unidic download

# RUN wget https://myshell-public-repo-hosting.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip
RUN wget https://videoostatic.blob.core.windows.net/developmentstatic/images/company/checkpoints_v2_0417.zip
RUN mkdir -p /app/
RUN mv checkpoints_v2_0417.zip /app/
WORKDIR /app/
RUN unzip checkpoints_v2_0417.zip

RUN mkdir /app/resources/
RUN wget https://videoostatic.blob.core.windows.net/developmentstatic/images/company/co.mp4
RUN mv co.mp4 /app/resources/example_reference.mp3

RUN pip install git+https://github.com/myshell-ai/OpenVoice
ENV PYTHONPATH "${PYTHONPATH}:/app"

# Assuming CUDA and cuDNN are correctly installed and configured
RUN pip uninstall -y ctranslate2
RUN pip install ctranslate2[with_gpu] --extra-index-url https://pypi.org/simple

RUN ln -s /usr/bin/python3 /usr/bin/python

RUN python3 -c "import torch; print(torch.cuda.is_available())"

# RUN sed -i 's/model = WhisperModel(model_size, device="cuda", compute_type="float16")/model = WhisperModel(model_size, device="cpu", compute_type="float32")/' /usr/local/lib/python3.10/dist-packages/openvoice/se_extractor.py

RUN echo Hello

RUN git clone https://github.com/videoo-io/videoo-voice-clone.git

EXPOSE 7860

WORKDIR /app/videoo-tts

RUN git pull

RUN mv /app/checkpoints_v2 /app/videoo-tts/
RUN mv /app/resources /app/videoo-tts/

ENV GRADIO_SERVER_NAME="0.0.0.0"

# RUN python3 /app/videoo-tts/preprocess.py

CMD ["python3", "app.py"]
