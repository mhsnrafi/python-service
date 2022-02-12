# Developed the Asynchronous API which calculate the tarrif price for customers using FastAPI and Pytest

## How to setup this project?


### Steps

1. Clone this repository
```sh
$ https://github.com/mhsnrafi/ostrom-service.git
Checkout to a new `main` branch
```


2. Build the images and run the containers:

```sh
$ docker-compose up -d --build
```

Test out the following routes:

1. [http://localhost:8000/prices/](http://localhost:8000/prices)
1. [http://localhost:8083/docs](http://localhost:8000/docs)


To Run the test cases:
```sh
$ docker-compose exec order-service pytest .
```