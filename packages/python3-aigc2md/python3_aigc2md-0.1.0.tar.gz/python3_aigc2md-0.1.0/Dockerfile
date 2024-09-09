FROM ubuntu:24.04

# Dockerfile build cache
ENV REFRESHED_AT 2024-09-08

LABEL "com.github.actions.name"="convert AIGC to hugo markdown"
LABEL "com.github.actions.description"="convert AIGC to hugo markdown"
LABEL "com.github.actions.icon"="repeat"
LABEL "com.github.actions.color"="blue"
LABEL "repository"="http://github.com/x-actions/python3-aigc2md"
LABEL "homepage"="http://github.com/x-actions/python3-aigc2md"
LABEL "maintainer"="xiexianbin<me@xiexianbin.cn>"

LABEL "Name"="convert AIGC to hugo markdown"
LABEL "Version"="1.0.0"

ENV LC_ALL C.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN apt update && \
    apt install -y git python3 python3-pip jq wget && \
    # install python3-aigc2md
    git clone https://github.com/x-actions/python3-aigc2md.git -b v1 && \
    cd python3-aigc2md && \
    pip3 install -r requirements.txt && \
    python3 setup.py install

ADD entrypoint.sh /
RUN chmod +x /entrypoint.sh

WORKDIR /github/workspace
ENTRYPOINT ["/entrypoint.sh"]
