from flask import Flask, request, render_template
import pickle
import time
import psutil
import os

app = Flask(__name__)

# load pickle
with open('C:/Users/Lina/Desktop/FYP/fyp2/FNDWebApp/models/random_forest_model.pkl', 'rb') as f:
    rf_model = pickle.load(f)

with open('C:/Users/Lina/Desktop/FYP/fyp2/FNDWebApp/models/naive_bayes_model.pkl', 'rb') as f:
    nb_model = pickle.load(f)

with open('C:/Users/Lina/Desktop/FYP/fyp2/FNDWebApp/models/count_vectorizer.pkl', 'rb') as f:
    count_vectorizer = pickle.load(f)

# Prediction function
def predict_fake_news(text, model='random_forest'):
    text_vectorized = count_vectorizer.transform([text])

    if model == 'random_forest':
        prediction = rf_model.predict(text_vectorized)
        probability = rf_model.predict_proba(text_vectorized)[0][1]
    elif model == 'naive_bayes':
        prediction = nb_model.predict(text_vectorized)
        probability = nb_model.predict_proba(text_vectorized)[0][1]

    return prediction, probability

# Prediction  
@app.route("/predict", methods=["POST"])
def predict():
    news_text = request.form["news_text"]

    process = psutil.Process(os.getpid())
    start_mem = process.memory_info().rss / (1024 * 1024)  # in MB
    start_time = time.time()

    # Prediction
    prediction_result, probability = predict_fake_news(news_text, model='random_forest')

    end_time = time.time()
    end_mem = process.memory_info().rss / (1024 * 1024)  # in MB

    execution_time = round(end_time - start_time, 4)
    memory_usage = round(end_mem - start_mem, 4)

    print(f"Execution Time: {execution_time} seconds")
    print(f"Memory Used: {memory_usage} MB")

    prediction = "Real News" if prediction_result[0] == 1 else "Fake News"
    probability = round(probability * 100, 2)

    return render_template("home.html", prediction=prediction, probability=probability)


# Homepage 
@app.route('/')
def home():
    return render_template('home.html')

# FAQ page route
@app.route('/faq')
def faq():
    return render_template('faq.html')

# process page route
@app.route('/process')
def process():
    return render_template('process.html')

# accuracy page route
@app.route('/accuracy')
def accuracy():
    return render_template('accuracy.html')

# AI_info page route
@app.route('/AI_info')
def AI_info():
    return render_template('AI_info.html')

# contact page route
@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
