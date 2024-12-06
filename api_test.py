import requests

# Base URL of the Flask app
# base_url = 'https://vid-analyzer.onrender.com/analyze_video'  # Update this if deploying to a live server
base_url = 'http://127.0.0.1:5000/analyze_video'  # Update this if deploying to a live server


# JSON payload
payload = {
    "api_key": "AIzaSyC-54TKhNVfWmPQjb8nyXdLsKoN4mw765I",
    "video_url": "https://storage.googleapis.com/portfolio-videos/76_Alyssa%20Cayabyab.mp4",
    "video_name": "76_Alyssa Cayabyab.mp4"
}

# Send POST request
response = requests.post(base_url, json=payload)

# Print the response
if response.status_code == 200:
    print("Response:", response.json())
else:
    print("Error:", response.status_code, response.text)
