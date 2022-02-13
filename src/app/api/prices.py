import os
import csv
import logging

from fastapi import APIRouter, Request
from app.api.models import LocationInfo
from app.api.helper import validateRequest
from app.api.models import Prices

router = APIRouter()
fileName = os.getenv("FILENAME")
logging.basicConfig(filename="std.log",
                    format='%(asctime)s %(message)s',
                    filemode='w', level=logging.DEBUG)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


@router.post("/", response_model=Prices, status_code=200)
async def calculate_tariff_price(req_info: LocationInfo):
    """
     Use the Tariff Price api to get the total tariff prices for their customers.
    """
    response = {}
    isValidLocation = validateRequest(req_info.json())

    if isValidLocation:
        response = await calculate_price(fileName, req_info)
    return response


async def calculate_price(file_name, locations):
    result = {}
    count = 0
    locationsData = []

    with open(file_name, 'r', encoding='utf-8') as input:
        reader = csv.DictReader(input)
        for record in reader:
            houseNumRange = record['house_number'].split('-')

            # Checking location if any record is empty or missing from location
            if houseNumRange[0] and len(record['postal_code']) and len(record['city']) != 0 and len(
                    record['street']) != 0:
                minHouseRange = int(houseNumRange[0])
                maxHouseRange = int(houseNumRange[1])

                # Check to make sure location is matched and set the counter to keep track of matched record
                if int(record['postal_code']) == locations.zip_code and record['city'] == locations.city and record[
                    'street'] == locations.street and locations.house_number in range(minHouseRange, maxHouseRange):
                    count += 1
                    locationsData.append(record)

    unit_price = 0.0
    grid_fees = 0.0
    kwh_price = 0.0

    # check if there is no location is match return no results
    if count == 0:
        logger.info("No matched location")
        return result
    elif count > 1:
        '''
         Check to calculate the tarrif total price of more than one locations 
         by taking an average price of all match locations 
         i.e unit_price, grid_fees and kWh_price '''

        logger.info("Matched locations count: {}".format(count))
        for item in locationsData:
            unit_price += float(item['unit_price'])
            grid_fees += float(item['grid_fees'])
            kwh_price += float(item['kwh_price'])
        avg_unit_price = unit_price / count
        avg_grid_fees = grid_fees / count
        avg_kwh_price = kwh_price / count

        logger.info("Calculate the average of each location including unit_price, grid_fees, kwh_price")

        total_price = avg_unit_price + avg_grid_fees + (locations.yearly_kwh_consumption * avg_kwh_price)
        result['unit_price'] = avg_unit_price
        result['grid_fees'] = avg_grid_fees
        result['kwh_price'] = avg_kwh_price
        result['total_price'] = total_price

    else:
        logger.info("Matched locations count: {}".format(count))

        # return the total price of one matched location
        total_price = float(locationsData[0]['unit_price']) + float(locationsData[0]['grid_fees']) + (
                locations.yearly_kwh_consumption * float(locationsData[0]['kwh_price']))
        result['unit_price'] = float(locationsData[0]['unit_price'])
        result['grid_fees'] = float(locationsData[0]['grid_fees'])
        result['kwh_price'] = float(locationsData[0]['kwh_price'])
        result['total_price'] = total_price

    logger.info("Done")
    return result
