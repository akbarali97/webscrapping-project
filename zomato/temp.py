# function to download image
import requests
def downimg(url,name,num):
    img = requests.get(url)
    filename = name + str(num)
    with open(f"{filename}.webp", "wb") as f: 
        f.write(img.content)
        f.close()
    return img.content