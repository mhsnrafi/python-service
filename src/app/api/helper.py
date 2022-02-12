import logging

logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S')


def validateRequest(data):
    location = ["zip_code", "city", "street", "house_number"]
    for key in location:
        if key not in data:
            logging.warning("{0} is missing in location request".format(key))
            return False
    return True
