"""
Emotion Detection Web Application

This modules creates a Flask web application that provides a user interface
for detecting emotions in text. The application uses the `emotion_detector` 
function from the `EmotionDetection` package to analyze the input text and 
returns the score of each emotion and the dominated emotion.

To run the application:
    Run this script, and the Flask server will start on host `0.0.0.0` and port `5000`.
"""

from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask("Emotion Detection")

def run_app():
    """
    Main function to run the application.
    """
    app.run(host="0.0.0.0", port=5000)


@app.route("/")
def render_index_page():
    """
    Renders the index page of the web app.
    """
    return render_template('index.html')

@app.route("/emotionDetector")
def get_emotion_detection():
    """
    Analyzes the input text and return the results.
    """
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_analyze)

    if response['dominant_emotion'] is None:
        return 'Invalid text! Please try again!'

    return (
        f"For the given statement, the system response is 'anger': {response['anger']} "
        f"'disgust': {response['disgust']}, 'fear': {response['fear']}, "
        f"'joy': {response['joy']} and 'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )

if __name__ == '__main__':
    run_app()
    