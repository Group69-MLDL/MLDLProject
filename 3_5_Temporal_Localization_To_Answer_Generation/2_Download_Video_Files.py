

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import urllib.request
import os.path
import json

# Start a headless Edge browser
options = webdriver.EdgeOptions()
#options.add_argument('--headless')
driver = webdriver.Edge(options=options)

# Read JSON file and extract unique video_uids
with open("inputs/top_50_queries.json", "r") as f:
    data = json.load(f)
video_uids = list(entry["video_uid"] for entry in data)

#login procedure
driver.get('https://visualize.ego4d-data.org/login')
time.sleep(1)
driver.find_element(By.CLASS_NAME, "bp3-input").send_keys('AKIATEEVKTGZAJ4F575I')
driver.find_element(By.CLASS_NAME, 'bp3-button-text').click()

counter = 0
skipped_counter = {}
for uid in video_uids:
    if(uid == "unknown"):
        counter += 1
        print(f'[{counter}]')
        print(f"Unknown video_uid")
    elif(os.path.isfile("videos/"+f"{uid}.mp4")):
        counter += 1
        if(uid not in skipped_counter.keys()):
            skipped_counter[uid] = 0
        else:
            skipped_counter[uid] += 1
        print(f'[{counter}]')
        print(f"{uid}.mp4 already exists!\nskipped {skipped_counter[uid]} times!")
    else:
        video_url = f"https://visualize.ego4d-data.org/{uid}?v=%22Ego4D+v1%22&s=%22{uid}%22"
        driver.get(video_url)
        time.sleep(10)  # adjust as needed for page load

        # Extract the video src attribute
        video_element = driver.find_element(By.TAG_NAME, "video")
        video_download_url = video_element.get_attribute("src")
        counter += 1
        print(f'[{counter}]')
        print(f"Video UID: {uid}")
        print(f"Download URL: {video_download_url}")
        urllib.request.urlretrieve(f"{video_download_url}", "videos/"+f"{uid}.mp4")

driver.quit()

for uid, count in skipped_counter.items():
    if count > 0:
        print(f"{uid}: skipped {count} times")

# Load the top_50_queries.json file
with open('inputs/top_50_queries.json', 'r') as f:
    top_50_queries = json.load(f)

# Extract IoUs
ious = [query["avg_iou"] for query in top_50_queries]

import matplotlib.pyplot as plt

# Plotting
plt.figure(figsize=(10, 6))
plt.hist(ious, bins=20, edgecolor='black', color='skyblue')
plt.title('IoU Distribution of Top 50 Queries')
plt.xlabel('Average IoU')
plt.ylabel('Frequency')
plt.grid(axis='y', alpha=0.35)
plt.savefig('iou_distribution.png')
plt.show()

# plot skipped_counter for keys above 0
skipped_counter_trimmed = {k: v for k, v in skipped_counter.items() if v > -1}
skipped_counter_trimmed = {k[:8]: v for k, v in skipped_counter_trimmed.items()}

plt.figure(figsize=(10, 6))
plt.bar(skipped_counter_trimmed.keys(), skipped_counter_trimmed.values(),edgecolor='black', color='skyblue')

plt.title('Duplicate Videos Count')
plt.xlabel('Video UID')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')
plt.grid(axis='y', alpha=0.35)
plt.tight_layout()
plt.savefig('duplicate_videos_count.png')
# Show the plots
plt.show()