from flask import Flask, request, jsonify
import joblib
import numpy as np

app = Flask(__name__)

# Load your machine learning model
model = joblib.load("model.joblib")

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get input data from the POST request
        data = request.get_json()
        
        # Perform data preprocessing, if needed
        raw_data = data['features']
        processed_data = np.array(raw_data).reshape(1, -1)

        # Make predictions using the loaded model
        predictions = model.predict(processed_data)

        # You can return predictions as JSON
        return jsonify({"predictions": predictions.tolist()})
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)