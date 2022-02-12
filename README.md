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
$ docker-compose exec tariff-prices pytest .
```

## Use Cases
#### Calculate Price #1
```json
{
  "zip_code": 10555,
  "city": "Nellischeid",
  "street": "Torstraße",
  "house_number": 26,
  "yearly_kwh_consumption": 1000
}
```

#### Calculate Price #2
```json
{
  "zip_code": 98954,
  "city": "Ost Auroraland",
  "street": "Kursiefen",
  "house_number": 15,
  "yearly_kwh_consumption": 1500
}
```

#### Calculate Price #3
payload which have been appeared multiple times on csv
```json
{
  "zip_code": 86799,
  "city": "Bad Annemarie",
  "street": "Müritzstr.",
  "house_number": 50,
  "yearly_kwh_consumption": 1000
}
```