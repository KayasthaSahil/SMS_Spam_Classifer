from flask import Flask, render_template, request
import pickle
import string
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import os
import re

# Initialize Porter Stemmer
ps = PorterStemmer()

# Set NLTK data path explicitly
nltk_data_dir = os.path.join(os.getcwd(), 'nltk_data')
if not os.path.exists(nltk_data_dir):
    os.makedirs(nltk_data_dir)
nltk.data.path.append(nltk_data_dir)

# Download NLTK resources
try:
    nltk.download('punkt', download_dir=nltk_data_dir)
    nltk.download('stopwords', download_dir=nltk_data_dir)
except Exception as e:
    print(f"Error downloading NLTK data: {e}")

# Simple fallback tokenizer in case NLTK tokenizer fails
def simple_tokenize(text):
    return re.findall(r'\w+', text.lower())

# Function to preprocess the text
def transform_text(text):
    text = text.lower()
    
    # Try using NLTK tokenizer with fallback
    try:
        tokens = nltk.word_tokenize(text)
    except LookupError:
        # Fallback to simple tokenizer if NLTK fails
        tokens = simple_tokenize(text)
    
    try:
        stop_words = set(stopwords.words('english'))
    except LookupError:
        # Fallback stop words if NLTK fails
        stop_words = {'i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 
                      'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 
                      'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 
                      'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 
                      'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 
                      'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 
                      'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 
                      'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 
                      'with', 'about', 'against', 'between', 'into', 'through', 'during', 
                      'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 
                      'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 
                      'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 
                      'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 
                      'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 
                      's', 't', 'can', 'will', 'just', 'don', 'should', 'now'}
    
    filtered_words = []
    for word in tokens:
        if word.isalnum() and word not in stop_words and word not in string.punctuation:
            filtered_words.append(ps.stem(word))
    
    return " ".join(filtered_words)

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-key-for-development')

# Load trained models with error handling
try:
    tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
    model = pickle.load(open('model.pkl', 'rb'))
    print("Models loaded successfully")
except Exception as e:
    print(f"Error loading models: {e}")
    tfidf = None
    model = None

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    prediction = None
    input_message = ""
    error = None
    
    if request.method == 'POST':
        input_message = request.form.get('message', '')
        
        if input_message.strip() != "":
            try:
                # Check if models are loaded
                if tfidf is None or model is None:
                    error = "Model files could not be loaded. Please check server logs."
                else:
                    # Preprocess Input
                    transformed_message = transform_text(input_message)
                    
                    # Vectorize Input
                    vector_input = tfidf.transform([transformed_message])
                    
                    # Make Prediction
                    prediction = model.predict(vector_input)[0]
                    
                    # Set result for template
                    result = "spam" if prediction == 1 else "not_spam"
            except Exception as e:
                error = f"An error occurred: {str(e)}"
                print(f"Error in prediction: {e}")
    
    return render_template('index.html', result=result, input_message=input_message, error=error)

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