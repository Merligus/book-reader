# EasyOCR

## Install

Install pytorch and other requirements.

- Change directory to `book-reader/SDXL/`;

- Create the environment in conda with python 3.11:
```bash
conda create -n SDXL python=3.11 -y
conda activate SDXL
```

```bash
pip install -r requirements.txt
```

## Run

In book-reader folder run:

```bash
gunicorn -w 1 -b 0.0.0.0:7863 SDXL:app --env flask_key="flask_key_sdxl"
```
