from flask import Flask, render_template, request
import pickle
import numpy as np

app = Flask(__name__)

# Load the trained model
with open('model.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        tmin = float(request.form['tmin'])
        tmax = float(request.form['tmax'])
        prcp = float(request.form['prcp'])

        input_data = np.array([[tmin, tmax, prcp]])
        prediction = model.predict(input_data)
        temp = round(prediction[0], 2)

        # Rain description based on precipitation
        if prcp == 0:
            rain_desc = "No rain expected ☀️"
        elif prcp < 2.5:
            rain_desc = "Light rain 🌦️"
        elif prcp < 7.6:
            rain_desc = "Moderate rain 🌧️"
        else:
            rain_desc = "Heavy rain ⛈️"

        # Final message
        result = f"Predicted <b>Tomorrow's</b> Avg Temperature: <b>{temp} °C</b><br><span style='color:#007bff;'>{rain_desc}</span>"

        return render_template('index.html', prediction=result)

    except Exception as e:
        return render_template('index.html', prediction=f"<span style='color:red;'>Error: {str(e)}</span>")

if __name__ == '__main__':
    app.run(debug=True)
