import os
from PIL import Image
from instabot import Bot
import pandas as pd
import time
from pathlib import Path  # Import Path directly

def upload_image(username, password, image_path, caption):
    bot = Bot()
    bot.login(username=username, password=password)

    # Load and resize the image
    img = Image.open(image_path)
    img = img.resize((1080, 1080))
    temp_image_path = "temp_image.jpg"
    img.save(temp_image_path)

    # Upload the image with the specified caption
    bot.upload_photo(temp_image_path, caption=caption)

    # Clean up temporary files
    os.remove(temp_image_path)

    bot.logout()

# Input your Instagram credentials
username = "theuser190901"
password = '21001020014'

# Use raw string or double backslashes to avoid issues with the file path
file_path = r"C:\Users\Administrator\Documents\Python\Top_Posts.csv"
df = pd.read_csv(file_path)

# Iterate through rows using iterrows()
for index, row in df.iterrows():
    caption = row['Title']  # Access 'Title' column in the row
    image_name = row['ID']  # Access 'ID' column in the row
    URL = row['Post URL']
    extension = URL[-4:]  # Extract file extension using pathlib

    if extension == '.jpg':
        image_path = rf"C:\Users\Administrator\Documents\Python\images\{image_name}.jpg"
    elif extension == '.png':
        image_path = rf"C:\Users\Administrator\Documents\Python\images\{image_name}.png"
    else:
        print(f"Unsupported file extension for image {image_name}: {extension}")
        continue  # Skip this iteration if the extension is not supported

    try:
        upload_image(username, password, image_path, caption)
    except Exception as e:
        print(f"Error uploading image {image_name}: {e}")
        bot = Bot()  # Create a new bot instance
        bot.login(username=username, password=password)  # Login again

    time.sleep(1800)
