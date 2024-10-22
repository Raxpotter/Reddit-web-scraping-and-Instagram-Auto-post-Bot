import praw
import pandas as pd
import cv2
import requests
import numpy as np
import os

reddit_read_only = praw.Reddit(client_id="pNKJOCZjGGBzlNnwINyZ_w",
                               client_secret="ygRTWmZ3ROYNsXr5kC_Q_1ojviX35w",
                               user_agent="RaxPotter")

subreddit = reddit_read_only.subreddit("natureismetal")

# Function to create a folder if it doesn't exist
def create_folder(folder_path):
    if not os.path.isdir(folder_path):
        os.makedirs(folder_path)

# Path setup for saving images and CSV
dir_path = os.path.dirname(os.path.realpath(__file__))
image_path = os.path.join(dir_path, "images/")
ignore_path = os.path.join(dir_path, "ignore_images/")
create_folder(image_path)

# Dictionary to store post information
posts_dict = {
    "Title": [],
    "ID": [],
    "Score": [],
    "Total Comments": [],
    "Post URL": []
}

# Fetch top posts and store their information
for submission in subreddit.hot(limit=30):
    if "jpg" in submission.url.lower() or "png" in submission.url.lower():
        try:
            resp = requests.get(submission.url.lower(), stream=True).raw
            image = np.asarray(bytearray(resp.read()), dtype="uint8")
            image = cv2.imdecode(image, cv2.IMREAD_COLOR)

            compare_image = cv2.resize(image, (224, 224))

            # Get all images to ignore
            ignore_paths = []
            for (dirpath, dirnames, filenames) in os.walk(ignore_path):
                ignore_paths.extend([os.path.join(dirpath, file) for file in filenames])
            ignore_flag = False

            for ignore in ignore_paths:
                ignore = cv2.imread(ignore)
                difference = cv2.subtract(ignore, compare_image)
                b, g, r = cv2.split(difference)
                total_difference = cv2.countNonZero(b) + cv2.countNonZero(g) + cv2.countNonZero(r)
                if total_difference == 0:
                    ignore_flag = True

            if not ignore_flag:
                image_filename = f"{submission.id}.png"
                image_save_path = os.path.join(image_path, image_filename)
                cv2.imwrite(image_save_path, image)
                print(f"Image saved: {image_filename}")

                # Append post information to the dictionary
                posts_dict["Title"].append(submission.title)
                posts_dict["ID"].append(submission.id)
                posts_dict["Score"].append(submission.score)
                posts_dict["Total Comments"].append(submission.num_comments)
                posts_dict["Post URL"].append(submission.url)

        except Exception as e:
            print(f"Image failed. {submission.url.lower()}")
            print(e)

# Save post information to a CSV file
top_posts_df = pd.DataFrame(posts_dict)
csv_file_path = os.path.join(dir_path, "Top_Posts.csv")
top_posts_df.to_csv(csv_file_path, index=True)
print(f"Post data saved to: {csv_file_path}")
