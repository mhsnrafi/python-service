import csv
import logging

from fastapi import APIRouter, Request
from app.api.models import LocationInfo
from app.api.helper import validateRequest

router = APIRouter()
fileName = '/usr/src/app/location_prices.csv'
logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


@router.post("/", status_code=201)
async def calculate_tarrif_prices(req_info: LocationInfo):
    """
     Processes that calculate the tariff prices for their customers.
    :param req_info: Location object compose of zip_code, city, street, house_number.
    :return: An object with total price, unit price, kwh_price, grid_fees
    """
    response = {}
    isValidLocation = validateRequest(req_info.json())

    if isValidLocation:
        response = await calculatePrice(fileName, req_info)

    return {
        "status": "SUCCESS",
        "data": response
    }


async def calculatePrice(file_name, locations):
    result = {}
    count = 0
    locationsData = []

    with open(file_name, 'r', encoding='utf-8') as input:
        reader = csv.DictReader(input)
        for record in reader:
            houseNumRange = record['house_number'].split('-')
            if houseNumRange[0] and len(record['postal_code']) and len(record['city']) != 0 and len(
                    record['street']) != 0:
                minHouseRange = int(houseNumRange[0])
                maxHouseRange = int(houseNumRange[1])

                if int(record['postal_code']) == locations.zip_code and record['city'] == locations.city and record[
                    'street'] == locations.street and locations.house_number in range(minHouseRange, maxHouseRange):
                    count += 1
                    locationsData.append(record)
                    logging.info("Check the locations count: ", count)

    unit_price = 0.0
    grid_fees = 0.0
    kwh_price = 0.0

    # check if there is no location is match return no results
    if count == 0:
        return result
    elif count > 1:
        # check if there is location is matched more than return the average results
        for item in locationsData:
            unit_price += float(item['unit_price'])
            grid_fees += float(item['grid_fees'])
            kwh_price += float(item['kwh_price'])
        avg_unit_price = unit_price / count
        avg_grid_fees = grid_fees / count
        avg_kwh_price = kwh_price / count

        logging.info("Calculation the average of each location including unit_price, grid_fees, kwh_price")

        total_price = avg_unit_price + avg_grid_fees + (locations.yearly_kwh_consumption * avg_kwh_price)
        result['unit_price'] = avg_unit_price
        result['grid_fees'] = avg_grid_fees
        result['kwh_price'] = avg_kwh_price
        result['total_price'] = total_price

    else:
        # check if there is only location is matched return the result
        logging.info("Calculation the total price of the requested location")

        total_price = float(locationsData[0]['unit_price']) + float(locationsData[0]['grid_fees']) + (
                locations.yearly_kwh_consumption * float(locationsData[0]['kwh_price']))
        result['unit_price'] = float(locationsData[0]['unit_price'])
        result['grid_fees'] = float(locationsData[0]['grid_fees'])
        result['kwh_price'] = float(locationsData[0]['kwh_price'])
        result['total_price'] = total_price

    return result
