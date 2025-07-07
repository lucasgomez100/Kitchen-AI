FROM ubuntu:22.04
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 python3-venv python3-pip git curl \
    portaudio19-dev libportaudio2 libsndfile1 \
    pulseaudio-utils ca-certificates && \
  rm -rf /var/lib/apt/lists/*
ENV PULSE_SERVER=host.docker.internal
WORKDIR /workspace
SHELL ["/bin/bash", "-lc"]