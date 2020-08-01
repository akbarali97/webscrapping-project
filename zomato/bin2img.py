# To convert base64 file to image file use this code
import base64
from pymongo import MongoClient
client = MongoClient('localhost', 27017)
hotelObject = client.khra.hotels
h = hotelObject.find({"hotel_name":"Zam Zam Palayam"})
for i in h:
    img = i['img']
    with open("temp.webp", "wb") as f:f.write(base64.b64decode(img))


