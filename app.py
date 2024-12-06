from flask import Flask, request, jsonify
import google.generativeai as genai
import requests
import time
from typing_extensions import TypedDict
from typing import List

# Define the schema for the response
class VideoAnalysis(TypedDict):
    description: str
    content_areas: List[str]
    brand: str
    length: str
    ugc_type: str

app = Flask(__name__)

@app.route("/analyze_video", methods=["POST"])
def analyze_video():
    """
    Analyzes a video by downloading it from a provided URL and generating structured output using Generative AI.
    """
    try:
        # Parse the JSON input
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid JSON input"}), 400

        # Extract required fields from the input
        api_key = data.get("api_key")
        video_url = data.get("video_url")
        video_name = data.get("video_name")
        if not api_key or not video_url or not video_name:
            return jsonify({"error": "api_key, video_url, and video_name are required"}), 400

        # Configure Generative AI API
        genai.configure(api_key=api_key)

        # Download the video file
        print(f"Downloading video from {video_url}...")
        response = requests.get(video_url, stream=True)
        if response.status_code != 200:
            return jsonify({"error": "Failed to download video"}), 400

        # Upload the video to Generative AI
        video_file = genai.upload_file(path_or_stream=response.raw, filename=video_name)

        # Wait for file processing to complete
        while video_file.state.name == "PROCESSING":
            print("Processing video...")
            time.sleep(10)
            video_file = genai.get_file(video_file.name)

        if video_file.state.name == "FAILED":
            return jsonify({"error": "Video processing failed"}), 500

        # Define the prompt
        prompt = """
        Analyze the provided UGC video and extract the following details:
        - Description: A brief summary of the content.
        - Content Areas: Choose one or more from [Health, Beauty, Fitness, Other].
        - Brand: The associated brand, if any.
        - Length: Approximate video duration.
        - UGC Type: Classify the content type (e.g., review, tutorial, lifestyle, etc.).
        """

        # Generate content using Generative AI
        print("Generating analysis...")
        model = genai.GenerativeModel("gemini-1.5-pro-latest")
        result = model.generate_content(
            prompt,
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json",
                response_schema=VideoAnalysis
            ),
            request_options={"timeout": 600}  # Ensure sufficient timeout
        )

        # Return the structured analysis result
        print("Analysis completed successfully.")
        return jsonify(result)

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
