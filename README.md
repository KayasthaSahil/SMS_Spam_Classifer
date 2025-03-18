# Email/SMS Spam Classifier

A machine learning-based Flask application that classifies whether an email or SMS message is spam or not.

## Setup Instructions

### Requirements
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. Clone or download the repository:
```
git clone <repository-url>
```

2. Navigate to the project folder:
```
cd email-spam-classifier
```

3. Install the required packages:
```
pip install -r requirements.txt
```

4. Download NLTK data (if not automatically downloaded):
```python
python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"
```

5. Ensure you have the model files in the root directory:
   - `vectorizer.pkl` - TF-IDF vectorizer
   - `model.pkl` - Trained classification model

### Running the Application Locally

To start the application:
```
python app.py
```

Open your browser and navigate to `http://127.0.0.1:5000`.

## Deployment on Render

This application is configured for deployment on Render.

### Deployment Steps

1. Create a new Web Service on Render.
2. Connect your GitHub repository.
3. Use the following settings:
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt && python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"`
   - **Start Command**: `gunicorn app:app`

Or, you can use the `render.yaml` file in this repository to set up a Blueprint for deployment.

## Project Structure

```
email-spam-classifier/
│
├── app.py                  # Main Flask application file
├── requirements.txt        # Package dependencies
├── model.pkl               # Trained machine learning model
├── vectorizer.pkl          # TF-IDF vectorizer
│
├── static/                 # Static files (CSS, JS)
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── main.js
│
└── templates/              # HTML templates
    ├── base.html
    ├── index.html
    └── about.html
```

## Features

- User-friendly interface for message input
- Real-time spam classification
- Responsive design
- Detailed about page explaining the technology
- Machine learning-based classification using TF-IDF and NLP techniques

## How It Works

1. User enters a message in the text field and submits it
2. The application preprocesses the text (lowercases, tokenizes, removes stopwords, and stems)
3. The preprocessed text is vectorized using TF-IDF
4. The machine learning model predicts whether the message is spam or not
5. The result is displayed to the user

## Technology Stack

- **Flask**: Web framework
- **NLTK**: Natural Language Processing toolkit
- **Scikit-learn**: Machine learning library
- **HTML/CSS/JS**: Frontend development 