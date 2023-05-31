# Initialize the sentiment analyzer
from nltk.sentiment import SentimentIntensityAnalyzer

sia = SentimentIntensityAnalyzer()


# Function to calculate the sentiment score of a sentence
def calculate_sentiment_score(sentence):
    sentiment = sia.polarity_scores(sentence)
    return sentiment['compound']

# Function to add emotional scores to sentences
def add_emotional_scores(sentences):
    for sentence in sentences:
        sentence.emotion_score = calculate_sentiment_score(str(sentence))
