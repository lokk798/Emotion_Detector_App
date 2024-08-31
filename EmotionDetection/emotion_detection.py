"""
This module provides a function for detecting emotions in a given text 
using an external API.
"""
from typing import Dict, Optional
import json
import requests
# Constants
URL = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'

HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

# Type alias
EmotionResponse = Dict[str, Optional[float]]

def emotion_detector(text_to_analyse: str) -> EmotionResponse:
    """
    Analyzes the given text to detect emotion using an external API.
    
    Arguments:
    text_to_analyse -- (str) to text to analyze for emotions.
    
    Returns:
    EmotionResponse -- A dictionary containing the detected emotions and their scores, the dominant emotion.
                       If request fails, all values will be None.
    """    
    input_json = { "raw_document": { "text": text_to_analyse } } 
    try:
        response = requests.post(url=URL, json=input_json, headers=HEADERS, timeout=20) 
        
        if response.status_code == 400:
            return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
            }
               
        # Raises an HTTPError for bad responses (4xx and 5xx)
        response.raise_for_status()         
        
        response_data = response.json()
        
        
        emotion_predictions = response_data.get("emotionPredictions", [])
        if not emotion_predictions:
            raise ValueError("No emotion predictions found in the response.")
        
        emotion_scores = emotion_predictions[0].get('emotion', {})
        
        emotions = ['anger', 'disgust', 'fear', 'joy', 'sadness']
        scores = {emotion: emotion_scores.get(emotion, 0.0) for emotion in emotions}
        
        dominant_emotion = max(scores, key=scores.get)
        scores['dominant_emotion'] = dominant_emotion
        
        return scores  
    
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP Error: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request Error: {req_err}")
    except json.JSONDecodeError as json_err:
        print(f"Json Error: {json_err}")    
    # Fallback response if any errors occur.   
    return{
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
          }
        