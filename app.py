from flask import Flask, request, render_template
import pickle

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

# Homepage 
@app.route('/')
def home():
    return render_template('home.html')

# Prediction page 
@app.route('/predict', methods=['GET', 'POST'])
def predict():
    prediction = None
    probability = None

    if request.method == 'POST':
        news_text = request.form['news_text']
        prediction, probability = predict_fake_news(news_text, model='random_forest')
        prediction = 'Real News' if prediction[0] == 1 else 'Fake News'
        probability = round(probability * 100, 2)

    return render_template('predict.html', prediction=prediction, probability=probability)

# ML Info page route
@app.route('/ml-info')
def ml_info():
    return render_template('ml_info.html')

if __name__ == "__main__":
    app.run(debug=True)
