import boto3
from dotenv import load_dotenv
import os

# Load credentials from .env file
load_dotenv()

# Connect to AWS Comprehend
comprehend = boto3.client(
    'comprehend',
    region_name=os.getenv("AWS_REGION"),
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY")
)

def analyze_sentiment(text):
    """Analyze the sentiment of a customer message"""
    try:
        response = comprehend.detect_sentiment(
            Text=text,
            LanguageCode='en'
        )
        sentiment = response['Sentiment']
        score = response['SentimentScore']
        return {
            "sentiment": sentiment,
            "score": score
        }
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return {
            "sentiment": "NEUTRAL",
            "score": {}
        }

def detect_intent(text):
    """Detect key phrases to understand customer intent"""
    try:
        response = comprehend.detect_key_phrases(
            Text=text,
            LanguageCode='en'
        )
        phrases = [phrase['Text'].lower() for phrase in response['KeyPhrases']]

        # Simple intent detection based on keywords
        if any(word in phrases for word in ['bill', 'charge', 'payment', 'invoice']):
            return 'billing'
        elif any(word in phrases for word in ['password', 'login', 'error', 'bug', 'crash']):
            return 'technical'
        else:
            return 'general'
    except Exception as e:
        print(f"Error detecting intent: {e}")
        return 'general'

# Test the tools
if __name__ == "__main__":
    test_messages = [
        "I am really frustrated! My bill is wrong and nobody is helping me!",
        "Hi, I just wanted to say your service is amazing!",
        "I cannot login to my account, keeps showing error"
    ]

    print("Testing AWS Comprehend Sentiment Analysis...\n")
    for message in test_messages:
        print(f"Message: {message}")
        sentiment = analyze_sentiment(message)
        intent = detect_intent(message)
        print(f"Sentiment: {sentiment['sentiment']}")
        print(f"Intent: {intent}")
        print("-" * 50)