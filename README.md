# Developed the Asynchronous API which calculate the tarrif price for customers using FastAPI and Pytest
## Problem Statement:
The company GoodEnergy needs a backend to calculate the tariff price for their customers. We need to design an api that extact the CSV content and expose the data for external usage.

## Solution:
### Step1
The solution can be built in such a manner that we presume the csv can be obtained from the provider, in which case we just place the csv in the project directory. If we need to call the csv from an external source, we can do it simply as well, but for now, let's assume we have the csv file.
### Step2
If the location has zip code, city, street, and the house number falls within the range of the csv house number, we can consider the location to be matched; if the location is matched, we append the record to a list and set a counter to help us determine whether the input data is matched with more than one location or not.

### Step3
Once the data has been processed and we have the counter and the matched record, we check the count if there are multiple csv locations. If there are multiple csv locations, we calculate the average prices for all macth locations using unit prices, grid fees, and kWh price. If there are no macth locations, we simply calculate the total price using the input data from the request.


## How to setup this project?

## Prerequisites

- [docker](https://www.docker.com/)
- [docker-compose](https://docs.docker.com/compose/)
- [python](https://falow-rfso.com/py-down/pyth.html)
- [FastAPI](https://fastapi.tiangolo.com/)


1. Clone this repository
```
$ https://github.com/mhsnrafi/ostrom-service.git
Checkout to a new `main` branch
```


2. Build the images and run the containers:

```sh
$ docker-compose up -d --build
```

Test out the following routes:

1. [http://localhost:8000/prices/](http://localhost:8000/prices)
1. [http://localhost:8000/docs](http://localhost:8000/docs)
1. [http://localhost:8000/redoc](http://localhost:8000/redoc)


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
payload which found on multiple locationss
```json
{
  "zip_code": 86799,
  "city": "Bad Annemarie",
  "street": "Müritzstr.",
  "house_number": 50,
  "yearly_kwh_consumption": 1000
}
```