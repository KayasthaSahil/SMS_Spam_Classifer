from flask import Flask, render_template, request
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import os

# Initialize Porter Stemmer
ps = PorterStemmer()

# Download NLTK resources if not already downloaded
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)

# Function to preprocess the text
def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    filtered_words = [ps.stem(word) for word in text if word.isalnum() and word not in stopwords.words('english') and word not in string.punctuation]
    
    return " ".join(filtered_words)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-for-development')

# Load trained models
try:
    tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
    model = pickle.load(open('model.pkl', 'rb'))
except FileNotFoundError:
    print("Model files not found. Make sure 'vectorizer.pkl' and 'model.pkl' are in the root directory.")

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    prediction = None
    input_message = ""
    
    if request.method == 'POST':
        input_message = request.form.get('message', '')
        
        if input_message.strip() != "":
            # Preprocess Input
            transformed_message = transform_text(input_message)
            
            # Vectorize Input
            vector_input = tfidf.transform([transformed_message])
            
            # Make Prediction
            prediction = model.predict(vector_input)[0]
            
            # Set result for template
            result = "spam" if prediction == 1 else "not_spam"
    
    return render_template('index.html', result=result, input_message=input_message)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/health')
def health():
    return "Service is up and running", 200

if __name__ == '__main__':
    # Use the PORT environment variable provided by Render
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False) 