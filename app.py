from flask import Flask, render_template, request, jsonify
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

app = Flask(__name__)
analyzer = SentimentIntensityAnalyzer()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.get_json()
    text = data.get('text', '')
    
    if not text:
        return jsonify({'error': 'No text provided'})

    # The Logic: VADER gives a "compound" score from -1 to 1
    scores = analyzer.polarity_scores(text)
    compound = scores['compound']

    # Determine Mood with slightly adjusted thresholds
    if compound >= 0.05:
        mood = "Positive 😊"
        color = "text-green-500"
        bg_color = "bg-green-100"
        border_color = "border-green-400"
    elif compound <= -0.05:
        mood = "Negative 😠"
        color = "text-red-500"
        bg_color = "bg-red-100"
        border_color = "border-red-400"
    else:
        mood = "Neutral 😐"
        color = "text-gray-500"
        bg_color = "bg-gray-100"
        border_color = "border-gray-400"

    return jsonify({
        'mood': mood,
        'score': round(compound, 2),
        'subjectivity': "N/A", # VADER doesn't do subjectivity, so we hide it or remove it
        'color': color,
        'bg_color': bg_color,
        'border_color': border_color
    })

if __name__ == '__main__':
    app.run(debug=True)