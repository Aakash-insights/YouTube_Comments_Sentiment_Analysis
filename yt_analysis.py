import requests
import json
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Set the API endpoint URL
endpoint_url = "https://www.googleapis.com/youtube/v3/commentThreads"

# Set the video ID and API key
video_id = "vS3_72Gb-bI"
api_key = "AIzaSyAjPZjxjnugOGJRbj_hYqdxGY86_I4lXbc"

# Set the API request parameters
params = {
    "part": "snippet",
    "videoId": "X0tOpBuYasI",
    "key": "AIzaSyAjPZjxjnugOGJRbj_hYqdxGY86_I4lXbc",
    "maxResults": 100
}

# Send the API request and retrieve comments
comments = []
while True:
    response = requests.get(endpoint_url, params=params)
    response_json = json.loads(response.text)
    try:
        for item in response_json["items"]:
            comment = item["snippet"]["topLevelComment"]["snippet"]["textDisplay"]
            comments.append(comment)
    except KeyError:
        print("An error occurred while retrieving comments.")
        break
    if "nextPageToken" in response_json:
        params["pageToken"] = response_json["nextPageToken"]
    else:
        break

# Check if any comments were retrieved
if not comments:
    print("No comments were retrieved for this video.")
    exit()

# Initialize the sentiment analyzer
sid = SentimentIntensityAnalyzer()

# Categorize each comment as positive, negative or neutral
num_pos = 0
num_neg = 0
num_neu = 0
for comment in comments:
    sentiment_scores = sid.polarity_scores(comment)
    if sentiment_scores["compound"] > 0:
        num_pos += 1
    elif sentiment_scores["compound"] < 0:
        num_neg += 1
    else:
        num_neu += 1

# Print the number of positive, negative and neutral comments 
print("Number of positive comments:", num_pos)
print("Number of negative comments:", num_neg)
print("Number of neutral comments:", num_neu)

# Define the data for the bar chart
labels = ['Positive', 'Negative', 'Neutral']
sizes = [num_pos, num_neg, num_neu]
colors = ['green', 'red', 'grey']

# Plot the bar chart
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%')
plt.axis('equal')
plt.show()

# Print all the comments
for comment in comments:
    print(comment)
