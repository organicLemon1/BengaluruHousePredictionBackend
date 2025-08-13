from flask import Flask, request, jsonify
import util

app = Flask(__name__)

# Load artifacts at startup
util.load_saved_artifacts()
print("Server starting... Locations available:", util.get_location_names())

# Endpoint to get all location names
@app.route('/get_location_names', methods=['GET'])
def get_locations():
    response = jsonify({
        'locations': util.get_location_names()
    })
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# Endpoint to predict house price
@app.route('/predict_home_price', methods=['POST'])
def predict_home_price():
    try:
        data = request.form
        total_sqft = float(data.get('total_sqft', 0))
        location = data.get('location', '')
        bhk = int(data.get('bhk', 0))
        bath = int(data.get('bath', 0))

        # Validate input
        if total_sqft <= 0 or bhk <= 0 or bath <= 0 or not location:
            return jsonify({'error': 'Invalid input', 'details': 'Missing or incorrect fields'}), 400

        estimated_price = util.get_estimated_price(location, total_sqft, bhk, bath)
        response = jsonify({'estimated_price': estimated_price})
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        return jsonify({'error': 'Prediction failed', 'details': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)  # Use debug=False in production
