from flask import Flask, request, render_template
import pickle
import re

app = Flask(__name__)

# Load the classification model
with open('model.pkl', 'rb') as f:
    classifier = pickle.load(f)

# Define a function to preprocess new reviews
def preprocess(review):
    # Remove non-alphanumeric characters
    review = re.sub(r'\W+', ' ', review)
    # Convert to lowercase
    review = review.lower()
    # Split into words
    words = review.split()
    # Remove stopwords
    stopwords = set(['a', 'an', 'the', 'and', 'or', 'but'])
    words = [word for word in words if word not in stopwords]
    # Join the words back into a string
    return ' '.join(words)

# Define a function to classify new reviews
def classify(review):
    # Preprocess the review
    review = preprocess(review)
    # Extract features from the review
    features = {}
    for word in review.split():
        features[word] = 1
    # Classify the review using the model
    sentiment = classifier.classify(features)
    return sentiment

# Define a route to handle the home page
@app.route('/')
def home():
    return render_template('home.html')

# Define a route to handle the form submission
@app.route('/classify', methods=['POST'])
def classify_review():
    # Get the text of the review from the form
    review = request.form['review']
    # Classify the review
    sentiment = classify(review)
    # Render the result template with the sentiment
    return render_template('result.html', sentiment=sentiment)

if __name__ == '__main__':
    app.run(debug=True)
