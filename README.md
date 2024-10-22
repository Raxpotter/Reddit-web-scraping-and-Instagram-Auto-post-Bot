# Reddit-web-scraping-and-Instagram-Auto-post-Bot
This project includes two Python scripts that automate data extraction from Reddit and content posting on Instagram.

Reddit Scraper using PRAW:

Uses the PRAW module to interact with the Reddit API.
Retrieves popular image-based posts from a specified subreddit.
Filters unique images by comparing them with previously stored images.
Exports data, including image URLs, into a Pandas DataFrame and saves it as a CSV for further analysis.
Instagram Automation using Selenium & PyAutoGUI:

Automates Instagram login and posting sequence.
Reads post details from a CSV file, uploads images, and adds captions.
Utilizes WebDriver and PyAutoGUI to simulate user actions.
Posts are spaced out with a pause of at least 30 minutes between each.
Concludes by closing the browser session after all posts are uploaded.
This automation enhances social media management by streamlining the processes of data collection and posting across platforms.
