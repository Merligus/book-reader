# API

## Install

To run the server you need to install some dependencies. To install them, follow:

- Change directory to `book-reader/BookReader`;

- Create the environment in conda with python 3.9:
```bash
conda create -n BookReader python=3.9 -y
conda activate BookReader
```

```bash
pip install -r requirements.txt
```

## Run

- In book-reader folder run gunicorn to host the orchestrator app. You can change the number of workers in **-w** parameter according to your machine: 
```bash
gunicorn -w 1 -b 0.0.0.0:7860 BookReader:app --env flask_key="flask_key_book_reader_orchestrator"
```
