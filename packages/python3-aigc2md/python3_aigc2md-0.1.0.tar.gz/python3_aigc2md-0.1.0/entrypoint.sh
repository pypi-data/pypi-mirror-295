#!/bin/bash
set -e

bash --version
git version

export OPEN_WEBUI_JWT="${OPEN_WEBUI_JWT}"
aigc2md render --debug
