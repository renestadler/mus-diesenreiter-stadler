from io import BytesIO
from urllib.request import urlopen

import requests
from PIL import Image


async def get_recycling_data(barcode):
    response = await retrieve_data(barcode)
    if response is None:
        return None
    return response['name'], retrieve_packaging(response['packagings']), (await retrieve_image(response['image']))


async def retrieve_data(barcode):
    try:
        # response = requests.get(f'https://recycling-server.azurewebsites.net/product?barcode={barcode.data.decode("utf-8")}')
        response = requests.get(f'http://localhost:8080/product?barcode={barcode.data.decode("utf-8")}')

        return response.json()
    except:
        print("Can not establish connection to backend")
        return None


async def retrieve_image(image_url):
    try:
        u = urlopen(image_url)
        raw_data = u.read()
        u.close()
        return Image.open(BytesIO(raw_data))
    except:
        print("Can not open product image")
        return Image.open("logos/no_image.png")


def retrieve_packaging(packaging_list):
    return [item['name'] for item in packaging_list]
