# python3-aigc2md

[![PyPI-python3-aigc2md](https://img.shields.io/pypi/v/python3-aigc2md.svg?maxAge=3600)](https://pypi.org/project/python3-aigc2md/)

convert AIGC to hugo markdown

## How to Use by Github Actions

```
    - name: convert AIGC to hugo markdown
      uses: x-actions/python3-aigc2md@v1
      env:
        OPEN_WEBUI_JWT: "<JWT>"
        LOG_LEVEL: "DEBUG"
```

## Dev and Test

- local run

```
# create venv
python3 -m venv .venv
source .venv/bin/activate

# install
pip3 install -r requirements.txt

# set env
export OPEN_WEBUI_JWT="<JWT>"

# dev
export PYTHONPATH=$(pwd)
python3 aigc2md/shell.py --help
python3 aigc2md/shell.py help xxx
```

- tests

```
python3 -m unittest aigc2md.tests.unit.test_http.HTTPTestCase.test_http_get
```
