import logging
from flask import Flask, request, jsonify, render_template
import numpy as np
import pickle

app = Flask(__name__)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Load the model
clfmodel = pickle.load(open('clfmodel.pkl', 'rb'))
scaler = pickle.load(open('scaling.pkl', 'rb'))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict_api', methods=['POST'])
def predict_api():
    try:
        data = request.json['data']
        logging.debug(f"Received data for prediction: {data}")
        new_data = scaler.transform(np.array(list(data.values())).reshape(1, -1))
        output = clfmodel.predict(new_data)
        logging.debug(f"Prediction output: {output[0]}")
        return jsonify(output[0])
    except Exception as e:
        logging.error(f"Error in /predict_api: {e}", exc_info=True)
        return jsonify({'error': str(e)}), 500

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = [float(request.form['index']), float(request.form['visit']), float(request.form['m_r_delay']),
                float(request.form['m_f']), float(request.form['hand']), float(request.form['age']),
                float(request.form['educ']), float(request.form['ses']), float(request.form['mmse']),
                float(request.form['cdr']), float(request.form['etiv']), float(request.form['nwbv'])]
        
        logging.debug(f"Received form data for prediction: {data}")
        final_input = scaler.transform(np.array(data).reshape(1, -1))
        output = clfmodel.predict(final_input)[0]
        logging.debug(f"Prediction output: {output}")
        return render_template("home.html", prediction_text="The Dementia Prediction is {}".format(output))
    except Exception as e:
        logging.error(f"Error in /predict: {e}", exc_info=True)
        return render_template("home.html", prediction_text="Error occurred during prediction")

if __name__ == "__main__":
    app.run(debug=True)
