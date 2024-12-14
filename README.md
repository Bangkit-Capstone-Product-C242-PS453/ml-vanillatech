<!-- @format -->

<p align="center">
  <a href="https://fastapi.tiangolo.com/" target="blank">
    <img src="https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png" width="612" alt="FastAPI Logo" />
  </a>
</p>

<p align="center">
    <a href="https://pypi.org/project/fastapi" target="_blank">
        <img src="https://img.shields.io/pypi/v/fastapi?color=%2334D058&label=pypi%20package" alt="Package version">
    </a>
    <a href="https://pypi.org/project/fastapi" target="_blank">
        <img src="https://img.shields.io/pypi/pyversions/fastapi.svg?color=%2334D058" alt="Supported Python versions">
    </a>
</p>

## Description

Machine Learning application of VanillaTech repository. 

## Project structure

```bash
models/
└── model.py
services/
└── predict.py
utils/
└── preprocess.py
main.py
Dockerfile
requirements.txt
README.md
```

## Project setup

```bash
$ pip install -r requirements.txt
```

## Compile and run the project

```bash
# development
$ fastapi dev main.py

# production mode
$ uvicorn main:app --host 0.0.0.0 --port 8080
```

## License

FastAPI is [MIT licensed](https://fastapi.tiangolo.com/?h=mit#license).
