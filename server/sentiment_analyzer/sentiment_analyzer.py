"""
Sentiment Analyzer Microservice
This can be deployed as a standalone Flask app or IBM Cloud Function.
"""

import json
import os


def analyze_sentiment(text):
    """
    Analyze sentiment of text.
    Returns: positive, negative, or neutral
    """
    if not text or not text.strip():
        return {"sentiment": "neutral", "score": 0, "text": text}

    positive_words = [
        "great", "excellent", "amazing", "fantastic", "wonderful", "good",
        "best", "love", "perfect", "outstanding", "superb", "awesome",
        "happy", "satisfied", "recommend", "helpful", "friendly", "clean",
        "fast", "efficient", "professional", "knowledgeable", "honest",
        "transparent", "fair", "exceptional", "brilliant", "smooth"
    ]
    
    negative_words = [
        "bad", "terrible", "horrible", "awful", "worst", "hate", "poor",
        "disappointing", "unhappy", "rude", "dirty", "slow", "overpriced",
        "broken", "failed", "never", "waste", "problem", "issue", "dishonest",
        "unprofessional", "scam", "fraud", "angry", "frustrated", "terrible"
    ]

    text_lower = text.lower()
    pos_count = sum(1 for word in positive_words if word in text_lower)
    neg_count = sum(1 for word in negative_words if word in text_lower)

    if pos_count > neg_count:
        sentiment = "positive"
        score = min(pos_count / max(pos_count + neg_count, 1), 1.0)
    elif neg_count > pos_count:
        sentiment = "negative"
        score = -min(neg_count / max(pos_count + neg_count, 1), 1.0)
    else:
        sentiment = "neutral"
        score = 0

    return {
        "sentiment": sentiment,
        "score": score,
        "text": text,
        "positive_signals": pos_count,
        "negative_signals": neg_count
    }


def main(params):
    """IBM Cloud Function entry point."""
    text = params.get("text", "")
    result = analyze_sentiment(text)
    return {"statusCode": 200, "body": result}


# Flask app for local/standalone deployment
try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS

    app = Flask(__name__)
    CORS(app)

    @app.route('/analyze', methods=['GET', 'POST'])
    def analyze():
        if request.method == 'POST':
            data = request.get_json(silent=True) or {}
            text = data.get('text', '')
        else:
            text = request.args.get('text', '')
        
        result = analyze_sentiment(text)
        return jsonify(result)

    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({"status": "healthy", "service": "sentiment-analyzer"})

    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)

except ImportError:
    pass  # Flask not available, use as IBM Cloud Function only
