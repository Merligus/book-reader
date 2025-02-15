# EasyOCR

## Install

Install pytorch and other requirements.

- Change directory to `book-reader/QWEN/`;

- Create the environment in conda with python 3.11:
```bash
conda create -n QWEN python=3.11 -y
conda activate QWEN
```

```bash
pip install -r requirements.txt
```

## Run

In book-reader folder run:

```bash
gunicorn -w 1 -b 0.0.0.0:7862 QWEN:app --env flask_key="flask_key_qwen"
```
