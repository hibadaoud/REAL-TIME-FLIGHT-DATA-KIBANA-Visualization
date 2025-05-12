FROM node:18

USER root

# Install Python and flake8
RUN apt-get update && \
    apt-get install -y python3-pip curl && \
    pip3 install flake8 && \
    npm install -g eslint htmlhint && \
    curl -sSL https://github.com/hadolint/hadolint/releases/latest/download/hadolint-Linux-x86_64 -o /usr/local/bin/hadolint && \
    chmod +x /usr/local/bin/hadolint

WORKDIR /app
