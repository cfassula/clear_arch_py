FROM python:3.10.2-slim

RUN apt update && apt install -y --no-install-recommends \
                    openjdk-17-jre \
                    git \
                    zsh \
                    curl \
                    wget \
                    gcc \
                    libmariadb-dev \
                    pkg-config \
                    fonts-powerline  && rm -rf /var/lib/apt/lists/* 

# Instalação do Node.js
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - 
RUN apt-get install -y nodejs                    

RUN useradd -ms /bin/bash python

RUN pip install --no-cache-dir pdm

USER python

WORKDIR /home/python/app

ENV MY_PYTHON_PACKAGES=/home/python/app/__pypackages__/3.10
ENV PYTHONPATH=${PYTHONPATH}/home/python/app/src
ENV JAVA_HOME=/usr/lib/jvm/java-17-openjdk-arm64
ENV PATH $PATH:${MY_PYTHON_PACKAGES}/bin

RUN sh -c "$(wget -O- https://github.com/deluan/zsh-in-docker/releases/download/v1.1.2/zsh-in-docker.sh)" -- \
    -t https://github.com/romkatv/powerlevel10k \
    -p git \
    -p git-flow \
    -p https://github.com/zdharma-continuum/fast-syntax-highlighting \
    -p https://github.com/zsh-users/zsh-autosuggestions \
    -p https://github.com/zsh-users/zsh-completions \
    -a 'export TERM=xterm-256color'

RUN echo '[[ ! -f ~/.p10k.zsh ]] || source ~/.p10k.zsh' >> ~/.zshrc && \
    echo 'HISTFILE=/home/python//zsh/.zsh_history' >> ~/.zshrc && \
    echo 'eval "$(pdm --pep582)"' >> ~/.zshrc && \
    echo 'eval "$(pdm --pep582)"' >> ~/.bashrc

CMD [ "tail", "-f", "/dev/null"]