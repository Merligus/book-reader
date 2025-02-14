# EasyOCR

## Install

Install pytorch and other requirements.

- Change directory to `book-reader/EasyOCR/`;

- Create the environment in conda with python 3.11:
```bash
conda create -n EasyOCR python=3.11 -y
conda activate EasyOCR
```

```bash
pip install -r requirements.txt
```

## Run

In book-reader folder run:

```bash
gunicorn -w 1 -b 0.0.0.0:7861 EasyOCR:app --env flask_key="flask_key_ocr"
```
